# design-reference-sourcing CHANGELOG

## [1.2.1] - 2026-09-01
- **修正越界兜底（配合 design-workflow 1.6.1）**：用户定调"品味基线只给模式 2，模式 1 只找参考做常规设计"。
- 「一·补充」第 5 步去掉"（与品味基线并列）"；第 6 步兜底改"按常规设计默认值推进（沿用通用反 slop 护栏，但**不调用模式 2 的 taste-profiles 品味基线**——那仅属模式 2）"。
- 版本 1.2.0 → 1.2.1。

## [1.2.0] - 2026-09-01
- **模式 1 默认路径·强制前置**（用户定调）：任何模式 1 任务，brief 定稿后自动触发参考检索，用户无须开口说「找参考」。
- 「一、何时触发」把「模式 1 默认路径·强制」列为首要用途；新增「一·补充 · 模式 1 强制检索流程」六步：提取检索键 → 按键选源 → 省流抓取 2–4 个 → 红点笔记提炼 → 注入 L2 → 检索不到兜底（`UNREFERENCED` + 品味基线，不阻塞流程）。
- description 同步：「9 个策展源」更正为「10 个」；版本 1.1.2 → 1.2.0。

## [1.1.2] - 2026-09-01
- 「二·补充 · 按资源类型分类的设计参考站」表新增 **b2tf.app**（Vintage Mobile App Design Directory）：复古风移动 App 设计目录，按分类（Entertainment / Lifestyle / News / Utilities / Photo & Video / Music…）策展真实 App 截图，免登录可直抓。
- 定位：与 mobbin.com 互补——mobbin 偏"真实产品通用 UI 模式"，b2tf 偏"vintage 美学在移动端的落地"，属移动端审美参考而非工具站，符合「能学到审美规律」筛选标准。
- 表头「精选 4 个 → 5 个」；子技能版本 1.1.1 → 1.1.2。

## [1.1.1] - 2026-09-01
- 开放策展源清单新增 **Codrops Creative Hub**（https://tympanus.net/codrops/hub/）：WebGL / Three.js / GSAP / SVG 的 demos、tutorials、sketches 与 UI 模式（页面过渡 / hover / cursor / grid / slideshow / typography）聚合站，免登录。
- 定位：与 ThreeUI / React Bits 互补，补全「前端动效实现参考 + 交互模式库」线（Codrops 含教程文本与社区 demos，那两个偏可直接复用的组件代码）。
- 抓取手法：feed 为 JS 渲染 → `agent-browser` 截图读 demo 视觉；`WebFetch` 取教程文字与 200+ 标签体系做定向检索。
- 同步更新：技能描述、4 处内联源列表、「9 个 → 10 个」计数；子技能版本 1.1.0 → 1.1.1。
