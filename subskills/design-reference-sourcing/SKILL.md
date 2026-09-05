---
name: design-reference-sourcing
description: 联网找素材做参考专项。**模式 1 默认路径的强制前置步骤**——用户输入任务 brief 后自动触发，去参考站找「对应的设计」作本次设计依据；用户主动说「找参考/找灵感/找配色/找音效/看看别人怎么做/搜一下案例」时同样触发。覆盖：12 个策展源（Pinterest 与爱给网需登录；Cosmos/ArtStation/Behance/Unicorn Studio/Refero Design/Awwwards/ThreeUI/React Bits/Spline Community/Codrops Creative Hub 开放可直抓）、**agent-browser CLI 截图读图（复用 Chrome 登录态，首选用于登录源与 JS 渲染画廊）**、开放源直抓与登录源带会话抓取的两种手法、合规红线（仅作参考不擅发、版权与署名）。接入设计工作流第二层「感知物料」，作为真实素材补给线。
version: 1.2.2
---

# design-reference-sourcing ｜ 联网找素材做参考

> 本子技能是 design-workflow 的**第二层「感知物料」的前置补给线**——动手设计前，先把真实世界的参考素材（色板 / 字体 / 构图 / 3D / 动效 / 音效）喂进 L2，避免凭空想象或套 AI 默认观感。
> 参考用来**校准审美与事实**，不是用来抄。所有抓取素材仅作内部参考 / 灵感，不擅自再发布第三方资产。

## 核心信条

1. **参考 = 校准，不是复制**。抓回来的图 / 音 / 模型只用于提炼规律（配色逻辑、构图节奏、动效语义），不能直接挪用为产出元素。
2. **开放源直抓，登录源带会话抓**。先看本清单判定登录要求，再选手法。
3. **合规红线优先于便捷**。版权素材复用需授权与署名；音效商用按平台 license。

## 〇、抓取手法优先级（重要 · 先读）

> 本环境已安装 **agent-browser 0.27.0**（CLI），通过 Agent 的 `execute_command` 直接调用，**无需 MCP 配置、每次对话默认可用**。它支持 `open` / `screenshot` / `snapshot` / `--profile Default`（复用本机 Chrome 登录态），是处理「JS 渲染画廊」与「登录源」的最佳手段。

**默认顺序**：

1. **首选：Agent 自带 `WebFetch` + `WebSearch`**（零配置、最稳，取文字/链接/结构）
   - 开放源（Cosmos / ArtStation / Behance / Unicorn Studio / ThreeUI / React Bits / Spline Community / Codrops Creative Hub）直接用 `WebFetch` 抓页面、`WebSearch` 补定向检索，已实测可用。
2. **次选：agent-browser 截图读图**（取**视觉内容**，这是 WebFetch 做不到的）
   - 目标页是 **JS 渲染的纯图片画廊**（`WebFetch` 拿不到图）→ `agent-browser open <url> && agent-browser screenshot <path>` → 用 `read_file` 读图提炼风格。
   - 需进入**登录源**（Pinterest / 爱给网等）→ 加 `--profile Default` 复用本机 Chrome 登录态，**免 cookie 注入**（`agent-browser --profile Default open <url>`）。
   - 调用方式：`execute_command` 跑 `agent-browser ...`（它是 CLI，不在 MCP 列表，走命令行即可）。
3. **cookie 注入仅作最后手段**：仅当 agent-browser 不可用且用户已主动提供会话 cookie 时，才走下方「Pinterest / 爱给网 cookie 实操记录」。密码一律不碰。

> **一句话**：先 `WebFetch`/`WebSearch` 直搜；要"看"到图或要进登录站，用 `execute_command` 调 `agent-browser --profile Default` 截图；cookie 注入是兜底里的兜底。

> **环境事实（写死）**：agent-browser 0.27.0 已安装，通过 `execute_command` 调用；`--profile Default` 可复用用户 Chrome 登录态，使 Pinterest / 爱给网等登录源可直接抓取（旧 cookie 注入记录见第六节，已降级为兜底）。

## 一、何时触发

- **模式 1 默认路径·强制（本子技能的首要用途）**：任何模式 1 任务，第 1 层 brief 定稿后、进第 2 层前，**自动触发一次参考检索，不许跳过**——按 brief 的载体 + 风格方向去参考站找「对应的设计」作本次设计的依据，抓回后提炼约束注入 L2。用户不需要开口说「找参考」。
- 用户主动说「找参考 / 找灵感 / 找配色 / 找字体参考 / 找音效 / 找 3D 参考 / 看看别人怎么做 / 搜一下案例」
- L2 感知物料阶段，需要真实素材锚定色板 / 字体 / 构图 / 动效 / 音效时
- 吸睛模式（模式 2）/ AI 自主（模式 3）探索前沿方向、需要跨界案例时

## 一·补充 ｜ 模式 1 强制检索流程（brief → 检索 → 提炼 → 注入）

> 这是模式 1 的**默认前置步骤**，与用户主动找参考无关——brief 定稿即执行。完整六步：

1. **提取检索键**：从第 1 层 brief 里取 ① 载体（App 界面 / 海报 / 长页…）② 风格方向（暗调编辑 / 复古 / 极简…）③ 2–3 个内容关键词。
2. **按键选源**：载体是移动 App → 优先 mobbin / b2tf；设计规格 / DESIGN.md 写法范例 → Refero Styles；网页动效 / 交互前沿 → Awwwards / Codrops / Unicorn Studio / ThreeUI / React Bits；平面海报 → Behance / Cosmos / curations.supply；品牌 → rebrand.gallery；不确定就按「二、策展源清单」开放源优先。
3. **抓取（省流）**：开放源 `WebFetch` + `WebSearch` 定向检索；要"看"到图 → `agent-browser` 截图（见第七节）。单次检索抓 **2–4 个高匹配参考**即可，不必铺开全站。
4. **提炼（红点笔记协议，必做）**：每张参考写 3 行（好在哪 / 什么机制让它美 / 可复用到哪），拆出**可复用规律**而非形容词——参考是用来校准审美的，不是拿来抄的。
5. **注入 L2**：色板 → `颜色.md`；字体/排版 → `文字.md`；构图节奏 → `排版构图.md`；动效语义 → `动画.md`。注入后作为第 2–5 层的硬性约束，不是可选项。
6. **兜底（检索不到不许卡流程）**：网络受限 / 无匹配 → 声明 `UNREFERENCED`，按常规设计默认值推进（沿用通用反 slop 护栏，但**不调用模式 2 的 taste-profiles 品味基线**——那仅属模式 2）。继续流程。宁可明说没参考，也不能假装参考过。

## 二、策展源清单（12 个，按登录要求分两类）

### 开放类（无需登录，可直接抓取）

| 源 | URL | 素材类型 | 抓取要点 |
|---|---|---|---|
| **Cosmos.so** | https://www.cosmos.so/ | 视觉灵感 / 按颜色·视觉相似度搜图 | 落地页可读；用 WebFetch 搜关键词或颜色，提取图源、艺术家与来源故事（其卖点即「surface artist/source/story」） |
| **ArtStation（VR/AR 频道）** | https://www.artstation.com/channels/virtual_and_augmented_reality | 3D / 概念艺术 / VR·AR | 可浏览；WebFetch 解析偏弱，必要时用 agent-browser 截图提取风格关键词 |
| **Behance** | https://www.behance.net/ | 全品类设计项目（平面 / 动效 / 品牌） | 可浏览；bot 易受阻，换 WebSearch 或 agent-browser 兜底 |
| **Unicorn Studio（Inspiration）** | https://www.unicorn.studio/inspiration | 网页 / 交互动效灵感 | 落地页可读；提取动效关键词、实现思路与交互范式 |
| **ThreeUI（Browse）** | https://threeui.com/browse | Three.js 组件 / WebGL 背景 / hero 动效 / 交互 shader | 公开画廊、免登录可浏览；页面 JS 渲染，实际组件列表用 agent-browser 截图提取动效与实现思路；下载源码可能需账号 |
| **React Bits** | https://reactbits.dev | React 动画 / 交互组件（开源、可复制使用） | 开源 React 组件库（David Haz / GitHub `DavidHDev/react-bits`）；落地页可读，`WebFetch` 取组件分类与效果说明，或直接看 GitHub 仓库拿代码。作「前端动效实现参考」+ UI 动效灵感；与 `design-frontend` 子技能互补（本源给真实组件，子技能给动效语义原则） |
| **Spline Community** | https://app.spline.design/community | 3D 场景 / 交互 3D 设计（#MadeInSpline） | 公开社区画廊、免登录可浏览（页有 Login/Sign Up 但内容开放）；`WebFetch` 可取 Trending/Popular/New 与分类，提取 3D 场景的构图 / 光影 / 交互范式；下载 `.spline` 源文件需账号 |
| **Codrops Creative Hub** | https://tympanus.net/codrops/hub/ | WebGL / Three.js / GSAP / SVG 演示·教程·草图 + UI 模式（页面过渡 / hover / cursor / grid / slideshow / typography） | 开放站、免登录；feed 为 JS 渲染，用 `agent-browser` 截图读 demo 视觉；`WebFetch` 取教程文字与 200+ 标签体系（WebGL/GSAP/Three.js/scroll/hover/cursor/page transition…）做定向检索；偏「前端动效实现参考 + 交互模式库」，与 ThreeUI / React Bits 互补（本源含教程文本与社区 demos，那两个偏可直接复用的组件代码） |
| **Refero Styles** | https://styles.refero.design/ | DESIGN.md 示例库（面向 AI 设计 Agent 的「设计规格 / 设计系统」写法范例） | 开放站、免登录（`WebFetch` 已验证可读）；**可直接抓取真实 DESIGN.md 范例来"读设计规范"**——当用户要产出 DESIGN.md / 机器可读设计规格 / 开发交接文档，或 L1 brief 要按"规格写法"结构化时，来这里取范式；与 mobbin / Behance 等「视觉素材」源定位不同——偏"设计表达格式 / 规格约定"而非"视觉参考" |
| **Awwwards（Sites of the Day）** | https://www.awwwards.com/websites/sites_of_the_day/ | 网页设计每日精选 / 创意站点 / 交互与动效前沿 | 开放浏览、免登录；feed 为 JS 渲染，`WebFetch` 取获奖信息与文字偏弱，用 `agent-browser` 截图读视觉（见第七节）；偏"网页创意与交互前沿成品鉴赏"，与 Codrops / Unicorn Studio 互补（Awwwards 偏成品站点审美标杆，那两个偏实现/组件） |

### 登录类（需账号，先手动登录再抓）

| 源 | URL | 素材类型 | 登录说明 |
|---|---|---|---|
| **Pinterest** | https://www.pinterest.com/ | 图片 / moodboard | 实质需登录，强反爬，未登录几乎不可抓。用户提供**会话 cookie（非密码）** → 由 Agent 注入抓取（见下方「Pinterest cookie 实操记录」） |
| **爱给网 aigei.com（角色音效）** | https://www.aigei.com/sound/class/role | 角色 / 音效素材 | 明确拦截未登录（实测返回「需先登录后才能继续浏览」）。✅ 2026-08-25 已验证：用户导出 cookie → Agent 注入后**登录态生效**（右上「登录」变为账号名），不绑 IP。 |

> **登录态保存说明**：本子技能**不存储密码**。对于登录类源，标准做法是——
> 1. 用户本人在浏览器完成登录；
> 2. 由用户主动提供**会话 token / cookie 字符串**（非账号密码），Agent 用 agent-browser 注入后抓取；
> 3. 或在 agent-browser 会话中由用户当面输入凭据（Agent 不记录）。
> 任何情况下都不得要求或缓存明文密码。

## 二·补充 · 按资源类型分类的设计参考站（精选 5 个）

> 与「二、策展源清单」互补——策展源按**平台 / 抓取方法**组织（批量抓图入 `taste-profiles`），本表按**资源类型**速查。
> **筛选标准：只收"能学到审美规律"的参考站；素材 / 工具 / 模板 / 推广站不收**（2026-08-31 精简：原 10 站中 6 个工具/推广站已删——landing.love / saaspo / sleek.design / uncut.wtf / hugeicons 及待补的 Design Systems）。

| 资源类型 | 站 | 参考价值 |
|---|---|---|
| Design Library（策展） | curations.supply | 精选过的素材合集——看"策展人怎么选"，长审美 |
| Animation（动效） | 60fps.design | 动效 / 交互参考（对应 `动画.md` 领域） |
| Mobile Apps（移动模式·通用） | mobbin.com | 移动 App UI 模式库——学"真实产品的信息架构" |
| Mobile Apps（移动模式·复古向） | b2tf.app | Vintage Mobile App Design Directory——按分类策展的复古风移动 App 设计目录，学"vintage 美学在移动端的落地"（与 mobbin 互补：mobbin 偏真实产品通用模式，b2tf 偏复古审美策展） |
| Brands（品牌案例） | rebrand.gallery | 品牌重塑 / 视觉系统案例——学"识别系统怎么变" |

> 使用：想"找灵感看作品"走本表；想"批量抓图入 taste-profiles"走策展源清单。两者互补。

### Pinterest cookie 实操记录（2026-08-25 验证）

- **导出方式**：用户在本人浏览器用 Cookie-Editor 等插件导出 Pinterest 全站 cookie（JSON 数组，含 `_pinterest_sess` / `_auth` / `csrftoken` 等）。
- **存放位置**：`D:\shujuchucun\yundong\图片\.workbuddy\browser-sessions\pinterest.cookies.json`（**不进技能目录、不被同步/提交**）。
- **注入手法**：agent-browser 的 `cookies set --curl <file>` 对 Cookie-Editor 格式报 `Invalid cookie fields`（多 `storeId`/`hostOnly`/`expirationDate`/`sameSite:null` 等非 CDP 合法字段）。已改用**逐条 `cookies set <name> <value> --domain --path [--httpOnly] [--secure] [--sameSite <Lax|None>] [--expires <秒>]`**，由 Python 子进程传参避免 shell 转义破坏值里的 `= / + " `。辅助脚本：`browser-sessions/_inject_cookies.py`。
- **注入顺序关键点**：必须先 `open https://www.pinterest.com/`（让 Pinterest 发一个空会话），**再注入 cookie 覆盖**，然后 reload——若先注入再 open，导航响应里的 `Set-Cookie` 会把注入的会话冲掉。
- **⚠️ 已验证结论**：注入本身成功（注入后未导航时 `_pinterest_sess` 为原始 1840 字符长值、`_auth=1`）。但**沙箱浏览器一导航到 pinterest.com，Pinterest 就拒绝该会话并重新签发空会话**（`_auth` 回到 `0`）。这是 Pinterest 的反爬 / 会话-IP 绑定在拦自动化浏览器，**非 cookie 错误或写入失败**。外网直连 Pinterest 可能同样受此限制。
- **因此 Pinterest 的可用路径**（按优先级）：
  1. **首选 agent-browser `--profile Default` 复用本机 Chrome 登录态截图**（见第七节，2026-08-28 验证可用，免 cookie 注入）；
  2. 优先用 10 个开放源（Cosmos / ArtStation / Behance / Unicorn Studio / Refero Styles / Awwwards / ThreeUI / React Bits / Spline Community / Codrops Creative Hub）做参考；
  3. 或请用户在**本人已登录的浏览器**里搜好、把图链 / 截图给我，我再做提炼；
  4. 爱给网（aigei.com）反爬较松，cookie 注入**历史已验证可行**（见下方记录），但现同样优先走 agent-browser。

### 爱给网 cookie 实操记录（2026-08-25 验证 ✅ 可行）

- **导出方式**：用户在本人浏览器用 Cookie-Editor 导出 aigei.com 全站 cookie（JSON 数组，共 8 条，关键为 `SESSION` / `gei_d_1` / `gei_d_u`）。
- **存放位置**：`D:\shujuchucun\yundong\图片\.workbuddy\browser-sessions\aigei.cookies.json`（不进技能目录、不被同步/提交）。
- **注入手法**：与 Pinterest 同源问题——`cookies set --curl` 对 Cookie-Editor 格式报 `Invalid cookie fields`。改逐条 `cookies set <name> <value> --domain --path [--httpOnly] [--secure] [--sameSite] [--expires]`（辅助脚本 `browser-sessions/_inject_aigei_cookies.py`，Python 子进程传参避免 shell 转义破坏值，且 `capture_output=True` 后用 `errors="replace"` 解码，因 agent-browser 输出含 Windows CP936 非 UTF-8 字节会触发解码崩溃）。
- **注入顺序**：`open` 先打开页面（让 aigei 发一个基础会话）→ 注入 cookie 覆盖 → 再 `open` 同 URL 重载。若先注入再 open，导航的 `Set-Cookie` 会冲掉注入会话。
- **注入结果**：8 条中 7 条成功；唯一失败的是 `SERVERID`（hostOnly + session、值含 `|`），但它是负载均衡粘性 cookie，aigei 每次响应会自动重发，**缺失无害**。登录态关键 cookie `SESSION` 注入成功。
- **✅ 验证结论（与 Pinterest 的关键差异）**：重载后页面右上角「登录」链接被替换为账号名 `link "街鹿"`（即已登录态）；`cookies get` 复核 `SESSION=6eba683d-185a-4c38-9404-f9dbc9feca1c` 与用户提供值**完全一致、未被重签为空**。证明 **aigei.com 接受沙箱/自动化浏览器注入的会话，不绑定 IP**（Pinterest 反之）。
- **注意**：首次未登录 `open` aigei 时会被短暂重定向到 `https://www.aigei.com/gei-common/pageComp/banIp/route` 的 banIp 拦截页，重载后正常进入；注入登录态后不再出现该拦截。
- **因此 aigei.com 的可用路径**：直接走「用户导出 cookie → Agent 注入 → 在已登录会话里导航/截图/提取」全流程，无需用户当面操作。



**开放源（Cosmos / ArtStation / Behance / Unicorn Studio / Refero Styles / Awwwards / ThreeUI / React Bits / Spline Community / Codrops Creative Hub）**
1. `WebFetch` 取页面文本 / 图片链接 / 署名 → 提炼色板、字体、构图、动效关键词。
2. `WebSearch` 补充「site:behance.net <主题>」等定向检索。
3. 当 WebFetch 解析失败（bot 阻挡 / JS 渲染）→ `agent-browser` 打开页面截图，再读图提取。

**登录源（Pinterest / 爱给网）**
1. `agent-browser` 打开登录页。
2. 用户自行完成登录（当面输入，或 Agent 注入用户提供的会话 cookie）。
3. 登录态保持后导航到目标板块 / 搜索词 → 截图或提取。
4. 抓取结果仅作内部参考；如需把其中素材作为产出元素，必须取得授权。

## 四、合规红线（必须）

- **仅作内部参考 / 灵感**，不擅自再发布第三方图 / 音 / 模型资产。
- Pinterest / Behance / ArtStation 图片均受版权保护，复用需授权与署名。
- 音效（爱给网）商用需按平台 license，留意「免费 / 会员 / 商用」分级。
- 提取到的「艺术家 / 来源 / 署名」如要写入最终产出，按用户既定的「来源署名分文件管理」约定处理——技能正文不内嵌裸 byline，图内绝不署名。

## 五、与五层流程的接驳

抓回的素材按类型落入 L2 各子位置：
- 色板 → `modules/02-感知物料/颜色.md`
- 字体 / 排版 → `modules/02-感知物料/文字.md`
- 构图节奏 → `modules/03-形式组织/排版构图.md`
- 动效语义 → `modules/02-感知物料/动画.md`
- 音效（如载体含声音）→ 存档备用，注明授权状态

L5 主观输出验收时回看：参考是否**真的校准了审美**，而非把产出带偏成「又一个模板」。

## 六、自检清单

- [ ] 已先判定目标源属于「开放」还是「登录」类？
- [ ] 登录类是否走了用户会话（而非索要密码）？
- [ ] 抓回素材是否只作参考、未直接挪用为产出元素？
- [ ] 如需复用，是否已确认授权与署名方式？
- [ ] 提炼出的色板 / 字体 / 动效规律是否落到 L2 对应子位置？

## 七、agent-browser 实操（2026-08-28 验证可用）

> 本环境 agent-browser 0.27.0 已安装，是 **CLI 程序**，Agent 通过 `execute_command` 调用（不在 MCP 列表，无需配置）。核心能力：`open` / `screenshot [path]` / `snapshot`（accessibility tree）/ `--profile <name>`（复用 Chrome 登录态）/ `--session-name`（自动存 cookie+localStorage）。

### 常用命令模板

```bash
# 1. 开放源：打开 + 截图（截图后用 read_file 读图提炼）
agent-browser open "https://www.behance.net/..." && agent-browser screenshot "references/reference-images/behance-001.png"

# 2. 登录源：复用本机 Chrome 登录态（Pinterest / 爱给网等，免 cookie 注入）
agent-browser --profile Default open "https://www.pinterest.com/..." && agent-browser screenshot "references/reference-images/pin-001.png"

# 3. 取文本化页面结构（不需要看图、只要链接/层级时）
agent-browser open "<url>" && agent-browser snapshot -i

# 4. 全页长截图
agent-browser open "<url>" && agent-browser screenshot --full "references/reference-images/full.png"

# 5. 移动端视口（验证手机版设计时）
agent-browser --viewport "390,844" open "<url>" && agent-browser screenshot "references/reference-images/mobile.png"
```

### 关键结论（与旧 cookie 记录的关系）
- **旧记录**（第六节下方 Pinterest / 爱给网 cookie 注入）是基于"无 agent-browser 或不可调用"前提的兜底。**现在 agent-browser 可用 + `--profile Default` 能复用登录态，Pinterest / 爱给网应优先走 agent-browser，不再需要手工导出/注入 cookie。**
- 旧 cookie 记录保留作为"agent-browser 不可用时的最后手段"，但标记为降级路径。
- 截图产出统一存 `references/reference-images/`（已建目录），并在 `design-taste` 的 taste-profiles `references` 字段里登记，使后续设计有真图可对标。

### 截图后如何提炼：红点笔记协议（接驳 L2，必做）

> 看过不等于吸收。每抓回一张参考，**必须**为它写一张"红点笔记"（3 行），否则参考不会沉淀为审美资产：

1. **好在哪**：一句话说清这张图最打动人的地方（"这个灰调里的一枚橙点"）。
2. **什么机制让它美**：拆出可复用的机制，而非形容词（"大面积灰调 + 单一高饱和强调色 → 安静的尖叫点"）。
3. **可复用到哪**：落到自己的哪个场景 / 手法（"可作 X 海报的撞色方案"）。

- 红点笔记按素材类型沉淀：
  - 色板 / 字体 / 构图规律 → 写进 `modules/02-感知物料/` 对应子位置（颜色 / 文字 / 动画）；
  - 属于某 taste profile 的参考 → 登记进 `subskills/design-taste/taste-profiles/<profile>.md` 的 `references` 字段（补真实图路径）与新增 `notes` 字段（红点笔记）；
  - 可复用的"造美手法" → 归入 `references/惊艳手法库.md`。
- 设计产出时回看这些真参考与红点笔记，避免"凭空想象 / 套 AI 默认观感"。
