# 来源署名 · greensock/gsap-skills

- **原始来源**：[greensock/gsap-skills](https://github.com/greensock/gsap-skills) — 官方 GSAP AI 技能集（GreenSock 维护，MIT，LOW 风险）。
- **吸收方式**：去名化为「易错纪律 + 关键 API 骨架」，**不内嵌完整 raw SKILL.md**、不塞工具清单式冗余。具体 API 参数随 GSAP 版本演进，以官方文档当前版本为准。
- **落入位置**：`subskills/design-frontend` 末尾新增「补充 · GSAP 落地参考（库专用 · 仅 GSAP 载体时调用）」段（design-workflow 1.6.6）。**未新建子技能节点**。
- **吸收的 5 个 web/vanilla 核心**（去名化后）：
  - `gsap-core`：camelCase 属性、transform 别名优于 raw transform、autoAlpha 优于 opacity、defaults 收敛节奏、`from`/`fromTo` 的 `immediateRender` 堆叠陷阱。
  - `gsap-timeline`：timeline + 位置参数取代 `delay` 链、labels、`defaults` 继承。
  - `gsap-scrolltrigger`：注册、`scrollTrigger` 配置（trigger/start/end/scrub/pin/toggleActions）、scrub 与 toggleActions 不混用、containerAnimation 必须 `ease:"none"`、`refresh()` 时机、清理。
  - `gsap-plugins`（仅 web/vanilla 相关）：SplitText / CustomEase / Flip / ScrollSmoother / ScrollToPlugin / Draggable+Inertia / MorphSVG+MotionPath 速查。
  - `gsap-performance`：只动 transform/opacity、will-change 仅真动元素、quickTo 高频更新、kill 离屏、matchMedia 处理 reduced-motion。
- **未吸收（红线 / 去重）**：
  - `gsap-react` / `gsap-frameworks`（Vue/Svelte 适配）→ 框架层，不收。
  - `gsap-utils` → 工具函数层，按需查官方，不固化。
  - 全部「安装命令 / marketplace 配置 / 具体库版本号」→ 实现层、会过时，剥离只留原则。
- **与既有资产的边界**：本段是「GSAP 具体写法」，不替代第八节「交互工程对错清单」与「决策门控」、第七/八节「性能与 reduced-motion 降级」、补充段「存量审计 / 组件选型纪律」。GSAP 只是实现手段，不豁免设计纪律。
- **署名**：技能正文不内嵌；图内不署名。
