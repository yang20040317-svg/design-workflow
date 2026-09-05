---
name: design-motion-vocabulary
description: 动效术语反查词典——把对 web 动效/效果的模糊描述翻成确切术语（「popover 打开时那弹一下」→ Pop in；「iOS 拉过头的回弹」→ Rubber-banding）。当用户问「这叫什么」或描述一个不知名的动效想找对词去 prompt AI/设计师时用。命名而非设计/构建。
agent_created: true
version: 1.0.0
---

# 动效词汇（Motion Vocabulary）

> 来源：Emil Kowalski `animation-vocabulary`。把 web 动效的模糊描述翻成精确术语，让用户知道该要什么。

## 快速开始

用户松散描述一个效果。你以如下格式返回匹配术语：

```
**Stagger** — Animate several items one after another with a small delay between each, creating a cascade.
```

若多个术语都沾边，列最佳匹配在前，再给 1–2 备选并一句话说明差异。

## 准则

1. **读意图非关键词**。用户描述的是他们*看到/感到*的（「springy」「滑掉」「自己画出来」），非技术名。把感觉映射到下方词典。
2. **逐字引词典**。其描述是权威——照用，勿转述。
3. **消歧近义术语**。两词竞争时（*Clip-path* vs *Mask*、*Pop in* vs *Bounce*、*Shared element transition* vs *Layout animation*），对比让用户能选。
4. **无精确匹配时**，给最近术语并明说这是近似，或用词典词汇描述效果（如「那是 *scale-in* 进场的 *stagger*」）。
5. **留在词典内**。术语真不在这，明说而非生造——但可用这些词解释概念。
6. **保持紧凑**。命名问题要的是名，不是散文。以术语起头；仅当被问才展开。

## 示例

**例 1 — 基于感觉**
用户：「popover 好像从你点的按钮里长出来，不是从中间？」
输出：
```
**Origin-aware animation** — An element animates out of its trigger, like a popover growing from the button that opened it instead of from its own center which is the default in CSS.
```

**例 2 — 消歧**
用户：「一张图变成另一张图那个。」
输出：
```
**Morph** — One shape smoothly turns into another shape, e.g. Dynamic Island.
Close alternates:
- **Crossfade** — if they simply fade over each other in the same spot.
- **Shared element transition** — if an element travels and transforms from one position into another.
```

**例 3 — 物理感**
用户：「iOS 那个拉过头抵抗然后弹回。」
输出：
```
**Rubber-banding** — Resistance and snap-back when you drag past a boundary (the iOS overscroll feel).
```

## 词典

### 进与出 — 元素如何出现/消失
- **Fade in / Fade out** — 改变 opacity 出现/消失。
- **Slide in** — 从屏外（左/右/上/下）滑入。
- **Scale in** — 从小长到大出现，常配 fade。
- **Pop in** — 带轻微过冲出现，像弹进位置。
- **Reveal** — 常动 clip-path/mask 逐渐显露内容。
- **Enter / Exit** — 元素加进/移出屏幕时的动画。

### 时序与编排 — 协调多元素/时刻
- **Keyframes** — 动画定义点（0%/50%/100%），浏览器填中间。
- **Interpolation / Tween** — 起止值间生成所有中间帧。
- **Stagger** — 多个元素逐个、小延迟错开，成级联。
- **Orchestration** — 刻意定时多动画，使其像一个协调运动。
- **Delay / Duration / Fill mode / Stepped animation** — 起始延迟 / 时长 / 首末帧保留 / 离散步进（如倒计时）。

### 位移与变换
- **Translate / Scale / Rotate / Skew** — 平移 / 缩放 / 旋转 / 斜切。
- **3D tilt / Flip** — rotateX/Y 加 3D 深度。
- **Perspective** — 3D 强度，值小放大景深。
- **Transform origin** — scale/rotate 生长的锚点。
- **Origin-aware animation** — 元素从触发源长出来，而非自身中心（CSS 默认）。

### 状态间过渡
- **Crossfade** — 一个淡出同时另一个淡入，同处。
- **Continuity transition** — 用视觉连接前后、保持用户方位（如同一矩形变大变小）。
- **Morph** — 一形状平滑变另一形状（Dynamic Island）。
- **Shared element transition** — 元素从一位置旅行并变形到另一位置（缩略图扩成卡）。
- **Layout animation** — 元素尺寸/位置变了，动到新位而非瞬移。
- **Accordion / Collapse** — 段平滑展开/收起高度。
- **Direction-aware transition** — 前进往一个方向、后退往反方向，导航有方向感。

### 滚动
- **Scroll reveal** — 入视口时淡/滑入。
- **Scroll-driven animation** — 进度直接绑滚动位置。
- **Parallax** — 背景前景不同速，造深度。
- **Page transition / View transition** — 页间 / 浏览器在两个状态页间变形、连共享元素。

### 反馈与交互
- **Hover effect / Press-Tap feedback / Hold to confirm / Drag / Drag to reorder / Swipe to dismiss / Rubber-banding / Shake-Wiggle / Ripple** — 悬停 / 点按微缩 / 按住填充确认 / 抓取拖 / 拖重排 / 滑走关 / 越界抵抗回弹 / 错抖 / 点按涟漪。

### 缓动
- **Easing / Ease-out / Ease-in / Ease-in-out / Linear / Cubic-bezier / Asymmetric easing** — 速率变化 / 快起慢收（UI 默认）/ 慢起快收（避用）/ 慢快快慢慢（屏上移动）/ 匀速（仅 spinner/跑马灯）/ 自定义曲线 / 非对称加速减速。

### 弹簧
- **Spring / Stiffness-Tension / Damping / Mass / Bounce / Perceptual duration / Momentum / Velocity / Interruptible animation** — 物理驱动 / 拉力强度 / 沉降速度 / 重量感 / 过冲 / 感知完成 / 惯性 / 速度 / 可中段重定向。

### 循环与环境动效
- **Marquee / Loop / Alternate(yoyo) / Orbit / Pulse / Float / Idle animation** — 连续滚 / 重复 / 往返 / 环绕 / 轻呼吸 / 轻浮漂 / 闲置微动。

### 打磨与效果
- **Blur / Clip-path / Mask / Before-after slider / Line drawing / Text morph / Skeleton-Shimmer / Number ticker / Tabular numbers / Typewriter** — 模糊软瑕疵 / 形状裁剪 / 软边遮 / 对比滑杆 / SVG 自绘 / 字符动画 / 骨架微光 / 数字滚动 / 等宽数字 / 打字机。

### 性能
- **Frame rate(FPS) / Jank / Dropped frame / Compositing / will-change / Layout thrashing** — 帧率 / 卡顿 / 掉帧 / 合成层 / 预提升提示 / 动 layout 属性致每帧重算。

### 应知原则
- **Purposeful animation** — 服务于功能，非纯装饰。
- **Anticipation / Follow-through / Squash & stretch** — 预备微动 / 主体停后余部续沉 / 形变传重量速度。
- **Perceived performance** — 对的动画让界面感觉更快。
- **Frequency of use** — 越常看，越短越微。
- **Spatial consistency** — 跨状态保持身份与位置，用户永不迷失去向。
- **Hardware acceleration** — 动 transform/opacity 让 GPU 保流畅。
- **Reduced motion** — 尊重 `prefers-reduced-motion`，调低或去动效。
