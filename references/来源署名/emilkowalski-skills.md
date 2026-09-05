# 来源署名 · emilkowalski/skills

- **来源**：emilkowalski/skills（GitHub 仓库）
- **类型**：AI Agent 技能集（动效 / 设计工程经验外化，12 个 SKILL.md）
- **作者**：Emil Kowalski（Vercel / Linear 前设计工程师）
- **协议**：MIT（免费可用、可改、可商用）
- **仓库**：https://github.com/emilkowalski/skills
- **吸收日期**：2026-08-31

## 吸收了什么（通用原理，去名化后并入 `design-frontend` 第八节）

- **动画"对错清单"**：`transition: all` 禁止 / `scale(0)` 进场禁止 / `ease-in` 入场禁止 / `transform-origin` 锚定触发器 / 键盘操作不动效 / hover 媒体查询门控 / 高频元素用 transition 不用 keyframes / Enter–Exit 不对称。
- **参数表**：三条自定义 easing 曲线（ease-out / ease-in-out / ease-drawer）、UI 时长表（≤300ms 硬上限）、spring 配置、按钮按压 `scale(0.97)`、stagger 30–80ms、blur ≤20px。
- **Review 三列格式**：`Before | After | Why`。
- **频率–动效决策原则**：用户高频看到的操作不动效（100+/天→不加；数十次/天→缩减；偶尔→标准；罕见→可玩）。

## 需剔除 / 边界（用户指定）

- **不吸收**其"克制 / 多数动画不该做"的宣传性语义——与主技能「默认预算 + 破格触发器」哲学按需取舍；「键盘不动效」等具体正确性保留。
- **适用边界**：仅功能型产品 UI / APP 交互组件（写程序 / 做 APP）；**设计感网页 / 海报 / 品牌页 / 叙事长页不套用**（走主技能 `动画.md` 与 `惊艳手法库`）。
- 技能正文不内嵌作者署名 / 仓库名；图内不署名。

## 其他

- 未吸收：write-swift / ask-sonner / pick-ui-library / prototype / animate-expo 等工具类 skill（与 design-workflow 领域无关或属实现层细节）。
- 动画词汇表（animation-vocabulary）暂未并入（待评估精简版）。
