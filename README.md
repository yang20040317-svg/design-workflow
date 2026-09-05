# design-workflow

通用设计工作流技能（WorkBuddy / Claude Code Skill 格式）——一个**操作型工作流**，不是分析框架。

## 五层顺序执行模型

```
第 1 步  第一层 场景       → 先把前提与边界定清楚
   ↓ 做完才进下一步
第 2 步  第二层 感知物料   → 准备要用的原材料
   ↓
第 3 步  第三层 形式组织   → 把材料排成结构
   ↓
第 4 步  第四层 信息叙事   → 让结构承载意义
   ↓
第 5 步  第五层 主观输出   → 验收受众最终体验
```

各层为**独立可编辑模块**（场景层合并为单文件，其余层按子位置分文件），见 [`modules/`](modules/)。

## 三种调用模式

| 模式 | 一句话定位 | 何时用 |
|---|---|---|
| 1 领域适配 | 按载体门控，稳健落地 | 绝大多数常规设计任务（默认） |
| 2 吸睛 | 抓眼球 / 强传播，借独特品味 | 传播 / 营销 / 社媒 / 需要强记忆点 |
| 3 AI 自主 | AI 主导，探索前沿方向 | 探索性 / 实验性任务 |

## 子技能（subskills/）

按载体 / 任务特征路由的专项方法论：

- **design-chart** — 数据可视化图表专项
- **design-frontend** — 前端 / 数字产品设计原则
- **design-icon-batch** — 图标 / 图形符号批量生产
- **design-ip-assets** — 专属视觉资产体系（IP 化本体）
- **design-metaphor-narrative** — 隐喻统摄的叙事型长页
- **design-mobile-app** — 移动端 App 界面 / 原型
- **design-motion-vocabulary** — 动效术语反查词典
- **design-photo-sketch** — 照片为底 + 手绘线稿叠加
- **design-prototype-divergence** — 原型发散（多变体探索）
- **design-reference-sourcing** — 联网找素材做参考
- **design-taste** — 独特品味档案容器（模式 2 本体）
- **design-typographic-glyph** — 图形字 / 合字设计

## 目录结构

```
design-workflow/
├── SKILL.md            # 主工作流入口
├── CHANGELOG.md        # 版本记录
├── modules/            # 五层模块（逐子位分文件）
├── subskills/          # 专项子技能
└── references/         # 参考：审美标准 / 惊艳手法库 / 脚本工具 / 来源署名
```

## 安装

将本目录（或克隆后）放入 `~/.workbuddy/skills/design-workflow`（用户级）或 `{workspace}/.workbuddy/skills/design-workflow`（项目级）。

## 版本

当前 v1.6.2，详见 [CHANGELOG.md](CHANGELOG.md)。
