# image_gen 生图 Prompt 模板（design-workflow 专用）

> 本文件供助手在对话中触发内置 `image_gen` 工具时套用。技能本体定义设计规范，
> 真正执行生图靠 `image_gen`（助手内置能力，非脚本）。模板目标是让生成图
> "符合本技能的视觉基因"，而非匿名通用 AI 图。
>
> 调用参数（助手侧）：
> - prompt：英文画面描述（越具体越好）
> - size：如 1024x1280（竖版 4:5）/ 1024x1024（方）
> - quality：low / medium / high
> - n：张数（默认 1）
> - style：vivid（强风格）/ natural（写实克制）

---

## 一、通用规则（所有生图都遵守）

- 文字必须可读：要求模型"legible Chinese calligraphy, not blurred, not decorative to unreadable"。
- 防 AI 默认观感：禁止 "AI purple, neon gradient, generic flat vector, 3D render cliché"。
- 墨朱调性默认：black ink main + vermilion seal red accent + warm off-white paper background。
- 落款/印章：右下角 small red seal stamp（completion mark）。

---

## 二、图形字 · 填字共生型（物品结构承载文字）

> 适用：啤酒杯 / 鸟 / 树 / 花 / 鱼 / 房屋等具象主体，文字填充进物品内部、少量笔画突破边缘。
> 视觉顺序：item → text → fusion（第一眼先认出物品，再看字长在内部）。

**英文模板（替换 <ITEM> / <TEXT> / <MOOD>）：**
```
A contemporary Chinese ink-painting style illustration where the main subject is a
<ITEM> rendered in bold black brush calligraphy. The body of the <ITEM> is filled
with dense, legible Chinese handwriting text "<TEXT>", the characters flowing along
the item's silhouette and internal structure, a few stroke-ends breaking past the
edge like flying white. Warm off-white paper background, vermilion seal stamp at
bottom-right. Mood: <MOOD>. Ink texture, visible brush pressure, NOT a vector,
NOT neon, NOT 3D cgi.
```

**示例（鸟 + 天天快乐）：**
```
A contemporary Chinese ink-painting style illustration where the main subject is a
bird rendered in bold black brush calligraphy. The body of the bird is filled with
dense, legible Chinese handwriting "天天快乐", the characters flowing along the
bird's wings and body, a few stroke-ends breaking past the edge like flying white.
Warm off-white paper background, vermilion seal stamp at bottom-right. Mood:
lighthearted festive. Ink texture, visible brush pressure, NOT a vector,
NOT neon, NOT 3D cgi.
```

---

## 三、图形字 · 以字寄形（汉字里寄图形）

> 适用：节令物产 / 品牌字 / 单字合字（鸡/茶/福/鱼…）。

**英文模板：**
```
A single large Chinese character "<CHAR>" as the hero visual, drawn in thick
northern-stele calligraphy. A <OBJECT> is fused into the character's strokes
sharing the same black ink — the object's form grows from one of the character's
strokes, not pasted on. 30-60% of the glyph area is the object. Warm off-white
paper, vermilion seal stamp bottom-right. Ink brush texture, NOT vector, NOT neon.
```

---

## 五、常用主体 prompt 片段（一键组合）

| 主体 | 英文片段 |
|---|---|
| 鸟 bird | a bird rendered in bold black brush calligraphy |
| 树 tree | a tree whose trunk and canopy are brush strokes |
| 鱼 fish | a fish with ink-brush fins and body |
| 杯 cup | a beer cup, foam as flying-white, body filled with text |
| 花 flower | a bloom whose petals are calligraphy strokes |

组合方式：填字共生型选「主体片段 + 填字模板」；以字寄形型选第三节模板。图形字技能不绑定任何具体 IP，主体片段仅作中性物象示例。
