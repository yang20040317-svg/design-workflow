---
id: character
name: 三果团 (Sanguo Tuan)
summary: 三个叠坐的红色圆胖果实小精怪，各有表情，呆萌有情绪，是 IP 的人格载体
status: example
---

> 📌 **本文件为「示例（example）」**：演示如何按「角色/吉祥物 IP」schema 填写。它不是强制资产——实际使用时请替换为你自己的 IP，或另建 `assets/<your-ip>-character.md` 后改名为 `character.md`。

# 角色/吉祥物 IP：三果团

> 基于原始视觉（三个叠放的红色圆胖果实 + 表情）去风险化重定义的原创 IP。固定比例与识别点，仅姿态/场景可变。

```yaml
form:
  species: 拟人化果实（原创，非特定真实水果）
  silhouette: 三个圆球纵向叠坐的团子剪影，远看即认
  proportions: 头身比约 1:0.6（极圆胖），三球等大略变小
  key_features:
    - 通体正红圆润无棱角
    - 顶端一小绿柄（唯一非红元素）
    - 中间球有简单表情（点眼 + 弧嘴），上下两球无脸或极简
    - 底部两小短脚/坐痕
color: 引用 palette.md 的 signature 红（#E8412E）
posture_library: [叠坐, 探头, 举小旗, 躺平, 排排站]
expression: 默认呆滞微甜，可切换 开心/惊讶/困
forbidden:
  - 瘦长尖脸
  - 写实照片感
  - 去除绿色小柄
references:
  - character-ref-01.png   # 原始参考（用户给的视觉，仅作风格参照，非商用素材）
```

## 说明
- 原始图为第三方作品，仅作为"形状/气质"参考，不内置为资产图，避免版权问题。
- 真实角色图后续由用户在生图/建模工具按本 schema 产出后，存 `character-ref-0x.png` 替换占位。
