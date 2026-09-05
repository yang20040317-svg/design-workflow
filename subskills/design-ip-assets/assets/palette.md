---
id: palette
name: 三果红签名板
summary: 以正红为绝对识别锚点的专属配色，色即 IP
status: example
---

> 📌 **本文件为「示例（example）」**：演示如何按「专属配色签名」schema 填写。实际使用时请替换为你自己的签名色板。

# 专属配色签名：三果红

```yaml
signature:
  hex: "#E8412E"          # 三果红：IP 主识别色，出现即"这是三果团"
  role: 主识别色（角色本体 + 关键 CTA + 符号）
base:
  - "#FFF7F2"            # 暖白底（角色栖居的背景）
  - "#2B2422"            # 墨黑字/描边
  - "#E8E2DB"            # 分隔/浅灰
accents:
  - "#3E7D4F"            # 柄绿（仅小面积，角色柄/点缀）
  - "#F4B740"            # 暖黄（高光/星星点缀）
rule: "signature 红每作品必出现 ≥1 次；总色 ≤5；红占主视觉面积 ≥30%"
forbidden:
  - "AI 紫 #7C3AED"
  - "荧光渐变"
  - "冷蓝主调"
references:
  - palette-ref-01.png
```
