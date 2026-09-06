# 来源署名 · Jakubantalik/transitions.dev

## 来源
- 仓库：[github.com/Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev)
- 作者：Jakub Antalik
- 授权：开源（站点与 agent skill 免费，Pro 扩展需登录；本吸收仅取免费通用方法论，未引入任何 Pro/付费内容）
- 性质：可复制粘贴的 UI 组件级 CSS 过渡片段库 + 安装式 agent skill + Refine 实时精调工具

## 本次吸收（design-workflow 1.6.7 · 收进 subskills/design-frontend · 不新建节点）
将其中**通用方法论**去名化后并入 `subskills/design-frontend`「补充 · 组件过渡选型参考（CSS 落地）」段，位于 GSAP 段之前，使动画层阅读顺序为：emilkowalski 决策 → transitions.dev 选型 → gsap 实现。

吸收的 3 层方法论：
1. **匹配纪律**：先匹配可见 UI 元素 → 再匹配动词 → 平局按开销取舍（`card resize` > `panel reveal`、`dropdown` > `modal`、`success check` > 整模态庆祝）；无清晰匹配回退让人选；`success check` 为纯动画须配 `icon swap` 组合。
2. **命名词汇表**：把常见交互的动效命名规范化（card resize / number pop-in / notification badge / text states swap / menu dropdown / modal / panel reveal / page side-by-side / icon swap / success check / avatar group hover / error state shake / input clear with dissolve / skeleton loader and reveal / shimmer text / tabs sliding / tooltip / texts reveal 等）。
3. **Motion Tokens 节奏体系**：共享语义化 timing token（durations / easings / distances / scales / blur）；按"用途"而非"原始数值"映射；强制 `prefers-reduced-motion` 守卫；低开销优先 + 最小 diff；禁 `transition: all`。

## 未吸收（红线 / 剥离项）
- 具体每个过渡的 **CSS 片段源码**（copy-paste 资产，随源站演进、会过时）。
- 按组件覆盖的 **私有变量**（如 `--resize-dur`、`--badge-*` 等逐过渡微调值）。
- **Refine 工具**与 **transitions-pro CLI**（运行时工具，非方法论）。
- **Pro 过渡**（confetti-burst 等，付费内容）。
- 安装命令 / marketplace 配置 / 具体版本号（实现层）。

## 与既有资产的分工
- `emilkowalski/skills`：管"该不该动 / 做对没有"（通用动效纪律）。
- 本来源：管"选哪个过渡 / 命名词汇 / 节奏 token"（组件级 CSS 过渡选型）。
- `greensock/gsap-skills`：管"用 JS 库怎么写"（GSAP 实现落地）。
- 三者皆须先过 design-frontend 第八节通用纪律；本来源与 gsap 段均不豁免设计纪律。

## IP 处理
- 全去名化、文档内署名（本文件）；图内不署名。
- 未引入 Pro 付费内容与私有 IP。
- 具体 API/片段参数随源站版本演进，以官方当前版本为准。
