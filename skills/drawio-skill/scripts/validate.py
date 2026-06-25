#!/usr/bin/env python3
"""Deterministic structural linter for .drawio files.

Catches the class of mistakes a vision self-check is slow and unreliable at:
dangling edge endpoints, duplicate or reserved ids, broken parent references,
and (as warnings) off-grid geometry, overlapping sibling nodes, and edge
routing defects. Runs without launching draw.io, so it is a fast pre-check
before the visual review step.

  python3 validate.py diagram.drawio

Edge routing checks (warnings): an edge segment crossing a non-incident leaf
vertex ("routes through vertex"), and two edges crossing each other ("edges X
and Y cross") — the two defects the SKILL.md step-5 self-check looks for
("Edge-shape overlap", "Stacked edges"), but caught here deterministically.

Routing is only knowable from the XML when an edge carries explicit waypoints
(``<Array as="points">``) — exactly the hand-routed case the SKILL.md tells
authors to use to route around shapes. Edges with no waypoints are auto-routed
by draw.io at render time (the path is not stored), so they are NOT geometry-
checked here, keeping these warnings free of false positives. Endpoints honour
``exitX/exitY``/``entryX/entryY`` when present, else the node centre, and
absolute positions are resolved through parent containers.

Exit status is non-zero when any error (or, with --strict, any warning) is
found, so it can gate a workflow. Compressed (non-XML) diagram pages are
skipped with a warning — this skill always writes uncompressed XML.

Usage: python3 validate.py <file.drawio> [--strict]
"""
import argparse
import sys
import xml.etree.ElementTree as ET

RESERVED = {"0", "1"}


def rect(cell):
    """Return (x, y, w, h) floats for a cell's geometry, or None if absent/bad.

    x/y default to 0 when omitted: draw.io treats a missing position as the
    origin, and container-managed children (table rows, swimlane/UML-class
    lines under tableLayout) legitimately omit x/y while keeping width/height.
    Only width/height are required to be present and numeric.
    """
    g = cell.find("mxGeometry")
    if g is None:
        return None
    try:
        return (float(g.get("x", "0")), float(g.get("y", "0")),
                float(g.get("width", "nan")), float(g.get("height", "nan")))
    except ValueError:
        return None


def is_edge_label(cell):
    """True for a draw.io edge label / relative-positioned child vertex.

    These legitimately omit width/height: their position is given relative to a
    parent edge (style ``edgeLabel``) or via ``relative="1"`` geometry. Treating
    them as normal vertices wrongly flags them as missing/invalid geometry.
    """
    if "edgeLabel" in (cell.get("style") or ""):
        return True
    g = cell.find("mxGeometry")
    return g is not None and g.get("relative") == "1"


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


# --- Edge routing geometry -------------------------------------------------
#
# These helpers reason about edge paths. They only apply to edges with explicit
# waypoints (the route is otherwise computed by draw.io at render time and not
# stored in the XML), so the checks never guess an auto-routed path.

def style_num(style, key):
    """Return float value of ``key=`` in a draw.io style string, or None."""
    for part in (style or "").split(";"):
        if part.startswith(key + "="):
            try:
                return float(part.split("=", 1)[1])
            except ValueError:
                return None
    return None


def abs_rect(cell, by_id):
    """Absolute (x, y, w, h) of a vertex, summing parent-container offsets.

    Children of a container use coordinates relative to the container origin, so
    an edge spanning containers needs absolute positions to be compared.
    """
    r = rect(cell)
    if r is None or any(v != v for v in r):
        return None
    x, y, w, h = r
    parent, seen = cell.get("parent"), set()
    while parent and parent in by_id and parent not in seen:
        seen.add(parent)
        p = by_id[parent]
        if p.get("vertex") == "1":
            pr = rect(p)
            if pr and not any(v != v for v in pr):
                x += pr[0]
                y += pr[1]
        parent = p.get("parent")
    return (x, y, w, h)


def endpoint(edge, end, by_id):
    """Absolute (x, y) where ``edge`` meets its source/target vertex.

    Honours exitX/exitY (source) and entryX/entryY (target) if the style pins
    them; otherwise the vertex centre. Returns None if the vertex is unresolved.
    """
    vid = edge.get(end)
    if not vid or vid not in by_id:
        return None
    box = abs_rect(by_id[vid], by_id)
    if box is None:
        return None
    x, y, w, h = box
    style = edge.get("style") or ""
    fx = style_num(style, "exitX" if end == "source" else "entryX")
    fy = style_num(style, "exitY" if end == "source" else "entryY")
    return (x + (fx if fx is not None else 0.5) * w,
            y + (fy if fy is not None else 0.5) * h)


def edge_waypoints(edge):
    """Explicit <Array as="points"> waypoints of an edge as [(x, y), ...]."""
    g = edge.find("mxGeometry")
    if g is None:
        return []
    arr = g.find("Array")
    if arr is None:
        return []
    pts = []
    for pt in arr.findall("mxPoint"):
        px, py = pt.get("x"), pt.get("y")
        if px is not None and py is not None:
            try:
                pts.append((float(px), float(py)))
            except ValueError:
                pass
    return pts


def edge_route(edge, by_id):
    """Absolute polyline [(x, y), ...] for a waypointed edge, or None.

    Returns None when the edge has no explicit waypoints (auto-routed; path
    unknown) or an endpoint cannot be resolved.
    """
    waypoints = edge_waypoints(edge)
    if not waypoints:
        return None
    s, t = endpoint(edge, "source", by_id), endpoint(edge, "target", by_id)
    if s is None or t is None:
        return None
    return [s] + waypoints + [t]


def _orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)


def segments_cross(p1, p2, p3, p4):
    """True if segments p1p2 and p3p4 properly cross (interior intersection).

    Proper crossing only: collinear overlap and shared-endpoint touches return
    False, so edges meeting at a common node or grazing a corner are not flagged.
    """
    o1, o2 = _orient(p1, p2, p3), _orient(p1, p2, p4)
    o3, o4 = _orient(p3, p4, p1), _orient(p3, p4, p2)
    return o1 != o2 and o3 != o4 and 0 not in (o1, o2, o3, o4)


def _point_in_rect(p, box, eps=1e-6):
    x, y, w, h = box
    return x + eps < p[0] < x + w - eps and y + eps < p[1] < y + h - eps


def route_hits_rect(points, box):
    """True if a polyline enters a rectangle's interior or crosses a border."""
    x, y, w, h = box
    corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    borders = list(zip(corners, corners[1:] + corners[:1]))
    for a, b in zip(points, points[1:]):
        if _point_in_rect(a, box) or _point_in_rect(b, box):
            return True
        if any(segments_cross(a, b, c, d) for c, d in borders):
            return True
    return False


def routes_cross(pa, pb):
    """True if any segment of polyline pa properly crosses any of pb."""
    for a1, a2 in zip(pa, pa[1:]):
        for b1, b2 in zip(pb, pb[1:]):
            if segments_cross(a1, a2, b1, b2):
                return True
    return False


def _range_gap(a1, a2, b1, b2):
    alo, ahi = sorted((a1, a2))
    blo, bhi = sorted((b1, b2))
    return max(0, max(alo, blo) - min(ahi, bhi))


def _range_overlap(a1, a2, b1, b2):
    alo, ahi = sorted((a1, a2))
    blo, bhi = sorted((b1, b2))
    return max(0, min(ahi, bhi) - max(alo, blo))


def _axis(a, b):
    if abs(a[0] - b[0]) < 1e-6:
        return "v"
    if abs(a[1] - b[1]) < 1e-6:
        return "h"
    return None


def _close_parallel(a1, a2, b1, b2, min_sep=24, max_gap=24):
    """True when two axis-aligned segments are visually too close/merged."""
    aa, bb = _axis(a1, a2), _axis(b1, b2)
    if aa is None or aa != bb:
        return False
    if aa == "v":
        sep = abs(a1[0] - b1[0])
        overlap = _range_overlap(a1[1], a2[1], b1[1], b2[1])
        gap = _range_gap(a1[1], a2[1], b1[1], b2[1])
    else:
        sep = abs(a1[1] - b1[1])
        overlap = _range_overlap(a1[0], a2[0], b1[0], b2[0])
        gap = _range_gap(a1[0], a2[0], b1[0], b2[0])
    return sep < min_sep and (overlap > 0 or gap < max_gap)


def _opposite_direction(a1, a2, b1, b2):
    da = (a2[0] - a1[0], a2[1] - a1[1])
    db = (b2[0] - b1[0], b2[1] - b1[1])
    return da[0] * db[0] + da[1] * db[1] < 0


def unnecessary_jog_warnings(eid, pts, max_bridge=40):
    """Warn on small U-shaped jogs that can usually be merged away."""
    warns = []
    for i in range(len(pts) - 3):
        a1, a2, b2, c2 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        if _axis(a1, a2) != _axis(b2, c2) or _axis(a1, a2) is None:
            continue
        if _axis(a2, b2) is None:
            continue
        if not _opposite_direction(a1, a2, b2, c2):
            continue
        if _dist(a2, b2) <= max_bridge:
            warns.append(f"edge {eid!r} has a small unnecessary jog near ({a2[0]:g},{a2[1]:g})")
    return warns


def auto_alignment_warnings(edge, by_id, min_delta=3, max_delta=24):
    """Warn when a near-horizontal/vertical auto edge will likely draw a tiny jog.

    Auto-routed edges do not store the rendered path. For adjacent nodes whose
    centers are almost, but not quite, aligned, draw.io commonly renders an
    unnecessary short elbow. Prefer aligning the shapes over accepting the jog.
    """
    if edge_waypoints(edge):
        return []
    style = edge.get("style") or ""
    if any(style_num(style, k) is not None for k in ("exitX", "exitY", "entryX", "entryY")):
        return []
    sid, tid = edge.get("source"), edge.get("target")
    if not sid or not tid or sid not in by_id or tid not in by_id:
        return []
    sb, tb = abs_rect(by_id[sid], by_id), abs_rect(by_id[tid], by_id)
    if not sb or not tb:
        return []
    sc = (sb[0] + sb[2] / 2, sb[1] + sb[3] / 2)
    tc = (tb[0] + tb[2] / 2, tb[1] + tb[3] / 2)
    dx, dy = abs(sc[0] - tc[0]), abs(sc[1] - tc[1])
    eid = edge.get("id")
    if dx > dy * 3 and min_delta <= dy <= max_delta:
        return [f"edge {eid!r} connects nearly horizontal nodes with center-y mismatch {dy:g}px; align shapes to avoid an auto jog"]
    if dy > dx * 3 and min_delta <= dx <= max_delta:
        return [f"edge {eid!r} connects nearly vertical nodes with center-x mismatch {dx:g}px; align shapes to avoid an auto jog"]
    return []


def unpinned_auto_edge_warnings(edge, by_id):
    """Warn on unpinned auto-routed edges between vertices.

    In dense process diagrams, unpinned edges let draw.io choose the side at
    render time. That often causes lines to appear to start inside a node, pick
    the wrong side, or share an endpoint with another edge.
    """
    if edge_waypoints(edge):
        return []
    style = edge.get("style") or ""
    if any(style_num(style, k) is not None for k in ("exitX", "exitY", "entryX", "entryY")):
        return []
    sid, tid = edge.get("source"), edge.get("target")
    if not sid or not tid or sid not in by_id or tid not in by_id:
        return []
    if by_id[sid].get("vertex") == "1" and by_id[tid].get("vertex") == "1":
        return [f"edge {edge.get('id')!r} is auto-routed without pinned exit/entry points"]
    return []


def _side_from_fraction(fx, fy, eps=1e-6):
    """Return the pinned side name implied by exit/entry fractions."""
    if fx is None or fy is None:
        return None
    if abs(fy) < eps:
        return "top"
    if abs(fy - 1) < eps:
        return "bottom"
    if abs(fx) < eps:
        return "left"
    if abs(fx - 1) < eps:
        return "right"
    return None


def _dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _normality_problem(side, endpoint_pt, neighbor_pt, min_len=30, eps=2):
    """Return a short defect string when a segment is not normal to a side."""
    if side in ("top", "bottom"):
        if abs(endpoint_pt[0] - neighbor_pt[0]) > eps:
            return "not vertical"
    elif side in ("left", "right"):
        if abs(endpoint_pt[1] - neighbor_pt[1]) > eps:
            return "not horizontal"
    else:
        return None
    if _dist(endpoint_pt, neighbor_pt) < min_len:
        return f"shorter than {min_len:g}px"
    return None


def endpoint_normality_warnings(edge, by_id):
    """Warnings for first/last segments that do not meet pinned sides cleanly."""
    warns = []
    style = edge.get("style") or ""
    pts = edge_route(edge, by_id)
    sx = style_num(style, "exitX")
    sy = style_num(style, "exitY")
    tx = style_num(style, "entryX")
    ty = style_num(style, "entryY")
    source_side = _side_from_fraction(sx, sy)
    target_side = _side_from_fraction(tx, ty)
    eid = edge.get("id")

    if pts:
        if source_side and len(pts) >= 2:
            problem = _normality_problem(source_side, pts[0], pts[1])
            if problem:
                warns.append(f"edge {eid!r} first segment from {source_side} is {problem}")
        if target_side and len(pts) >= 2:
            problem = _normality_problem(target_side, pts[-1], pts[-2])
            if problem:
                warns.append(f"edge {eid!r} final segment into {target_side} is {problem}")
        return warns

    # Auto-routed non-aligned pinned edges are visually risky in dense swimlanes:
    # draw.io may add a short segment or hug a lane border that is not visible in
    # XML. Require explicit waypoints when a clean normal segment is not obvious.
    source_pt = endpoint(edge, "source", by_id)
    target_pt = endpoint(edge, "target", by_id)
    if source_pt and target_pt:
        if (source_side in ("top", "bottom") or target_side in ("top", "bottom")) and abs(source_pt[0] - target_pt[0]) > 2:
            warns.append(f"edge {eid!r} has pinned top/bottom endpoint(s) but no waypoints to preserve vertical endpoint segments")
        if (source_side in ("left", "right") or target_side in ("left", "right")) and abs(source_pt[1] - target_pt[1]) > 2:
            warns.append(f"edge {eid!r} has pinned left/right endpoint(s) but no waypoints to preserve horizontal endpoint segments")
    return warns


def _segment_near_rect_border(a, b, box, margin=24):
    """True when a horizontal/vertical route hugs a rectangle border."""
    x, y, w, h = box
    x2, y2 = x + w, y + h
    if abs(a[1] - b[1]) < 1e-6:
        yy = a[1]
        lo, hi = sorted((a[0], b[0]))
        if hi <= x or lo >= x2:
            return False
        return abs(yy - y) < margin or abs(yy - y2) < margin
    if abs(a[0] - b[0]) < 1e-6:
        xx = a[0]
        lo, hi = sorted((a[1], b[1]))
        if hi <= y or lo >= y2:
            return False
        return abs(xx - x) < margin or abs(xx - x2) < margin
    return False


def lane_boundary_warnings(cells, ids, routed):
    """Warn when an explicit route travels too close to swimlane borders."""
    lanes = []
    for c in cells:
        if c.get("vertex") == "1" and "swimlane" in (c.get("style") or ""):
            box = abs_rect(c, ids)
            if box:
                lanes.append((c.get("id"), box))
    warns = []
    for eid, pts, _ in routed:
        for a, b in zip(pts, pts[1:]):
            for lid, box in lanes:
                if _segment_near_rect_border(a, b, box):
                    warns.append(f"edge {eid!r} runs too close to swimlane {lid!r} border")
                    break
    return warns


def endpoint_stack_warnings(cells, ids, tol=6):
    """Warn when multiple edges share the same source/target endpoint."""
    buckets = {}
    for c in cells:
        if c.get("edge") != "1":
            continue
        for end in ("source", "target"):
            vid = c.get(end)
            pt = endpoint(c, end, ids)
            if not vid or pt is None:
                continue
            key = (end, vid, round(pt[0] / tol), round(pt[1] / tol))
            buckets.setdefault(key, []).append(c.get("id"))
    warns = []
    for (end, vid, _, _), eids in buckets.items():
        if len(eids) > 1:
            joined = ", ".join(repr(eid) for eid in eids)
            warns.append(f"edges {joined} share the same {end} endpoint on vertex {vid!r}")
    return warns


def _has_dense_vertical_swimlanes(cells):
    return sum(1 for c in cells
               if c.get("vertex") == "1"
               and "swimlane" in (c.get("style") or "")
               and "horizontal=0" in (c.get("style") or "")) >= 3


def geometry_warnings(cells, ids, parents):
    """Edge-through-vertex and edge-crossing warnings for waypointed edges."""
    warns = []
    routed = []          # (edge_id, polyline, {source, target})
    strict_process_routing = _has_dense_vertical_swimlanes(cells)
    for c in cells:
        if c.get("edge") == "1":
            if strict_process_routing:
                warns += unpinned_auto_edge_warnings(c, ids)
            warns += auto_alignment_warnings(c, ids)
            warns += endpoint_normality_warnings(c, ids)
            pts = edge_route(c, ids)
            if pts:
                warns += unnecessary_jog_warnings(c.get("id"), pts)
                routed.append((c.get("id"), pts,
                               {c.get("source"), c.get("target")}))
    # Edge routes through an unrelated leaf vertex (containers wrap children, so
    # an edge legitimately traverses them — restrict to leaves, as overlap does).
    leaves = [(c.get("id"), abs_rect(c, ids)) for c in cells
              if c.get("vertex") == "1" and c.get("id") not in parents
              and not is_edge_label(c)]
    leaves = [(vid, box) for vid, box in leaves if box]
    for eid, pts, ends in routed:
        for vid, box in leaves:
            if vid not in ends and route_hits_rect(pts, box):
                warns.append(f"edge {eid!r} routes through vertex {vid!r}")
    # Edge-edge crossings (both routes known).
    for i in range(len(routed)):
        for j in range(i + 1, len(routed)):
            (ia, pa, _), (ib, pb, _) = routed[i], routed[j]
            if routes_cross(pa, pb):
                warns.append(f"edges {ia!r} and {ib!r} cross")
            for a1, a2 in zip(pa, pa[1:]):
                for b1, b2 in zip(pb, pb[1:]):
                    if _close_parallel(a1, a2, b1, b2):
                        warns.append(f"edges {ia!r} and {ib!r} have parallel segments too close")
                        break
                else:
                    continue
                break
    warns += lane_boundary_warnings(cells, ids, routed)
    if strict_process_routing:
        warns += endpoint_stack_warnings(cells, ids)
    return warns


def check_page(diagram):
    """Return (errors, warnings) for one <diagram> page."""
    name = diagram.get("name", "?")
    model = diagram.find("mxGraphModel")
    if model is None:
        if (diagram.text or "").strip():
            return [], [f"page {name!r}: compressed, skipped (cannot lint)"]
        return [f"page {name!r}: no <mxGraphModel>"], []
    root = model.find("root")
    cells = root.findall("mxCell") if root is not None else []
    errors, warns = [], []
    ids = {}
    for c in cells:
        cid = c.get("id")
        if cid in ids:
            errors.append(f"duplicate id {cid!r}")
        ids[cid] = c
    parents = {c.get("parent") for c in cells}            # ids that have children
    for c in cells:
        cid, parent = c.get("id"), c.get("parent")
        is_v, is_e = c.get("vertex") == "1", c.get("edge") == "1"
        if parent is not None and parent not in ids:
            errors.append(f"cell {cid!r} parent {parent!r} does not exist")
        for end in ("source", "target"):
            ref = c.get(end)
            if ref and ref not in ids:
                errors.append(f"edge {cid!r} {end} {ref!r} does not exist")
        if (is_v or is_e) and cid in RESERVED:
            errors.append(f"cell {cid!r} reuses reserved id 0/1")
        if is_v and not is_edge_label(c):
            r = rect(c)
            if r is None or any(v != v for v in r):       # None or NaN
                errors.append(f"vertex {cid!r} has missing/invalid geometry")
            else:
                x, y, w, h = r
                if w <= 0 or h <= 0:
                    warns.append(f"vertex {cid!r} non-positive size {w:g}x{h:g}")
                if x < 0 or y < 0:
                    warns.append(f"vertex {cid!r} negative position ({x:g},{y:g})")
    # Sibling overlap: only leaf vertices (containers legitimately wrap children).
    boxes = [(c.get("id"), c.get("parent"), rect(c)) for c in cells
             if c.get("vertex") == "1" and c.get("id") not in parents and rect(c)
             and not any(v != v for v in rect(c))]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (ia, pa, ra), (ib, pb, rb) = boxes[i], boxes[j]
            if pa == pb and overlap(ra, rb):
                warns.append(f"vertices {ia!r} and {ib!r} overlap")
    warns += geometry_warnings(cells, ids, parents)
    return errors, warns


def main():
    ap = argparse.ArgumentParser(description="Lint a .drawio file for structural errors.")
    ap.add_argument("file")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failure too")
    args = ap.parse_args()
    try:
        tree = ET.parse(args.file)
    except (ET.ParseError, OSError) as exc:
        sys.exit(f"error: cannot parse {args.file}: {exc}")
    pages = tree.getroot().findall("diagram") or [tree.getroot()]
    errors, warns = [], []
    for page in pages:
        e, w = check_page(page)
        errors += e
        warns += w
    for w in warns:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(errors)} error(s), {len(warns)} warning(s)")
    if errors or (args.strict and warns):
        sys.exit(1)


if __name__ == "__main__":
    main()
