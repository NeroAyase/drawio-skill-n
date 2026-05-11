# drawio-skill — From Text to Professional Diagrams

[English](README.md) | [Online Docs](https://agents365-ai.github.io/drawio-skill/)

## 功能说明

- 根据自然语言描述生成 `.drawio` XML 文件
- 使用 draw.io 桌面版原生 CLI 将图表导出为 PNG、SVG、PDF 或 JPG
- **6 种图表类型预设**：ERD、UML 类图、序列图、架构图、ML/深度学习、流程图 — 包含预设形状、样式和布局规范
- **动画连接线** (`flowAnimation=1`) 适用于数据流和管道图（在 SVG 和 draw.io 桌面版中可见）
- **ML 模型图支持** 带张量形状标注 `(B, C, H, W)` — 适合 NeurIPS/ICML/ICLR 论文
- **网格对齐布局** — 所有坐标对齐到 10px 倍数，确保整洁对齐
- **浏览器降级方案** — 当桌面 CLI 不可用时生成 diagrams.net URL
- 迭代设计：预览、获取反馈、反复优化直到图表满意为止
- **自动启动** draw.io 桌面版，导出后可直接精修
- 当图表有助于解释复杂系统时自动触发
- **样式预设（v1.3 新增）** — 用一个 `.drawio` 文件或图片"教会"Skill 你的风格，命名保存后可在后续图表中复用。详见 SKILL.md 的 `## Style Presets` 小节。
- **自定义输出目录（v1.4 新增）** — 在提示里指定任意路径（如 `./artifacts/`、`docs/images/`），Skill 会自动 `mkdir -p` 并导出到那里；适合 CI/CD 产物流水线。

## 对比

### 与无 skill 的原生智能体对比

| 功能 | 原生智能体 | 本 skill |
|------|-----------|---------|
| 生成 draw.io XML | 是 — LLM 本身了解格式 | 是 |
| 导出后自检 | 否 | 是 — 读取 PNG 自动修复 6 类问题 |
| 迭代反馈循环 | 否 — 需手动重新提问 | 是 — 定向编辑，5 轮安全阀 |
| 主动触发 | 否 — 仅在明确要求时 | 是 — 3+ 组件时自动建议画图 |
| 布局规范 | 无 — 每次结果不一致 | 按复杂度分级间距、路由走廊、hub 居中策略 |
| 网格对齐 | 否 | 是 — 所有坐标对齐到 10px 倍数 |
| 图表类型预设 | 否 | 是 — 6 种预设（ERD、UML、序列图、架构图、ML/DL、流程图） |
| 动画连接线 | 否 | 是 — `flowAnimation=1` 数据流可视化 |
| ML/DL 模型图 | 否 | 是 — 张量形状标注、层类型配色 |
| 配色方案 | 随机/不一致 | 7 色语义系统（蓝=服务、绿=数据库、紫=安全…） |
| 连线路由规则 | 基础 | 锚点分配、连接分布、走廊绕行 |
| 容器/分组 | 无 | Swimlane、Group、自定义容器 + 父子嵌套 |
| 嵌入式导出 | 否 | 是 — `--embed-diagram` 保持导出文件可编辑 |
| 浏览器降级 | 否 | 是 — CLI 不可用时生成 diagrams.net URL |
| 自动启动桌面版 | 否 | 是 — 导出后自动打开 `.drawio` 文件精修 |

### 与其他 draw.io Skills / 工具对比

| 功能 | 本 skill | [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)（官方，1.3k⭐） | [bahayonghang/drawio-skills](https://github.com/bahayonghang/drawio-skills)（60⭐） | [GBSOSS/ai-drawio](https://github.com/GBSOSS/ai-drawio)（63⭐） |
|---------|-----------|---------------|-------------------|--------------|
| **方式** | 纯 SKILL.md | SKILL.md / MCP / Project | YAML DSL + MCP | 插件 + 浏览器 |
| **依赖** | 仅 draw.io 桌面版 | draw.io 桌面版 | MCP 服务（`npx`） | 浏览器 + 本地服务 |
| **多智能体** | ✅ 6 个平台 | ❌ 仅 Claude Code | ❌ 仅 Claude Code | ❌ |
| **自检** | ✅ 2 轮自动修复 | ❌ | ❌ | ❌ 截图 |
| **迭代审查** | ✅ 5 轮循环 | ❌ 一次生成 | ✅ 3 种工作流 | ❌ |
| **布局指南** | ✅ 按复杂度分级 + 网格对齐 | ✅ 基础间距 | ❌ 依赖 MCP | ❌ |
| **图表预设** | ✅ 6 种（ERD、UML、序列、架构、ML、流程） | ❌ | ❌ | ❌ |
| **动画连线** | ✅ `flowAnimation=1` | ❌ | ❌ | ❌ |
| **ML/DL 图** | ✅ 张量标注、层配色 | ❌ | ❌ | ❌ |
| **配色系统** | ✅ 7 色语义 | ❌ | ✅ 5 种主题 | ❌ |
| **容器/分组** | ✅ swimlane + group | ✅ 详细 | ❌ | ❌ |
| **嵌入式导出** | ✅ `--embed-diagram` | ✅ | ❌ | ❌ |
| **连线路由** | ✅ 走廊 + waypoints | ✅ 箭头间距规则 | ❌ | ❌ |
| **浏览器降级** | ✅ diagrams.net URL | ❌ | ❌ | ❌ |
| **自动启动** | ✅ 打开桌面版 | ❌ | ❌ | ❌ |
| **云图标** | AWS 基础 | ❌ | ✅ AWS/GCP/Azure/K8s | ❌ |
| **零配置** | ✅ 复制 skills/drawio-skill/ | ✅ | ❌ 需要 `npx` | ❌ 需安装插件 |

### 核心优势

1. **自检 + 迭代循环** — 唯一纯 SKILL.md 方案中能自动读取输出、修复问题、支持多轮优化的
2. **6 种图表类型预设** — ERD、UML 类图、序列图、架构图、ML/深度学习、流程图 — 每种都有预设形状、样式和布局规范
3. **ML/DL 模型图** — 张量形状标注、层类型配色、编码器/解码器泳道 — 专为学术论文打造
4. **多智能体、零配置** — 跨 6 个平台运行，仅需 `skills/drawio-skill/` 目录 + draw.io 桌面版，无需 MCP、Python、Node.js、浏览器
5. **专业级布局** — 网格对齐坐标、按复杂度分级间距、路由走廊、hub 居中策略、动画连接线
6. **浏览器降级** — 桌面 CLI 不可用时生成 diagrams.net URL，导出后自动启动桌面版编辑

## 支持的图表类型

- **架构图**：微服务架构、云架构（AWS/GCP/Azure）、网络拓扑、部署架构 — 带分层泳道和 hub 居中策略
- **ML / 深度学习**：Transformer、CNN、LSTM、GRU 架构 — 带张量形状标注和层类型配色
- **流程图**：业务流程、工作流、决策树、状态机 — 带语义形状（平行四边形 I/O、菱形判断）
- **UML**：类图（继承/组合/聚合箭头）、序列图（生命线、激活框）
- **数据图**：ER 图（表容器、PK/FK 标记）、数据流图（DFD）
- **其他**：组织架构图、思维导图、线框图

## 工作流程

<p align="center">
  <img src="assets/workflow-cn.png" width="420" alt="工作流程">
</p>

## 安装

两步 —— 先装 draw.io CLI,再把技能加载到 host:

1. **[安装 draw.io 桌面版](INSTALL_CLI_CN.md)** —— macOS / Windows / Linux 各平台配方。
2. **[安装技能](INSTALL_SKILL_CN.md)** —— 插件市场(推荐)、手动克隆、以及更新命令。

## 使用方式

参见 [USAGE_CN.md](USAGE_CN.md) —— 包含自然语言提示词、微服务示例,以及多种拓扑演示(星形 / 分层 / 环形)。

## 文件说明

- `skills/drawio-skill/SKILL.md` — **唯一必需的文件**，所有平台加载的 skill 指令
- `skills/drawio-skill/references/` — 详细参考（图表类型、样式预设、提取算法、故障排除）
- `skills/drawio-skill/scripts/` — 内置脚本（PNG 修复、浏览器 URL 编码器）
- `skills/drawio-skill/styles/built-in/` — 内置样式预设（`default.json`、`corporate.json`、`handdrawn.json`）
- `README.md` — 英文说明（GitHub 首页显示）
- `README_CN.md` — 本文件（中文）
- `assets/` — 示例图表和工作流图片

> **提示：** 仅 `skills/drawio-skill/SKILL.md` 及其 `references/` + `scripts/` + `styles/` 为 skill 运行所必需。`assets/` 和 README 文件仅为文档用途，可以安全删除以节省空间。

> 所有示例图表均由 Claude Opus 4.6 配合本 skill 生成。

## 样式预设

样式预设让你捕获并复用视觉风格，跨多张图表保持一致。激活预设后，它会替代内置的配色、形状词汇、字体和连线默认值。

### 内置预设

| 名称 | 说明 |
|------|------|
| `default` | 干净的蓝/绿/黄配色，与内置规范保持一致 |
| `corporate` | 低饱和度专业配色，适合商务演示 |
| `handdrawn` | 手绘描边风格，适合非正式或白板式图表 |

### 将预设应用到图表

```
画一个微服务架构图，使用我的 "corporate" 样式
```

或者设置默认样式，让后续所有图表自动使用：

```
把 "corporate" 设为我的默认样式
```

### 从文件中学习样式

指向任意 `.drawio` 文件或图片：

```
从 ~/diagrams/brand.drawio 学习我的样式，保存为 "mybrand"
从 ~/diagrams/screenshot.png 学习我的样式，保存为 "mybrand"
```

Skill 会自动提取配色、形状、字体和连线风格，渲染样例图供预览，确认后才保存至 `~/.drawio-skill/styles/mybrand.json`。

### 管理预设

| 你说的话 | 发生什么 |
|---|---|
| "列出我的样式" | 以表格展示所有用户和内置预设 |
| "显示我的 `<name>` 样式" | 格式化输出预设 JSON |
| "把 `<name>` 设为默认" | 设为所有图表的默认激活预设 |
| "取消默认" | 清除默认（恢复内置规范） |
| "删除 `<name>`" | 删除用户预设（会请求确认） |
| "把 `<a>` 重命名为 `<b>`" | 重命名用户预设 |

## 已知限制

- **命令名因平台而异**：macOS Homebrew 安装的命令是 `draw.io`，部分 Linux 包使用 `drawio`。本 skill 兼容两者，请用 `draw.io --version` 或 `drawio --version` 确认你的系统使用哪个
- **Linux 无头导出**：需要 `xvfb` 进行显示虚拟化 — 没有显示器的服务器上 CLI 导出会失败
- **浏览器降级需要 Python**：`diagrams.net` URL 生成器使用 `python3` 进行压缩/编码。如果 CLI 和 Python 都不可用，skill 仅生成 `.drawio` XML 文件
- **自检需要视觉能力**：自动修复步骤需要模型的视觉能力来读取导出的 PNG。不支持视觉的模型会跳过此步骤
- **云图标**：目前支持基础 AWS 资源图标。GCP、Azure 和 Kubernetes 图标集尚未包含
- **微服务示例缺少源文件**：`assets/` 中的 `microservices-example.png` 在会话中生成，但源 `.drawio` 文件未保留

## 开源协议

MIT

## 支持作者

如果这个 skill 对你有帮助，欢迎支持作者：

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="微信支付">
      <br>
      <b>微信支付</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="支付宝">
      <br>
      <b>支付宝</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/awarding/award.gif" width="180" alt="打赏">
      <br>
      <b>打赏</b>
    </td>
  </tr>
</table>

## 作者

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
