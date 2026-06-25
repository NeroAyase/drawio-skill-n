import argparse
from pathlib import Path
import html


DEFAULT_OUT = Path("business-swimlane-template.drawio")


def esc(value):
    return html.escape(value, quote=True).replace("\n", "&#xa;")


def style(parts):
    base = ["whiteSpace=wrap", "html=1", "fontSize=14", "spacing=6"]
    return ";".join(parts + base) + ";"


EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#455A64;fontSize=13;labelBackgroundColor=#FFFFFF;spacing=4;"
EDGE_DASH_RED = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#D32F2F;dashed=1;fontSize=13;labelBackgroundColor=#FFFFFF;spacing=4;"
EDGE_RED = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#D32F2F;fontSize=13;labelBackgroundColor=#FFFFFF;spacing=4;"
EDGE_CFG = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;strokeColor=#F9A825;dashed=1;fontSize=13;labelBackgroundColor=#FFFFFF;spacing=4;"


def geom(x, y, w, h):
    return f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />'


def cell(id_, value, sty, x, y, w, h, parent="1", vertex=True):
    return (
        f'        <mxCell id="{id_}" value="{esc(value)}" style="{sty}" '
        f'{"vertex" if vertex else "edge"}="1" parent="{parent}">\n'
        f"          {geom(x, y, w, h)}\n"
        f"        </mxCell>"
    )


def vertex(id_, value, shape, fill, stroke, x, y, w, h, parent="1"):
    return cell(id_, value, style([shape, f"fillColor={fill}", f"strokeColor={stroke}"]), x, y, w, h, parent)


def text(id_, value, x, y, w=620, h=40, size=24):
    sty = f"text;html=1;strokeColor=none;fillColor=none;fontSize={size};fontStyle=1;align=left;verticalAlign=middle;"
    return cell(id_, value, sty, x, y, w, h)


def lane(id_, value, y, fill, stroke, width=3900, height=190):
    sty = f"swimlane;horizontal=0;startSize=150;fillColor={fill};strokeColor={stroke};fontSize=18;fontStyle=1;html=1;whiteSpace=wrap;spacing=6;"
    return cell(id_, value, sty, 40, y, width, height)


def edge(id_, src, dst, value="", sty=EDGE, points=None, offset=None):
    body = f'        <mxCell id="{id_}" value="{esc(value)}" style="{sty}" edge="1" parent="1" source="{src}" target="{dst}">\n'
    if points or offset:
        body += '          <mxGeometry relative="1" as="geometry">\n'
        if points:
            body += '            <Array as="points">\n'
            for x, y in points:
                body += f'              <mxPoint x="{x}" y="{y}" />\n'
            body += '            </Array>\n'
        if offset:
            body += f'            <mxPoint x="{offset[0]}" y="{offset[1]}" as="offset" />\n'
        body += '          </mxGeometry>\n'
    else:
        body += '          <mxGeometry relative="1" as="geometry" />\n'
    body += '        </mxCell>'
    return body


def graph(cells, dx=1422, dy=794):
    return (
        f'    <mxGraphModel dx="{dx}" dy="{dy}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        'arrows="1" fold="1" page="1" pageScale="1" pageWidth="4000" pageHeight="1300" math="0" shadow="0">\n'
        "      <root>\n"
        '        <mxCell id="0" />\n'
        '        <mxCell id="1" parent="0" />\n'
        + "\n".join(cells)
        + "\n      </root>\n"
        "    </mxGraphModel>"
    )


def page(name, id_, cells):
    return f'  <diagram id="{id_}" name="{esc(name)}">\n{graph(cells)}\n  </diagram>'


def main_page():
    cells = [text("title1", "通用业务泳道流程图（主流程）", 40, 20, 900)]
    lanes = [
        ("lane_ext", "业务发起方", 90, "#E1F5FE", "#0288D1", 2900, 190),
        ("lane_intake", "接入与识别", 280, "#FFF8E1", "#F9A825", 2900, 190),
        ("lane_text", "核心处理", 470, "#E8F5E9", "#43A047", 2900, 230),
        ("lane_quality", "业务执行", 700, "#F3E5F5", "#8E24AA", 2900, 190),
        ("lane_result", "结果使用", 890, "#E8EAF6", "#3949AB", 2900, 190),
        ("lane_support", "异常与追溯", 1080, "#FFEBEE", "#D32F2F", 2900, 190),
    ]
    cells += [lane(*l) for l in lanes]
    xs = [220, 560, 910, 1260, 1610, 1960, 2310]
    box = ("rounded=1", 220, 86)
    doc = ("shape=mxgraph.flowchart.document", 220, 92)
    dia = ("rhombus", 220, 112)
    cells += [
        vertex("m1", "业务触发\n前台 / 渠道 / 系统 / 批处理任务", box[0], "#B3E5FC", "#0288D1", xs[0], 40, box[1], box[2], "lane_ext"),
        vertex("m2", "提交业务请求\n场景ID + 业务单号 + 主体元数据", doc[0], "#B3E5FC", "#0288D1", xs[1], 37, doc[1], doc[2], "lane_ext"),
        vertex("m3", "入参校验\n场景ID / 业务单 / 主体编码 / 数据内容", dia[0], "#FFF3C4", "#F9A825", xs[0], 40, dia[1], dia[2], "lane_intake"),
        vertex("m4", "场景自动匹配\n加载规则组 / 链路 / 时效 / 字段要求", box[0], "#FFF3C4", "#F9A825", xs[1], 56, box[1], 80, "lane_intake"),
        vertex("m5", "链路分流\n标准链路 or 已有结果链路", dia[0], "#C8E6C9", "#43A047", xs[1], 73, dia[1], dia[2], "lane_text"),
        vertex("m6", "数据预处理\n格式检查 / 转换标记 / 切片预留", box[0], "#C8E6C9", "#43A047", xs[2], 86, box[1], box[2], "lane_text"),
        vertex("m7", "核心服务处理\n提交任务 / 排队 / 回调或轮询", box[0], "#C8E6C9", "#43A047", xs[3], 86, box[1], box[2], "lane_text"),
        vertex("m8", "数据标准化\n分段 / 时间戳 / 置信度 / 数据来源", box[0], "#C8E6C9", "#43A047", xs[4], 86, box[1], box[2], "lane_text"),
        vertex("m9", "主体处理\n渠道映射 / 角色映射 / 主体编码", box[0], "#C8E6C9", "#43A047", xs[5], 86, box[1], box[2], "lane_text"),
        vertex("m10", "业务任务生成\n去重 / 优先级 / 截止时间", box[0], "#E1BEE7", "#8E24AA", xs[4], 70, box[1], box[2], "lane_quality"),
        vertex("m11", "规则执行\n关键词 / 固定规则 / 语义规则", box[0], "#E1BEE7", "#8E24AA", xs[5], 70, box[1], box[2], "lane_quality"),
        vertex("m12", "智能判断\n完整性 / 风险 / 意图变化", box[0], "#E1BEE7", "#8E24AA", xs[6], 70, box[1], box[2], "lane_quality"),
        vertex("m13", "结果汇总\n总体结论 / 规则明细 / 风险等级", box[0], "#C5CAE9", "#3949AB", xs[4], 70, box[1], box[2], "lane_result"),
        vertex("m14", "证据留存与回放\n命中片段 / 时间戳 / 角色", box[0], "#C5CAE9", "#3949AB", xs[5], 70, box[1], box[2], "lane_result"),
        vertex("m15", "报表 / 导出 / 下游同步\n覆盖率 / 命中率 / 批次记录", box[0], "#C5CAE9", "#3949AB", xs[6], 70, box[1], box[2], "lane_result"),
        vertex("m16", "异常队列\n字段缺失 / 未知场景 / 服务失败 / 模型失败", box[0], "#FFCDD2", "#D32F2F", xs[0], 52, box[1], box[2], "lane_support"),
        vertex("m17", "人工复核预留\n低置信度 / 角色不确定 / 高风险", box[0], "#FFCDD2", "#D32F2F", xs[6], 52, box[1], box[2], "lane_support"),
        vertex("m18", "审计追溯\n任务ID / 规则版本 / 模型版本 / 配置版本", box[0], "#FFCDD2", "#D32F2F", xs[4], 52, box[1], box[2], "lane_support"),
    ]
    cells += [
        edge("e1", "m1", "m2", sty=EDGE + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"),
        edge("e2", "m2", "m3", sty=EDGE + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;", points=[(710, 250), (370, 250)]),
        edge("e3", "m3", "m4", "通过", sty=EDGE + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", offset=(0, -22)),
        edge("e4", "m3", "m16", "异常", EDGE_DASH_RED + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(-55, 0)),
        edge("e5", "m4", "m5", sty=EDGE + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", points=[(710, 446), (520, 446), (520, 599)]),
        edge("e6", "m5", "m6", "标准处理", sty=EDGE + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", offset=(0, -24)),
        edge("e7", "m6", "m7", sty=EDGE + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"),
        edge("e8", "m7", "m8", sty=EDGE + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"),
        edge("e9", "m5", "m8", "已有结果", EDGE + "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;", points=[(710, 503), (1760, 503)], offset=(0, -18)),
        edge("e10", "m8", "m9", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("e11", "m9", "m10", sty=EDGE + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;", points=[(2110, 735), (1760, 735)]),
        edge("e12", "m10", "m11", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("e13", "m11", "m12", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("e14", "m12", "m13", sty=EDGE + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;", points=[(2460, 920), (1760, 920)], offset=(-30, 0)),
        edge("e15", "m13", "m14", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("e16", "m14", "m15", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("e17", "m9", "m17", "低置信度 / 角色不确定", EDGE_DASH_RED + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;", points=[(2770, 599), (2770, 1175)], offset=(0, -22)),
        edge("e18", "m7", "m16", "失败 / 超时", EDGE_DASH_RED + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.75;entryY=0;entryDx=0;entryDy=0;", points=[(1410, 1000), (425, 1000)], offset=(0, -20)),
        edge("e19", "m13", "m18", "处理依据", EDGE_DASH_RED + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(55, 0)),
    ]
    return page("01-主流程泳道", "main-flow", cells)


def config_page():
    cells = [text("title2", "配置期与运行期关系", 40, 20)]
    cells += [
        cell("cbox", "配置期：平台预置", "swimlane;startSize=40;fillColor=#FFF8E1;strokeColor=#F9A825;fontSize=18;fontStyle=1;html=1;", 40, 90, 900, 560),
        cell("rbox", "运行期：外部系统自动触发", "swimlane;startSize=40;fillColor=#E8F5E9;strokeColor=#43A047;fontSize=18;fontStyle=1;html=1;", 1080, 90, 900, 560),
    ]
    for id_, val, x, y in [
        ("c1", "场景字典\n场景ID / 子场景ID / 名称", 60, 80),
        ("c2", "规则组绑定\n关键词 / 固定 / 语义 / 智能模型", 340, 80),
        ("c3", "处理链路配置\n标准处理 / 已有结果 / 混合", 620, 80),
        ("c4", "时效与优先级\nT+1 / 1小时 / 高峰排队", 200, 280),
        ("c5", "字段校验要求\n业务单 / 主体 / 原始数据 / 时间戳", 480, 280),
    ]:
        cells.append(vertex(id_, val, "rounded=1", "#FFF3C4", "#F9A825", x, y, 220, 88, "cbox"))
    for id_, val, x, y in [
        ("r1", "业务系统生成请求/数据\n前台 / 渠道 / 系统 / 批处理任务", 60, 80),
        ("r2", "调用接入接口\n携带场景ID和业务元数据", 340, 80),
        ("r3", "自动匹配配置\n加载规则组 / 链路 / 时效", 620, 80),
        ("r4", "自动生成业务任务\n进入主流程处理", 340, 410),
    ]:
        cells.append(vertex(id_, val, "rounded=1", "#C8E6C9", "#43A047", x, y, 230, 92, "rbox"))
    cells += [
        edge("cr1", "c1", "r3", "场景匹配", EDGE_CFG + "exitX=0.5;exitY=0;entryX=0.5;entryY=0;", points=[(210, 140), (1815, 140)], offset=(0, -20)),
        edge("cr2", "c2", "r3", "规则组", EDGE_CFG + "exitX=0.5;exitY=1;entryX=0.75;entryY=1;", points=[(490, 620), (1872.5, 620)], offset=(0, 18)),
        edge("cr3", "c3", "r3", "链路类型", EDGE_CFG + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, 24)),
        edge("rr1", "r1", "r2", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("rr2", "r2", "r3", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("rr3", "r3", "r4", sty=EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", points=[(1815, 360), (1535, 360)]),
    ]
    return page("02-配置期与运行期", "config-runtime", cells)


def field_page():
    cells = [text("title3", "字段与信息流（独立视图）", 40, 20)]
    cells += [
        cell("ibox", "外部系统传入", "swimlane;startSize=40;fillColor=#E1F5FE;strokeColor=#0288D1;fontSize=18;fontStyle=1;html=1;", 40, 90, 560, 680),
        cell("pbox", "平台处理中生成/补充", "swimlane;startSize=40;fillColor=#E8F5E9;strokeColor=#43A047;fontSize=18;fontStyle=1;html=1;", 760, 90, 560, 680),
        cell("obox", "结果与下游使用", "swimlane;startSize=40;fillColor=#E8EAF6;strokeColor=#3949AB;fontSize=18;fontStyle=1;html=1;", 1480, 90, 560, 680),
    ]
    left = [
        ("f1", "场景ID / 子场景ID", 80),
        ("f4", "数据URL / 文件元数据", 190),
        ("f5", "已有处理结果 / 原始数据ID", 300),
        ("f3", "主体角色 / 人员编码 / 组织编码", 410),
        ("f2", "业务单号 / 工单号 / 批次号", 520),
    ]
    middle = [
        ("p1", "场景配置快照", 80),
        ("p2", "处理任务ID / 处理状态", 190),
        ("p3", "标准化数据 / 时间戳 / 置信度", 300),
        ("p4", "channel / subject / role", 410),
        ("p5", "规则版本 / 模型版本 / 配置版本", 520),
    ]
    right = [
        ("o1", "业务任务ID", 80),
        ("o2", "规则命中明细", 190),
        ("o3", "命中证据", 300),
        ("o4", "总体结论 / 风险等级 / 需复核标记", 410),
        ("o5", "报表导出 / 下游同步 / 审计追溯", 520),
    ]
    for id_, val, y in left:
        cells.append(vertex(id_, val, "rounded=1", "#B3E5FC", "#0288D1", 80, y, 260, 70, "ibox"))
    for id_, val, y in middle:
        cells.append(vertex(id_, val, "rounded=1", "#C8E6C9", "#43A047", 80, y, 260, 70, "pbox"))
    for id_, val, y in right:
        cells.append(vertex(id_, val, "rounded=1", "#C5CAE9", "#3949AB", 80, y, 260, 70, "obox"))
    cells += [
        edge("fe1", "f1", "p1", "匹配场景", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -20)),
        edge("fe2", "p1", "o1", "生成任务", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -20)),
        edge("fe3", "f2", "o1", "关联结果", EDGE + "exitX=1;exitY=0.5;entryX=0.5;entryY=0;", points=[(700, 645), (700, 50), (1690, 50)], offset=(0, -20)),
        edge("fe4", "f3", "p4", "映射角色", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, 20)),
        edge("fe6", "f4", "p2", "处理", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -20)),
        edge("fe7", "p2", "p3", "标准化", sty=EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(60, 0)),
        edge("fe8", "f5", "p3", "已有结果", EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, 20)),
        edge("fe9", "p3", "o2", "业务输入", sty=EDGE + "exitX=1;exitY=0.35;entryX=0;entryY=0.25;", points=[(1360, 414.5), (1360, 297.5)], offset=(0, -20)),
        edge("fe10", "p3", "o3", "证据定位", sty=EDGE + "exitX=1;exitY=0.85;entryX=0;entryY=0.5;", points=[(1400, 449.5), (1400, 425)], offset=(0, 20)),
        edge("fe11", "p4", "o2", "角色规则", sty=EDGE + "exitX=1;exitY=0.5;entryX=1;entryY=0.75;", points=[(1160, 535), (1160, 720), (1900, 720), (1900, 332.5)], offset=(0, 20)),
        edge("fe12", "p5", "o5", "审计", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, 20)),
        edge("fe13", "o2", "o4", "汇总", sty=EDGE + "exitX=0.5;exitY=1;entryX=1;entryY=0.5;", points=[(1690, 380), (1850, 380), (1850, 535)], offset=(55, 0)),
        edge("fe14", "o3", "o4", "汇总", sty=EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(-55, 0)),
        edge("fe15", "o4", "o5", "下游使用", sty=EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(55, 0)),
    ]
    return page("03-字段与信息流", "field-flow", cells)


def exception_page():
    cells = [text("title4", "异常分流与补偿", 40, 20)]
    y_top, y_bottom = 120, 390
    xs = [70, 330, 610, 890, 1170, 1450, 1730]
    cells.append(vertex("s0", "主流程步骤", "ellipse", "#E1F5FE", "#0288D1", xs[0], y_top + 25, 140, 76))
    for id_, val, x in [
        ("x1", "入参异常？\n场景不存在 / 业务单缺失 / 主体编码缺失", xs[1]),
        ("x2", "数据异常？\nURL失败 / 格式不支持 / 空数据", xs[2]),
        ("x3", "处理异常？\n超时 / 失败 / 空结果 / 低置信度", xs[3]),
        ("x4", "角色异常？\n渠道缺失 / 主体无法映射", xs[4]),
        ("x5", "规则/模型异常？\n规则组缺失 / 模型超时 / 解析失败", xs[5]),
        ("x6", "输出异常？\n证据定位失败 / 导出失败 / 同步失败", xs[6]),
    ]:
        cells.append(vertex(id_, val, "rhombus", "#FFF3C4", "#F9A825", x, y_top, 220, 126))
    for id_, val, x in [
        ("a1", "阻断进入后续处理\n异常队列\n等待外部系统补字段或修配置", xs[1],),
        ("a2", "重试或补偿\n重新下载 / 重新处理 / 重新调用模型", xs[2],),
        ("a3", "降级继续\n规则/模型异常可降级时\n保留可用规则结果\n标记部分完成", xs[4],),
        ("a4", "人工复核预留\n低置信度 / 角色不确定 / 高风险", xs[5],),
        ("a5", "主结果保存\n输出侧后续补偿", xs[6],),
    ]:
        shape = "ellipse" if id_ == "a5" else "rounded=1"
        cells.append(vertex(id_, val, shape, "#FFCDD2" if id_ != "a5" else "#C5CAE9", "#D32F2F" if id_ != "a5" else "#3949AB", x, y_bottom, 220, 104))
    cells += [
        edge("xe1", "s0", "x1", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        edge("xe2", "x1", "x2", "否", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -22)),
        edge("xe3", "x2", "x3", "否", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -22)),
        edge("xe4", "x3", "x4", "否", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -22)),
        edge("xe5", "x4", "x5", "否", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -22)),
        edge("xe6", "x5", "x6", "否", sty=EDGE + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -22)),
        edge("xe7", "x1", "a1", "是", EDGE_RED + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(40, 0)),
        edge("xe8", "x2", "a2", "是", EDGE_RED + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(40, 0)),
        edge("xe9", "x3", "a2", "失败 / 空文本", EDGE_RED + "exitX=0.25;exitY=1;entryX=0.5;entryY=0;", points=[(945, 310), (720, 310)], offset=(0, -18)),
        edge("xe10", "x3", "a4", "低置信度", EDGE_DASH_RED + "exitX=0.75;exitY=1;entryX=0.25;entryY=0;", points=[(1055, 340), (1505, 340)], offset=(0, -18)),
        edge("xe11", "x4", "a4", "是", EDGE_DASH_RED + "exitX=0.5;exitY=1;entryX=0.75;entryY=0;", points=[(1280, 300), (1615, 300)], offset=(0, 18)),
        edge("xe12", "x5", "a1", "规则缺失", EDGE_RED + "exitX=0.5;exitY=0;entryX=0;entryY=0.5;", points=[(1560, 60), (250, 60), (250, 442)], offset=(0, -18)),
        edge("xe15", "x6", "a5", "是 / 否", EDGE + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", offset=(45, 0)),
        edge("xe16", "a2", "a4", "超过阈值", EDGE_DASH_RED + "exitX=0.5;exitY=1;entryX=0.5;entryY=1;", points=[(720, 650), (1560, 650)], offset=(0, 18)),
        edge("xe17", "a3", "a4", "部分完成", EDGE_DASH_RED + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", offset=(0, -18)),
    ]
    return page("04-异常分流与补偿", "exception-flow", cells)


def build_mxfile():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="drawio" version="30.2.4">\n'
        + "\n".join([main_page(), config_page(), field_page(), exception_page()])
        + "\n</mxfile>\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate a compact generic Chinese swimlane draw.io template."
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=str(DEFAULT_OUT),
        help="Output .drawio path. Defaults to ./business-swimlane-template.drawio.",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_mxfile(), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
