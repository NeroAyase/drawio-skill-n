# drawio-skill-n — Personal Fork of drawio-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Upstream](https://img.shields.io/badge/upstream-Agents365--ai%2Fdrawio--skill-blue)](https://github.com/Agents365-ai/drawio-skill)
[![Personal Fork](https://img.shields.io/badge/fork-personal%20preferences-6f42c1)](https://github.com/NeroAyase/drawio-skill-n)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2ea44f)](https://agentskills.io)

**English** · [中文](README_CN.md) · [📖 Online Docs](https://agents365-ai.github.io/drawio-skill/)

This repository is a personal fork of [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill). It keeps the original project's foundation and MIT license, while adding adjustments that fit my own Codex/draw.io workflow: leaner skill loading, stronger validation for dense Chinese swimlane diagrams, and a generic Chinese swimlane template. It is not an official replacement for the upstream project.

A skill that turns natural-language descriptions into `.drawio` XML and exports them to PNG / SVG / PDF / JPG via the native draw.io desktop CLI. It can also turn an **existing codebase** (Python / JS-TS / Go / Rust) into an auto-laid-out structure diagram. Works with **Claude Code, Cursor, Copilot, OpenClaw, Codex, Hermes**, and any agent compatible with the [Agent Skills](https://agentskills.io) format.

<p align="center">
  <img src="assets/microservices-example.png" width="900" alt="Microservices Architecture — generated from a single natural-language prompt">
</p>

## ✨ Highlights

- **6 diagram type presets** — ERD, UML Class, Sequence, Architecture, ML/Deep Learning, Flowchart
- **Visualize a codebase** — extract and auto-lay-out the structure of a Python / JS-TS / Go / Rust project (import graphs) or a Python class hierarchy — Graphviz placement, transitive reduction, nested module containers
- **Search 10,000+ official shapes** — resolve the exact AWS / Azure / GCP / Cisco / Kubernetes / UML / BPMN icon style instead of guessing (no more blank-box `shape=mxgraph.*` typos)
- **AI / LLM brand logos** — 321 logos (OpenAI, Claude, Gemini, Mistral, Llama, Ollama, LangChain…) that draw.io has none of, for LLM-app architecture diagrams
- **Self-check + auto-fix** — reads its own PNG output and auto-fixes overlaps, clipped labels, stacked edges, and more (up to 2 rounds)
- **Iterative feedback loop** — up to 5 rounds of targeted refinement
- **Style presets** — capture your visual style from a `.drawio` file or image, reuse on demand
- **Clean layout** — grid-aligned, spacing scales with diagram size, connectors routed clear of nodes
- **Multi-agent, zero-config** — runs from a single SKILL.md; no MCP server, no background daemon (the optional `npx` installer needs Node, the skill itself does not)

## 🖼️ Examples

> [!TIP]
> **The hero image above was generated from this single prompt:**

```
Create a microservices e-commerce architecture with Mobile/Web/Admin clients,
API Gateway (auth + rate limiting + routing), Auth/User/Order/Product/Payment
services, Kafka message queue, Notification service, and User DB / Order DB /
Product DB / Redis Cache / Stripe API
```

The skill is designed to route edges cleanly across different topologies, avoiding lines that cross through shapes:

<table>
  <tr>
    <td align="center" width="33%">
      <img src="assets/demo-star.png" alt="Star topology" width="100%"><br>
      <b>Star</b> · 7 nodes<br>
      <sub>Central message broker with 6 microservices radiating outward, no edge crossings on this example.</sub>
    </td>
    <td align="center" width="33%">
      <img src="assets/demo-layered.png" alt="Layered flow" width="100%"><br>
      <b>Layered</b> · 10 nodes / 4 tiers<br>
      <sub>E-commerce stack with horizontal and diagonal cross-connections routed via corridors.</sub>
    </td>
    <td align="center" width="33%">
      <img src="assets/demo-ring.png" alt="Ring cycle" width="100%"><br>
      <b>Ring</b> · 8 nodes<br>
      <sub>CI/CD pipeline with a closed loop and 2 spur branches flowing along the perimeter.</sub>
    </td>
  </tr>
</table>

Full walkthrough in [docs/USAGE.md](docs/USAGE.md).

## 🚀 Installation

### 1. Install the draw.io desktop CLI

| Platform | Command |
|----------|---------|
| **macOS** | `brew install --cask drawio` |
| **Windows** | [Download installer](https://github.com/jgraph/drawio-desktop/releases) |
| **Linux** | `.deb`/`.rpm` from [releases](https://github.com/jgraph/drawio-desktop/releases); `sudo apt install xvfb` for headless |

Verify with `drawio --version`. On **WSL2** the CLI is the Windows desktop exe reached via `/mnt/c` — the skill detects this automatically (see [troubleshooting](skills/drawio-skill/references/troubleshooting.md)). Full recipes in [docs/INSTALL_CLI.md](docs/INSTALL_CLI.md).

### 2. Install the skill

```bash
# Any agent (Claude Code, Cursor, Copilot, ...)
npx skills add Agents365-ai/365-skills -g
```

```text
# Claude Code plugin marketplace
> /plugin marketplace add Agents365-ai/365-skills
> /plugin install drawio
```

```bash
# Manual install
git clone https://github.com/Agents365-ai/drawio-skill.git \
  ~/.claude/skills/drawio-skill
```

Also indexed on [SkillsMP](https://skillsmp.com/skills/agents365-ai-drawio-skill-skills-drawio-skill-skill-md) and [ClawHub](https://clawhub.ai/agents365-ai/drawio-pro-skill).

**Updating:** `/plugin update drawio` (Claude Code), `skills update drawio-skill` (SkillsMP), `clawhub update drawio-pro-skill` (OpenClaw), or `git pull` for manual installs — see [docs/INSTALL_SKILL.md#updates](docs/INSTALL_SKILL.md#updates). Release history in [CHANGELOG.md](CHANGELOG.md).

## ⚡ Quick Start

After installation, just describe what you want. For example, an ML model:

```
Draw a Transformer encoder-decoder for machine translation: 6-layer encoder
with self-attention, 6-layer decoder with cross-attention, input embeddings
(batch × 512 × 768), positional encoding, and a final output projection.
Annotate tensor shapes between layers and color-code by layer type.
```

The skill plans the layout, generates the `.drawio` XML, exports to your chosen format, self-checks the result, and lets you iterate.

## 🗺️ Visualize a Codebase

Beyond hand-authored diagrams, the skill turns **existing code into structure diagrams** — no manual coordinates. Just ask:

> *"Visualize the module structure of this Python project"* · *"Draw the class hierarchy of `mypackage`"*

<p align="center">
  <img src="assets/code-structure-example.png" width="900" alt="Auto-generated class hierarchy of Python's logging package — modules boxed, inheritance arrows resolved">
</p>

<sub>↑ Python's <code>logging</code> package as a class hierarchy — one command, modules auto-boxed, every inheritance edge resolved.</sub>

Under the hood it runs a bundled extractor → auto-layout → validate pipeline:

```bash
# Import graph — Python / JS-TS / Go / Rust
python3 scripts/pyimports.py   myproject --group -o graph.json
python3 scripts/jsimports.py   ./src     --group -o graph.json
python3 scripts/goimports.py   ./module  --group -o graph.json
python3 scripts/rustimports.py ./crate   --group -o graph.json

# Python class-inheritance hierarchy
python3 scripts/pyclasses.py   mypackage --group -o graph.json

# any extractor → auto-layout → editable .drawio
python3 scripts/autolayout.py  graph.json -o diagram.drawio
```

| Piece | What it does |
|---|---|
| **5 extractors** | import graphs for **Python · JS/TS · Go · Rust**, plus **Python class inheritance** |
| **Auto-layout** | Graphviz places nodes and routes orthogonal edges *around* them — removes the manual-coordinate ceiling for large graphs |
| **Transitive reduction** | drops edges implied by a longer path, turning a dense hairball into a traceable graph (asyncio: 149 → 46 edges) |
| **Nested containers** | `--group` boxes modules by sub-package, nested for deep package trees |
| **Deterministic validator** | `validate.py` lints the `.drawio` (dangling edges, duplicate ids, overlaps) before the visual self-check |

Layout needs Graphviz (`brew install graphviz` / `apt install graphviz`) — optional; everything else works without it. Full format + flag reference in [references/autolayout.md](skills/drawio-skill/references/autolayout.md).

## 🧩 Supported Diagram Types

| Category | Examples | Notable features |
|---|---|---|
| Architecture | microservices, cloud (AWS/GCP/Azure), network topology, deployment | Tier-based swimlanes, hub-center strategy |
| ML / Deep Learning | Transformer, CNN, LSTM, GRU | Tensor shape annotations, layer-type color coding |
| Flowcharts | business processes, workflows, decision trees, state machines | Semantic shapes (parallelogram I/O, diamond decisions) |
| UML | class diagrams, sequence diagrams | Inheritance / composition / aggregation arrows; lifelines + activation boxes |
| Data | ER diagrams, data flow diagrams (DFD) | Table containers, PK/FK notation |
| Other | org charts, mind maps, wireframes | — |

## 🔍 Shape Search

Need a real AWS / Azure / GCP / Cisco / Kubernetes / UML / BPMN icon? The skill searches **10,000+ official draw.io shapes** for the exact style string — so vendor icons render correctly instead of falling back to a blank box from a guessed `shape=mxgraph.*` name.

> *"Add an AWS Lambda wired to an S3 bucket"* · *"Use the real Kubernetes pod icon"*

```bash
python3 scripts/shapesearch.py "aws lambda" --limit 5
# → Lambda (77x93)
#   outlineConnect=0;...;shape=mxgraph.aws3.lambda;fillColor=#F58534;...
```

<p align="center">
  <img src="assets/shape-search-example.png" width="900" alt="Serverless AWS architecture built from official draw.io icons resolved by shapesearch.py">
</p>

<sub>↑ A serverless AWS architecture — every icon is the real official draw.io shape resolved by <code>shapesearch.py</code>, not a hand-guessed <code>shape=</code> string.</sub>

Covers AWS / Azure / GCP / Cisco / Kubernetes / UML / BPMN / ER / electrical / P&ID and the general shape sets. Hand-writable style cheatsheet + search usage in [references/shapes.md](skills/drawio-skill/references/shapes.md).

## 🤖 AI / LLM Brand Logos

draw.io ships **no** modern AI/LLM logos, so an LLM-app diagram renders as generic boxes. `aiicons.py` resolves a brand name to a draw.io image style for any of **321 logos** (OpenAI, Claude, Gemini, Mistral, Llama, Cohere, DeepSeek, Qwen, Ollama, LangChain, HuggingFace…) from [lobe-icons](https://github.com/lobehub/lobe-icons) (MIT).

```bash
python3 scripts/aiicons.py "claude" --json      # CDN-referenced (default)
python3 scripts/aiicons.py "openai" --embed     # self-contained data URI
```

<p align="center">
  <img src="assets/ai-logos-example.png" width="900" alt="Multi-provider LLM app diagram with real AI brand logos resolved by aiicons.py">
</p>

<sub>↑ A multi-provider LLM app — every brand logo resolved by <code>aiicons.py</code>. Icons are referenced from the unpkg CDN by default (network needed at render time); <code>--embed</code> inlines them for offline use. Logos are trademarks of their owners, used for identification only.</sub>

## 🎨 Style Presets

Capture a visual style once, reuse it everywhere. Three presets are built in — `default`, `corporate`, `handdrawn` — and you can teach the skill your own style from a `.drawio` file or a flat image:

```
Draw a microservices architecture using my "corporate" style
```

```
Learn my style from ~/diagrams/brand.drawio as "mybrand"
```

The skill extracts colors, shapes, fonts, and edge style, renders a preview, and only saves the preset after you approve. Full preset-management commands in [docs/STYLE_PRESETS.md](docs/STYLE_PRESETS.md).

## 🔄 How it works

<p align="center">
  <img src="assets/workflow.png" width="700" alt="Internal workflow">
</p>

Behind the scenes: **check dependencies → plan layout → generate `.drawio` XML → export draft PNG → self-check + auto-fix** (up to 2 rounds) → **show to user → 5-round feedback loop** until approved → **final export**.

## 🆚 Comparison

### vs Native Agent (no skill)

| Feature | Native agent | drawio-skill |
|---|---|---|
| Self-check after export | ❌ | ✅ reads PNG, auto-fixes 6 issue types |
| Iterative review loop | ❌ manual re-prompt | ✅ targeted edits, 5-round safety valve |
| Diagram type presets | ❌ | ✅ 6 presets (ERD, UML, Seq, Arch, ML, Flow) |
| Visualize a codebase | ❌ | ✅ import graphs (Py/JS/Go/Rust) + class diagrams |
| Auto-layout for large graphs | ❌ hand-places, overlaps | ✅ Graphviz placement, ortho routing, nested containers |
| Structural validation | ❌ | ✅ deterministic `.drawio` linter |
| Official shape search | ❌ guesses, blank boxes | ✅ exact style for 10k+ AWS/Azure/GCP/UML shapes |
| AI/LLM brand logos | ❌ none | ✅ 321 logos (OpenAI/Claude/Gemini/…) via aiicons.py |
| Grid-aligned layout | ❌ | ✅ 10px snap, routing corridors |
| Color palette | random / inconsistent | ✅ 7-color semantic system |
| Style presets | ❌ | ✅ learn from `.drawio` file or image |

### vs Other draw.io Skills & Tools

| Feature | drawio-skill | [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) (official)<br>![stars](https://img.shields.io/github/stars/jgraph/drawio-mcp?style=flat-square&logo=github&v=2) | [bahayonghang/drawio-skills](https://github.com/bahayonghang/drawio-skills)<br>![stars](https://img.shields.io/github/stars/bahayonghang/drawio-skills?style=flat-square&logo=github) | [GBSOSS/ai-drawio](https://github.com/GBSOSS/ai-drawio)<br>![stars](https://img.shields.io/github/stars/GBSOSS/ai-drawio?style=flat-square&logo=github) |
|---|---|---|---|---|
| **Approach** | Pure SKILL.md | SKILL.md / MCP / Project | YAML DSL + CLI (MCP optional) | Claude Code plugin |
| **Dependencies** | draw.io desktop only | draw.io desktop | draw.io desktop (MCP optional) | draw.io plugin + browser |
| **Multi-agent** | ✅ 6 platforms | ❌ Claude apps only | ✅ Claude / Gemini / Codex | ❌ Claude Code only |
| **Self-check + auto-fix** | ✅ 2-round (reads PNG) | ❌ | ✅ validation + strict mode | ❌ screenshot only |
| **Iterative review** | ✅ 5-round loop | ❌ generate once | ✅ 3 workflows | ❌ |
| **Diagram presets** | ✅ 6 types | ❌ | ✅ paper-mode classifier | ❌ |
| **ML/DL diagrams** | ✅ tensor shapes, layer colors | ❌ | ❌ | ❌ |
| **Color system** | ✅ 7-color semantic | ❌ | ✅ 6 themes | ❌ |
| **Official shape search** | ✅ 10k+ shapes (local) | ✅ 10k+ shapes (MCP) | ❌ | ❌ |
| **AI/LLM brand logos** | ✅ 321 (lobe-icons) | ❌ | ❌ | ❌ |
| **Browser fallback** | ✅ diagrams.net URL (viewer + editable) | ❌ inline preview only | ✅ via optional MCP | ✅ diagrams.net viewer (primary) |
| **Zero-config** | ✅ copy `skills/drawio-skill/` | ✅ | ✅ desktop-only mode | ❌ needs plugin install |

Full comparison + key-advantages summary in [docs/COMPARISON.md](docs/COMPARISON.md) (with audit timestamp).

## 🎯 When to use (and when not to)

**Good fit:**
- Polished, precise diagrams — stakeholder decks, architecture, network topology, strict UML, ER diagrams
- Solid opaque fills, 10,000+ official shapes, branded icons (AWS / Azure / GCP / Cisco / Kubernetes + AI/LLM logos), swimlanes, and custom geometry
- Anything you'll export to PNG / SVG / PDF and keep editable

**Reach for a sibling skill instead when you need:**
- **A casual, hand-drawn / whiteboard look** → [excalidraw-skill](https://github.com/Agents365-ai/excalidraw-skill) or [tldraw-skill](https://github.com/Agents365-ai/tldraw-skill)
- **Diagrams-as-code that live in git and render in Markdown** → [mermaid-skill](https://github.com/Agents365-ai/mermaid-skill) (general) or [plantuml-skill](https://github.com/Agents365-ai/plantuml-skill) (UML)
- **Freeform infinite-canvas sketching / freehand strokes** → [tldraw-skill](https://github.com/Agents365-ai/tldraw-skill)

## 🔗 Related Skills

Part of the [Agents365-ai diagram-skill family](https://github.com/Agents365-ai) — pick the right tool for the job:

| Skill | Style | Best for |
|---|---|---|
| [excalidraw-skill](https://github.com/Agents365-ai/excalidraw-skill) | Hand-drawn / sketchy | Whiteboard mockups, informal diagrams |
| [mermaid-skill](https://github.com/Agents365-ai/mermaid-skill) | Text-based, auto-layout | README-embeddable, version-control friendly |
| [plantuml-skill](https://github.com/Agents365-ai/plantuml-skill) | UML-focused | Class / sequence diagrams in CI pipelines |
| [tldraw-skill](https://github.com/Agents365-ai/tldraw-skill) | Whiteboard collaboration | Casual sketches, FigJam-style boards |

## 🙏 Upstream

This fork is based on the original work by **Agents365-ai**:

- Upstream repository: https://github.com/Agents365-ai/drawio-skill
- Author profile: https://github.com/Agents365-ai

The changes in this fork are personal workflow adjustments and are maintained for my own usage habits.

## 📄 License

[MIT](LICENSE)
