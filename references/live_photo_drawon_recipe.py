"""
RECIPE · 实况图 live photo · 手绘线稿 draw-on 动画
==================================================
design-workflow 技能参考实现：把"照片 + 手绘线稿叠加"从静态合成推进到
"逐笔绘制动效"。照片作底 100% 不动，线条层用 stroke-dashoffset 一笔笔画出
（draw-on），做成会"活过来"的实况图。

对应技能段（已抽离为专项子技能）：
  - subskills/design-photo-sketch/SKILL.md「第三部分 · 实况图 live photo · 手绘线稿 draw-on 动画」
  - subskills/design-photo-sketch/SKILL.md（draw-on 双模式动画见该子技能）

依赖：numpy, opencv-python-headless, Pillow（无网络、沙箱可直接跑）

═══════════════════════════════════════════════════════════════
核心原则（用户纠正 · 本管线红线）——只适用于「实况图 live photo」管线，
不上升为通用设计原则（详见 subskills/design-photo-sketch）。
  1. 必须基于真实轮廓：任何补全 / 拟人化线条，端点必须取自真实提取 / 构造
     的主体轮廓上的点，绝不在轮廓之外另造漂浮几何（如独立的 bbox 圆脸、
     悬浮星星、自己造的梨形身子）。
  2. 整体衔接：补全 / 拟人化线条要从轮廓的对应点「长」出去，连成一个整体，
     禁止各画各的拼贴（即便分两幕，第二幕也要从第一幕的轮廓点衔接）。
  3. 线条流畅：全身统一一种曲线语言（Chaikin 平滑 + 重采样），不混入第二种
     生硬线型（如垂直硬腿）。
  4. 不替用户加元素：拟人化 / 装饰（脸、星）默认关闭，加不加由用户选择。
═══════════════════════════════════════════════════════════════

用法：
  python live_photo_drawon_recipe.py --mode trace  --src 原图.jpg --out 目录
  python live_photo_drawon_recipe.py --mode persona --src 原图.jpg --out 目录
  （--decor 开启可选的装饰性脸 / 星，非整体衔接，需用户明确选择）

产出：<OUT>/live_<mode>_static.png  <OUT>/live_<mode>.gif  <OUT>/live_<mode>.html
"""
import os, base64, math, argparse, io
import numpy as np
import cv2
from PIL import Image, ImageDraw

# ============================ 可配置项 ============================
SRC = r"D:/shujuchucun/yundong/图片/original_cloud.jpg"   # ← 改成你的原图
OUT = r"D:/shujuchucun/yundong/图片"                      # ← 产物输出目录

MODE      = "trace"   # 'trace' 只描真实轮廓 | 'persona' 基于轮廓+整体衔接创造人形
ADD_DECOR = False     # 装饰性脸/星（非整体衔接，需用户明确选择才开，见 --decor）
TOP_N      = 18       # trace 模式保留的最长轮廓数
TARGET_TOTAL = 3.2    # 描轮廓总时长（秒）
MIN_LEN    = 50       # 短于该像素的轮廓丢弃（去碎线）
ACT        = 4.5      # persona 模式整体 draw-on 时长（秒）
# =================================================================

INK   = (244, 240, 230)   # 轮廓白
FACE  = (58, 54, 64)      # 柔黑墨（眼/嘴，在白云上要可读）
PINK  = (233, 90, 174)    # 腮红
WHITE = (255, 255, 255)   # 高光


# ----------------------------- 工具函数 -----------------------------
def chaikin(pts, iters=2):
    pts = np.asarray(pts, dtype=np.float64)
    for _ in range(iters):
        new = [pts[0]]
        for i in range(len(pts) - 1):
            p, q = pts[i], pts[i + 1]
            new.append(p * 0.75 + q * 0.25)
            new.append(p * 0.25 + q * 0.75)
        pts = np.asarray(new)
    return pts


def chaikin_closed(pts, iters=3):
    pts = np.asarray(pts, dtype=np.float64)
    for _ in range(iters):
        new, n = [], len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            new.append(p * 0.75 + q * 0.25)
            new.append(p * 0.25 + q * 0.75)
        pts = np.asarray(new)
    return pts


def resample(pts, step=3.0):
    pts = np.asarray(pts, dtype=np.float64)
    if len(pts) < 2:
        return pts
    out = [pts[0]]
    acc = 0.0
    for i in range(1, len(pts)):
        seg = pts[i] - pts[i - 1]
        L = np.linalg.norm(seg)
        if L < 1e-3:
            continue
        while acc + L >= step:
            t = (step - acc) / L
            out.append(pts[i - 1] + seg * t)
            pts[i - 1:] = (pts[i - 1] + seg * t, *pts[i:])
            seg = pts[i] - pts[i - 1]
            L = np.linalg.norm(seg)
            acc = 0.0
        acc += L
    out.append(pts[-1])
    return np.asarray(out)


def plen(pts):
    if len(pts) < 2:
        return 0.0
    return float(np.sum(np.linalg.norm(np.diff(pts, axis=0, prepend=pts[:1]), axis=1)))


def pts_str(pts):
    return ' '.join('%.1f,%.1f' % (x, y) for x, y in pts)


def smooth(control, step=3.0, iters=2):
    return resample(chaikin(np.asarray(control, dtype=np.float64), iters=iters), step=step)


def ellipse_pts(cx, cy, rx, ry, n=64, rot=0.0):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    xs, ys = rx * np.cos(t), ry * np.sin(t)
    if rot:
        c, s = math.cos(rot), math.sin(rot)
        xs, ys = xs * c - ys * s, xs * s + ys * c
    return np.stack([cx + xs, cy + ys], axis=1)


def arc_pts(cx, cy, rx, ry, a0, a1, n=22):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a))
            for a in np.linspace(a0, a1, n)]


def sparkle(cx, cy, R, r):
    pts = []
    for i in range(8):
        ang = -math.pi / 2 + i * math.pi / 4
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    pts.append(pts[0])
    return np.array(pts)


def draw_partial(d, pts, ratio, color, w):
    if ratio <= 0 or len(pts) < 2:
        return
    cum = np.linalg.norm(np.diff(pts, axis=0, prepend=pts[:1]), axis=1)
    target = cum.sum() * ratio
    idx = int(np.searchsorted(np.cumsum(cum), target))
    idx = max(1, min(len(pts) - 1, idx))
    sub = pts[:idx + 1]
    if len(sub) >= 2:
        d.line([tuple(p) for p in sub], fill=color, width=w, joint='curve')


# ----------------------------- 提取轮廓 -----------------------------
def extract_contours(img_arr):
    """Canny + 闭运算 + 只取外轮廓。返回 (contours, H, W)。
    适合背景纯色/低纹的图（如蓝天白云、建筑窗格不抢边）。"""
    H, W = img_arr.shape[:2]
    gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 1.5)
    edges = cv2.Canny(blur, 45, 130)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, H, W


def extract_subject_hsv(img_arr):
    """HSV 高亮 + 低饱和：提取"主体"（云朵/亮前景），避开天空/楼面。
    适合构图里有大量边缘干扰（楼宇、街景）的图。
    返回 (contours, H, W)。"""
    H, W = img_arr.shape[:2]
    hsv = cv2.cvtColor(img_arr, cv2.COLOR_RGB2HSV)
    sat = hsv[..., 1].astype(np.int32)
    val = hsv[..., 2].astype(np.int32)
    # 中部带 mask 收紧，避免边缘楼越界
    m = np.zeros((H, W), np.uint8)
    m[:, int(W * 0.10):int(W * 0.90)] = 255
    body = ((val > 178) & (sat < 55) & (m > 0)).astype(np.uint8) * 255
    body = cv2.morphologyEx(body, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    body = cv2.morphologyEx(body, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(body, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, H, W


def main_contour_from(contours, H, W):
    """取最大面积外轮廓作主主体，重采样 + 重度 Chaikin，得到真实轮廓线。
    若 contours 为空返回 None。"""
    if not contours:
        return None
    c = max(contours, key=cv2.contourArea).reshape(-1, 2).astype(np.float64)
    # 中央 mask：避免抓到底部楼面、左右楼宇等干扰
    m = np.zeros((H, W), np.uint8)
    m[int(H * 0.05):int(H * 0.80), int(W * 0.20):int(W * 0.80)] = 255
    c = c[(m[c[:, 1].astype(int), c[:, 0].astype(int)] > 0)]
    if len(c) < 5:
        return None
    g = resample(chaikin_closed(c, iters=3), step=4.0)
    return g


# ----------------------------- 模式 A：trace（只描真实轮廓） -----------------------------
def build_trace(contours, H, W):
    raw = []
    for c in contours:
        pts = c.reshape(-1, 2).astype(np.float64)
        L = plen(pts)
        if L < MIN_LEN:
            continue
        s = cv2.approxPolyDP(c, epsilon=2.5, closed=False).reshape(-1, 2).astype(np.float64)
        if len(s) < 3:
            continue
        raw.append({'pts': chaikin(s, iters=2), 'len': L})
    raw.sort(key=lambda x: -x['len'])
    kept = raw[:TOP_N]
    # 自上而下时序
    kept.sort(key=lambda x: x['pts'][:, 1].min())
    total_len = sum(s['len'] for s in kept) or 1.0
    raw_durs = [max(0.25, min(0.9, s['len'] / total_len * 0.7)) for s in kept]
    scale = TARGET_TOTAL / (sum(raw_durs) or 1.0)
    t = 0.0
    for s, dd in zip(kept, raw_durs):
        s['dur'] = dd * scale
        s['start'] = t
        t += s['dur'] * 0.4
        s['color'] = INK
        s['width'] = 3
    return kept, t + kept[-1]['dur'] * 0.6 + 0.2


# ----------------------------- 模式 B：persona（基于轮廓 + 整体衔接） -----------------------------
def build_persona(contour, H, W):
    """基于真实主体轮廓，从轮廓点长出头/颈/臂/发/裙裾，连成一个整体。
    所有补全线端点取自 contour 上的点 → 满足「基于轮廓 + 整体衔接」。"""
    g0 = np.asarray(contour, dtype=np.float64)
    top_idx = int(np.argmin(g0[:, 1]))           # 云顶最高点 → 接颈/头
    gown = np.roll(g0, -top_idx, axis=0)
    if not np.allclose(gown[0], gown[-1]):
        gown = np.vstack([gown, gown[0]])        # 闭合
    gy = gown[:, 1]; gx = gown[:, 0]             # 闭合后重算，保证索引对齐
    top_pt = gown[0]                             # = 真实轮廓顶点
    cx = float(gx.mean())
    ymin, ymax = float(gy.min()), float(gy.max())

    # 关键衔接点（全部取自 gown 上的点 → 保证「整体」）
    bot_y = float(gy.max())
    bot_mask = gy > bot_y - 28
    bot_pts = gown[bot_mask]
    bot_L = bot_pts[np.argmin(bot_pts[:, 0])]
    bot_R = bot_pts[np.argmax(bot_pts[:, 0])]
    bot_M = bot_pts[np.argmin(np.abs(bot_pts[:, 0] - cx))]

    # 云轮廓本身就是「头 + 身」（用户纠正：不要再额外加椭圆头）。
    # 只从云底端点接裙裾，让云底顺势垂落成裙摆 → 女子意象，不画硬腿、不加手。
    hem_L = smooth([[bot_L[0], bot_L[1]], [bot_L[0] - 26, ymax + 160], [bot_L[0] - 10, ymax + 345]], step=4.5)
    hem_M = smooth([[bot_M[0], bot_M[1]], [bot_M[0] + 14, ymax + 170], [bot_M[0] - 6, ymax + 345]], step=4.5)
    hem_R = smooth([[bot_R[0], bot_R[1]], [bot_R[0] + 26, ymax + 160], [bot_R[0] + 10, ymax + 345]], step=4.5)

    lines = [
        ('gown', gown, 5.0),
        ('hem_L', hem_L, 5.5),
        ('hem_M', hem_M, 5.5),
        ('hem_R', hem_R, 5.5),
    ]
    lines = [{'key': k, 'pts': p, 'color': INK, 'width': wd, 'mode': 'draw'} for k, p, wd in lines]
    return lines


def build_persona_timeline(lines):
    """保底正数时长公式：任意笔数都不会出现负时长/负起笔。"""
    N = len(lines)
    if N == 0:
        return 0.0
    Ltot = sum(max(1.0, plen(l['pts'])) for l in lines)
    base = max(0.20, ACT * 0.35 / N)
    spread = max(ACT - base * N, ACT * 0.1)
    acc = 0.0
    for l in lines:
        L = max(1.0, plen(l['pts']))
        l['dur'] = base + (L / Ltot) * spread
        l['start'] = acc * 0.78
        acc += l['dur']
    return lines[-1]['start'] + lines[-1]['dur'] + 0.5


# ----------------------------- 装饰（非整体衔接 · 可选 · 需用户选） -----------------------------
def build_decor(main_contour, W, H, end_t):
    """装饰性脸/星：明确标注为「额外点缀、非整体衔接、需用户明确选择」。
    默认关闭，开启即表示用户接受「加元素」。"""
    extras = []
    if main_contour is None:
        return extras, end_t
    bx, by, bw, bh = cv2.boundingRect(main_contour.reshape(-1, 1, 2).astype(np.int32))
    cx, cyc = bx + bw / 2, by + bh / 2
    t2 = end_t + 0.15
    eye_gap = bw * 0.15
    eye_y = cyc - bh * 0.04
    eye_r = max(7.0, bw * 0.040)
    for sx in (-1, 1):
        ex = cx + sx * eye_gap
        extras.append({'kind': 'dot', 'pos': (ex, eye_y), 'r': eye_r,
                       'color': FACE, 'start': t2, 'dur': 0.25})
        extras.append({'kind': 'dot', 'pos': (ex - eye_r * 0.3, eye_y - eye_r * 0.35),
                       'r': eye_r * 0.38, 'color': WHITE, 'start': t2 + 0.1, 'dur': 0.2})
    smile = arc_pts(cx, eye_y + bh * 0.10, bw * 0.20, bh * 0.07, math.radians(20), math.radians(160))
    extras.append({'kind': 'line', 'pts': np.array(smile), 'color': FACE,
                   'width': 3, 'start': t2 + 0.25, 'dur': 0.5})
    for sx in (-1, 1):
        blx, bly = cx + sx * bw * 0.27, eye_y + bh * 0.07
        extras.append({'kind': 'blush', 'pos': (blx, bly), 'rx': bw * 0.06,
                       'ry': bh * 0.035, 'color': PINK, 'start': t2 + 0.5, 'dur': 0.35})
    return extras, t2 + 0.9


# ----------------------------- 导出 -----------------------------
def export(lines, extras, img_arr, W, H, OUT, mode, end_t):
    img0 = Image.fromarray(img_arr)
    # 静态合层
    drawn = img0.copy()
    d = ImageDraw.Draw(drawn)
    for l in lines:
        d.line([tuple(x) for x in l['pts']], fill=tuple(l['color']),
               width=int(round(l['width'])), joint='curve')
    for e in extras:
        if e['kind'] == 'line':
            d.line([tuple(x) for x in e['pts']], fill=e['color'],
                   width=int(e['width']), joint='curve')
        elif e['kind'] == 'dot':
            d.ellipse([e['pos'][0] - e['r'], e['pos'][1] - e['r'],
                       e['pos'][0] + e['r'], e['pos'][1] + e['r']], fill=e['color'])
        elif e['kind'] == 'blush':
            d.ellipse([e['pos'][0] - e['rx'], e['pos'][1] - e['ry'],
                       e['pos'][0] + e['rx'], e['pos'][1] + e['ry']], fill=e['color'])
    sp = os.path.join(OUT, f'live_{mode}_static.png')
    drawn.save(sp)
    print('static ->', sp)

    # HTML（draw-on + pop）
    bio = io.BytesIO()
    img0.convert('RGB').save(bio, 'JPEG', quality=88)
    b64 = base64.b64encode(bio.getvalue()).decode()
    svg = []
    for l in lines:
        L = plen(l['pts'])
        col = '#%02X%02X%02X' % l['color']
        svg.append(
            f'<polyline points="{pts_str(l["pts"])}" fill="none" stroke="{col}" '
            f'stroke-width="{l["width"]:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-dasharray="{L:.1f}" '
            f'stroke-dashoffset="{L:.1f}" '
            f'style="animation: draw {l["dur"]:.2f}s ease-out {l["start"]:.2f}s forwards"/>')
    for e in extras:
        if e['kind'] == 'line':
            L = plen(e['pts']); col = '#%02X%02X%02X' % e['color']
            svg.append(
                f'<polyline points="{pts_str(e["pts"])}" fill="none" stroke="{col}" '
                f'stroke-width="{e["width"]:.1f}" stroke-linecap="round" '
                f'stroke-linejoin="round" stroke-dasharray="{L:.1f}" '
                f'stroke-dashoffset="{L:.1f}" '
                f'style="animation: draw {e["dur"]:.2f}s ease-out {e["start"]:.2f}s forwards"/>')
        elif e['kind'] == 'dot':
            col = '#%02X%02X%02X' % e['color']
            svg.append(f'<circle cx="{e["pos"][0]:.1f}" cy="{e["pos"][1]:.1f}" r="{e["r"]:.1f}" '
                       f'fill="{col}" opacity="0" style="animation: pop {e["dur"]:.2f}s ease-out {e["start"]:.2f}s forwards"/>')
        elif e['kind'] == 'blush':
            col = '#%02X%02X%02X' % e['color']
            svg.append(f'<ellipse cx="{e["pos"][0]:.1f}" cy="{e["pos"][1]:.1f}" rx="{e["rx"]:.1f}" '
                       f'ry="{e["ry"]:.1f}" fill="{col}" opacity="0" style="animation: pop {e["dur"]:.2f}s ease-out {e["start"]:.2f}s forwards"/>')
    TEMPL = """<!doctype html><html><head><meta charset="utf-8"><style>
@keyframes draw { to { stroke-dashoffset: 0; } }
@keyframes pop { from { opacity:0; } to { opacity:1; } }
body { margin:0; background:#0e1217; display:flex; justify-content:center; }
.wrap { position:relative; width:420px; max-width:100%; margin:24px auto; }
img { width:100%; display:block; }
svg { position:absolute; inset:0; width:100%; height:100%; }
</style></head><body><div class="wrap">
<img src="data:image/jpeg;base64,__B64__">
<svg viewBox="0 0 __W__ __H__">__SVG__</svg>
</div></body></html>"""
    html = (TEMPL.replace('__B64__', b64).replace('__W__', str(W)).replace('__H__', str(H))
            .replace('__SVG__', '\n'.join(svg)))
    hp = os.path.join(OUT, f'live_{mode}.html')
    open(hp, 'w', encoding='utf-8').write(html)
    print('html   ->', hp)

    # GIF
    fps = 15
    n_frames = int((end_t + (max([e['start'] + e['dur'] for e in extras], default=end_t))) * fps) + 4
    GIF_W, GIF_H = 360, 504
    orig_small = img0.resize((GIF_W, GIF_H), Image.LANCZOS)
    sw, sh = GIF_W / W, GIF_H / H
    lines_s = [{'pts': l['pts'] * np.array([sw, sh]), 'start': l['start'], 'dur': l['dur'],
                'color': l['color'], 'width': l['width']} for l in lines]
    ext_s = []
    for e in extras:
        if e['kind'] == 'line':
            ext_s.append({'kind': 'line', 'pts': e['pts'] * np.array([sw, sh]), 'color': e['color'],
                          'width': max(1, int(e['width'] * sw)), 'start': e['start'], 'dur': e['dur']})
        elif e['kind'] == 'dot':
            ext_s.append({'kind': 'dot', 'pos': (e['pos'][0] * sw, e['pos'][1] * sh),
                          'r': max(1, e['r'] * sw), 'color': e['color'], 'start': e['start']})
        elif e['kind'] == 'blush':
            ext_s.append({'kind': 'blush', 'pos': (e['pos'][0] * sw, e['pos'][1] * sh),
                          'rx': e['rx'] * sw, 'ry': e['ry'] * sh, 'color': e['color'], 'start': e['start']})
    frames = []
    for k in range(n_frames):
        tt = k / fps
        frame = orig_small.copy()
        d = ImageDraw.Draw(frame)
        for l in lines_s:
            r = max(0.0, min(1.0, (tt - l['start']) / l['dur']))
            if r <= 0:
                continue
            draw_partial(d, l['pts'], r, tuple(l['color']), w=2)
        for e in ext_s:
            if tt < e['start']:
                continue
            if e['kind'] == 'line':
                r = min(1.0, (tt - e['start']) / e['dur'])
                draw_partial(d, e['pts'], r, e['color'], e['width'])
            elif e['kind'] == 'dot':
                d.ellipse([e['pos'][0] - e['r'], e['pos'][1] - e['r'],
                           e['pos'][0] + e['r'], e['pos'][1] + e['r']], fill=e['color'])
            elif e['kind'] == 'blush':
                d.ellipse([e['pos'][0] - e['rx'], e['pos'][1] - e['ry'],
                           e['pos'][0] + e['rx'], e['pos'][1] + e['ry']], fill=e['color'])
        frames.append(frame.convert('P', palette=Image.ADAPTIVE, colors=96))
    gp = os.path.join(OUT, f'live_{mode}.gif')
    frames[0].save(gp, save_all=True, append_images=frames[1:],
                   duration=int(1000 / fps), loop=0, optimize=True, disposal=2)
    print('gif    ->', gp, 'frames=', len(frames),
          'size=', os.path.getsize(gp))


def main():
    global SRC, OUT, MODE, ADD_DECOR
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--mode", default=MODE, choices=["trace", "persona"])
    ap.add_argument("--decor", action="store_true", help="开启装饰性脸/星（非整体衔接，需用户明确选择）")
    ap.add_argument("--extractor", default="canny", choices=["canny", "hsv"],
                    help="persona 模式用 HSV 提主体更稳（亮+低饱和），避开楼宇/天空；trace 模式仍走 canny")
    args = ap.parse_args()
    SRC, OUT, MODE = args.src, args.out, args.mode
    if args.decor:
        ADD_DECOR = True

    img_arr = np.array(Image.open(SRC).convert("RGB"))
    H, W = img_arr.shape[:2]
    print(f"[{MODE}] loaded {SRC}, {W}x{H}")

    contours, _, _ = extract_contours(img_arr)

    if MODE == "trace":
        lines, end_t = build_trace(contours, H, W)
        print(f"trace: {len(lines)} outlines, end_t={end_t:.2f}s")
    else:  # persona
        if args.extractor == "hsv":
            subj, _, _ = extract_subject_hsv(img_arr)
            contours_for_main = subj
        else:
            contours_for_main = contours
        main_c = main_contour_from(contours_for_main, H, W)
        if main_c is None:
            print("!! 未提取到主体轮廓，回退 trace 模式")
            lines, end_t = build_trace(contours, H, W)
        else:
            lines = build_persona(main_c, H, W)
            end_t = build_persona_timeline(lines)
            print(f"persona: 基于真实轮廓长出 {len(lines)} 笔，end_t={end_t:.2f}s "
                  f"(extractor={args.extractor})")

    extras = []
    if ADD_DECOR:
        main_c = main_c if (MODE == "persona") else (max(contours, key=cv2.contourArea) if contours else None)
        extras, _ = build_decor(main_c, W, H, end_t)
        print(f"decor enabled: {len(extras)} extras (非整体衔接点缀)")

    export(lines, extras, img_arr, W, H, OUT, MODE, end_t)
    print("done.")


if __name__ == "__main__":
    main()
