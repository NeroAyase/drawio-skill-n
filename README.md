# drawio-skill — From Text to Professional Diagrams

[中文文档](README_CN.md) | [Online Docs](https://agents365-ai.github.io/drawio-skill/)

## What it does

- Generates `.drawio` XML files from natural language descriptions
- Exports diagrams to PNG, SVG, PDF, or JPG using the native draw.io desktop CLI
- **6 diagram type presets**: ERD, UML Class, Sequence, Architecture, ML/Deep Learning, Flowchart — with preset shapes, styles, and layout conventions
- **Animated connectors** (`flowAnimation=1`) for data-flow and pipeline diagrams (visible in SVG and draw.io desktop)
- **ML model diagram support** with tensor shape annotations `(B, C, H, W)` — ideal for NeurIPS/ICML/ICLR papers
- **Grid-aligned layout** — all coordinates snap to 10px multiples for clean alignment
- **Browser fallback** — generates diagrams.net URLs when the desktop CLI is unavailable
- Iterative design: preview, get feedback, and refine diagrams until they look right
- **Auto-launch** draw.io desktop after export for manual fine-tuning
- Triggers automatically when diagrams would help explain complex systems
- **Style presets (v1.3 new)** — teach the skill your visual style from a `.drawio` file or image, save it by name, and apply it to future diagrams. See `## Style Presets` in SKILL.md.
- **Custom output directory (v1.4 new)** — ask for any output path (e.g. `./artifacts/`, `docs/images/`) and the skill will `mkdir -p` and export there; ideal for CI/CD artifact pipelines.

## Comparison

### vs No Skill (native agent)

| Feature | Native agent | This skill |
|---------|-------------|------------|
| Generate draw.io XML | Yes — LLMs know the format | Yes |
| Self-check after export | No | Yes — reads PNG and auto-fixes 6 issue types |
| Iterative review loop | No — must manually re-prompt | Yes — targeted edits, 5-round safety valve |
| Proactive triggers | No — only when explicitly asked | Yes — auto-suggests when 3+ components |
| Layout guidelines | None — varies by run | Complexity-scaled spacing, routing corridors, hub placement |
| Grid alignment | No | Yes — all coordinates snap to 10px multiples |
| Diagram type presets | No | Yes — 6 presets (ERD, UML, Sequence, Architecture, ML/DL, Flowchart) |
| Animated connectors | No | Yes — `flowAnimation=1` for data-flow visualization |
| ML model diagrams | No | Yes — tensor shape annotations, layer-type color coding |
| Color palette | Random/inconsistent | 7-color semantic system (blue=services, green=DB, purple=auth...) |
| Edge routing rules | Basic | Pin entry/exit points, distribute connections, waypoint corridors |
| Container/group patterns | None | Swimlane, group, custom container with parent-child nesting |
| Embed diagram in export | No | Yes — `--embed-diagram` keeps exported PNG/SVG/PDF editable |
| Browser fallback | No | Yes — generates diagrams.net URL when CLI unavailable |
| Auto-launch desktop app | No | Yes — opens `.drawio` file after export for fine-tuning |

### vs Other draw.io Skills & Tools

| Feature | This skill | [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) (official, 1.3k⭐) | [bahayonghang/drawio-skills](https://github.com/bahayonghang/drawio-skills) (60⭐) | [GBSOSS/ai-drawio](https://github.com/GBSOSS/ai-drawio) (63⭐) |
|---------|-----------|---------------|-------------------|--------------|
| **Approach** | Pure SKILL.md | SKILL.md / MCP / Project | YAML DSL + MCP | Plugin + browser |
| **Dependencies** | draw.io desktop only | draw.io desktop | MCP server (`npx`) | Browser + local server |
| **Multi-agent** | ✅ 6 platforms | ❌ Claude Code only | ❌ Claude Code only | ❌ |
| **Self-check** | ✅ 2-round auto-fix | ❌ | ❌ | ❌ screenshot |
| **Iterative review** | ✅ 5-round loop | ❌ generate once | ✅ 3 workflows | ❌ |
| **Layout guidance** | ✅ complexity-scaled + grid snap | ✅ basic spacing | ❌ relies on MCP | ❌ |
| **Diagram presets** | ✅ 6 types (ERD, UML, Seq, Arch, ML, Flow) | ❌ | ❌ | ❌ |
| **Animated edges** | ✅ `flowAnimation=1` | ❌ | ❌ | ❌ |
| **ML/DL diagrams** | ✅ tensor shapes, layer colors | ❌ | ❌ | ❌ |
| **Color system** | ✅ 7-color semantic | ❌ | ✅ 5 themes | ❌ |
| **Container/group** | ✅ swimlane + group | ✅ detailed | ❌ | ❌ |
| **Embed diagram** | ✅ `--embed-diagram` | ✅ | ❌ | ❌ |
| **Edge routing** | ✅ corridors + waypoints | ✅ arrowhead rules | ❌ | ❌ |
| **Browser fallback** | ✅ diagrams.net URL | ❌ | ❌ | ❌ |
| **Auto-launch** | ✅ opens desktop app | ❌ | ❌ | ❌ |
| **Cloud icons** | AWS basic | ❌ | ✅ AWS/GCP/Azure/K8s | ❌ |
| **Zero-config** | ✅ copy skills/drawio-skill/ | ✅ | ❌ needs `npx` | ❌ needs plugin install |

### Key advantages

1. **Self-check + iterative loop** — the only pure-SKILL.md solution that reads its own output and auto-fixes before showing the user, then supports multi-round refinement
2. **6 diagram type presets** — ERD, UML Class, Sequence, Architecture, ML/Deep Learning, Flowchart — each with preset shapes, styles, and layout conventions
3. **ML/DL model diagrams** — tensor shape annotations, layer-type color coding, encoder/decoder swimlanes — built for academic papers
4. **Multi-agent, zero-config** — works across 6 platforms with just the `skills/drawio-skill/` directory + draw.io desktop. No MCP server, no Python, no Node.js, no browser
5. **Production-grade layout** — grid-aligned coordinates, complexity-scaled spacing, routing corridors, hub-center strategy, animated connectors
6. **Browser fallback** — generates diagrams.net URLs when the desktop CLI is unavailable, plus auto-launch for desktop editing

## Supported diagram types

- **Architecture**: microservices, cloud (AWS/GCP/Azure), network topology, deployment — with tier-based swimlanes and hub-center strategy
- **ML / Deep Learning**: Transformer, CNN, LSTM, GRU architectures — with tensor shape annotations and layer-type color coding
- **Flowcharts**: business processes, workflows, decision trees, state machines — with semantic shape types (parallelogram I/O, diamond decisions)
- **UML**: class diagrams (inheritance/composition/aggregation arrows), sequence diagrams (lifelines, activation boxes)
- **Data**: ER diagrams (table containers, PK/FK notation), data flow diagrams (DFD)
- **Other**: org charts, mind maps, wireframes

## How it works

<p align="center">
  <img src="assets/workflow.png" width="420" alt="Workflow">
</p>

## Installation

Two steps — install the draw.io CLI first, then drop the skill into your host:

1. **[Install draw.io desktop](INSTALL_CLI.md)** — per-platform recipes for macOS / Windows / Linux.
2. **[Install the skill](INSTALL_SKILL.md)** — plugin marketplace (recommended), manual clone, and update commands.

## Usage

See [USAGE.md](USAGE.md) for natural-language prompts, a microservices walkthrough, and topology demos (star / layered / ring).

## Files

- `skills/drawio-skill/SKILL.md` — **the only required file**. Loaded by all platforms as the skill instructions.
- `skills/drawio-skill/references/` — detail references (diagram types, style presets, extraction, troubleshooting)
- `skills/drawio-skill/scripts/` — bundled scripts (PNG repair, browser URL encoder)
- `skills/drawio-skill/styles/built-in/` — built-in style presets (`default.json`, `corporate.json`, `handdrawn.json`)
- `README.md` — this file (English, displayed on GitHub homepage)
- `README_CN.md` — Chinese documentation
- `assets/` — example diagrams and workflow images

> **Note:** Only `skills/drawio-skill/SKILL.md` and its `references/` + `scripts/` + `styles/` are needed for the skill to work. The `assets/` and README files are documentation only and can be safely deleted to save space.

> All example diagrams were generated by Claude Opus 4.6 with this skill.

## Style Presets

Style presets let you capture and reuse a visual style across diagrams. When a preset is active, it replaces the built-in color palette, shape vocabulary, fonts, and edge defaults.

### Built-in presets

| Name | Description |
|------|-------------|
| `default` | Clean blue/green/yellow palette matching the built-in conventions |
| `corporate` | Muted, professional palette suited for business presentations |
| `handdrawn` | Sketch-style strokes for informal or whiteboard-style diagrams |

### Apply a preset to a diagram

```
Draw a microservices architecture using my "corporate" style
```

Or set a default so all future diagrams use it automatically:

```
Make "corporate" my default style
```

### Learn your style from a file

Point the skill at any `.drawio` file or flat image:

```
Learn my style from ~/diagrams/brand.drawio as "mybrand"
Learn my style from ~/diagrams/screenshot.png as "mybrand"
```

The skill extracts colors, shapes, fonts, and edge style, renders a sample diagram for preview, and saves to `~/.drawio-skill/styles/mybrand.json` only after you approve.

### Manage presets

| What you say | What happens |
|---|---|
| "list my styles" | Shows all user and built-in presets in a table |
| "show my `<name>` style" | Pretty-prints the preset JSON |
| "make `<name>` the default" | Sets it as the active default for all diagrams |
| "remove default" | Clears the default (reverts to built-in conventions) |
| "delete `<name>`" | Deletes the user preset (prompts for confirmation) |
| "rename `<a>` to `<b>`" | Renames a user preset |

## Known Limitations

- **Command name varies by platform**: macOS Homebrew installs the command as `draw.io`; some Linux packages use `drawio`. The skill handles both, but verify which name works on your system with `draw.io --version` or `drawio --version`
- **Linux headless export**: Requires `xvfb` for display virtualization — without it, CLI export will fail on servers without a display
- **Browser fallback requires Python**: The `diagrams.net` URL generator uses `python3` for compression/encoding. If neither CLI nor Python is available, the skill generates `.drawio` XML only
- **Self-check requires vision**: The auto-fix step reads exported PNGs using the model's vision capability. Models without vision support skip this step
- **Cloud icons**: Currently supports basic AWS resource icons. GCP, Azure, and Kubernetes icon sets are not yet included
- **No source .drawio for microservices example**: The `microservices-example.png` in assets was generated in a session but the source `.drawio` was not preserved

## License

MIT

## Support

If this skill helps you, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/awarding/award.gif" width="180" alt="Give a Reward">
      <br>
      <b>Give a Reward</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
