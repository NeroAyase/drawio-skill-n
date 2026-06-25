# Chinese Swimlane Layout

Use this reference for dense Chinese business-process diagrams, especially vertical swimlane diagrams with many nodes, exception paths, and long bypass connectors.

## Acceptance Gate

- Keep all visible labels in the user's language. For Chinese requests, use Chinese for titles, lanes, nodes, edge labels, notes, and legends by default. Preserve product names, protocols, APIs, file names, code symbols, and identifiers when translating them would be misleading.
- Text must not overlap text, borders, lane titles, edge labels, or connectors.
- Shapes must not overlap other shapes or swimlane/container title areas.
- Connectors must not run through unrelated shapes. Route long or cross-lane edges through outer corridors or empty row/column corridors.
- Edge labels must not sit on top of nodes. Prefer short labels with `labelBackgroundColor=#FFFFFF`; move labels with `<mxPoint as="offset">` when needed.
- Do not keep a long auxiliary edge if it makes the diagram tangled. Encode secondary detail in node text or a note instead.
- Run `scripts/validate.py` after edits. Treat warnings about overlaps, edge-through-shape, crossings, endpoint-normality, endpoint-stack, unpinned-auto-edge, lane-border-proximity, close-parallel-segment, and unnecessary-jog as fix-before-delivery items.
- Export every page to PNG and visually inspect all pages, not just page 1.

## Chinese Sizing Defaults

- Process/service rectangles: at least `220x80`; use `240x90` or larger for three or more lines.
- Decision diamonds: at least `220x110`; use `240x130` for labels with examples.
- Vertical swimlanes: at least `180px` high for one row of Chinese nodes; reserve a `140-160px` title band for vertical lane labels.
- Horizontal gaps between neighboring Chinese nodes: normally `180-260px`; increase only when an edge corridor or label needs it.
- Vertical gaps between node rows: normally `180px` or more.
- Edge routing corridors: reserve at least `100px` of empty space for long horizontal/vertical routes.
- Prefer grouping, row breaks, local vertical stacks, and compact spacing before widening the canvas.

## Compact Layout Strategy

- Divide long business flows into two or three visual zones, such as `接入/识别`, `核心处理`, and `执行/结果/异常`.
- Prefer a wrapped main route over one very long row when there are more than about 8-10 sequential nodes.
- Use local vertical stacks for stages that naturally belong together across lanes, such as `主体处理 -> 业务任务生成 -> 结果汇总 -> 审计追溯`.
- Keep the right edge of the diagram close to the last meaningful node or exception branch.
- Place exception/review nodes near the source column unless there is a clear semantic reason to group them elsewhere.

## Connector Routing Rules

- Pin `exitX/exitY` and `entryX/entryY` for every connector in dense swimlane/process diagrams.
- For left-to-right flow through a diamond, use left point for incoming and right point for primary outgoing: `entryX=0;entryY=0.5`, `exitX=1;exitY=0.5`.
- A diamond should have at most one horizontal outgoing edge on the right-point path. Route branch or bypass edges from top or bottom into a separate corridor.
- Distribute multiple connectors on the same shape across nearby points such as top-left, top-center, top-right, side-center, or bottom-center.
- For source/target vertices inside swimlanes but an edge with `parent="1"`, explicit waypoints must use absolute canvas coordinates, not child-relative coordinates.
- Route bypasses as clear orthogonal `L`/`U` paths above or below skipped nodes. Keep bypass segments at least `40px` from node borders and `24px` from swimlane borders.
- Put bypass labels such as `已有文本`, `异常`, `失败/超时`, `低置信度` on the long corridor, not next to branch endpoints.
- Keep neighboring parallel connector segments at least `24px` apart; separate dashed exception columns by at least `80px`.
- Collapse small U-shaped detours unless they carry a label or avoid a real obstacle.
- Align adjacent nodes exactly on center before relying on auto routing; small center mismatches often create unnecessary elbows.

## Endpoint Direction

- The first segment leaving a source should normally be perpendicular to the source side it exits.
- The final segment entering a target should normally be perpendicular to the target side it enters.
- For top/bottom exits or entries, place the adjacent waypoint on the same x-coordinate at least `30px` away from the shape.
- For left/right exits or entries, place the adjacent waypoint on the same y-coordinate at least `30px` away from the shape.
- Avoid corner-like entries on rounded rectangles; choose true side-center or top/bottom-center points.
- Do not add decorative bends just to repair direction. Move the nearest existing waypoint onto the exit/entry normal when possible.
- Diagonal edges are allowed when they are intentionally clearer, sparse, and do not cross nodes or labels.

## Generic Chinese Swimlane Template

For compact Chinese swimlane packages or dense cross-role business-process flows, prefer the bundled template script:

```powershell
python ".\scripts\chinese_swimlane_template.py" .\business-swimlane.drawio
python ".\scripts\validate.py" .\business-swimlane.drawio
drawio -x -f png --width 2200 -o .\business-swimlane-preview.png .\business-swimlane.drawio
```

Use the template as a starting layout, then replace labels and adjust local coordinates. Keep the template's compact zones, pinned endpoints, distributed exception routes, and separate pages for:

- `01-主流程泳道`
- `02-配置期与运行期`
- `03-字段与信息流`
- `04-异常分流与补偿`
