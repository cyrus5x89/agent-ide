#!/usr/bin/env python3
"""Clawd 'power-up' ladder: one SVG per Claude Code effort level. stdlib only.
Grid: 8 px cells, 32x32 cells in a 256 viewBox. Run: python3 make.py"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
C = 8
ORANGE, ORANGE_D, ORANGE_L, EYE = "#D97757", "#B5583A", "#EE9A7C", "#1A1A1A"
PEC, AB, BELLY, OUTLINE = "#E8906E", "#B85C3E", "#EBA088", "#2A1A14"

def R(x, y, w, h, fill, op=None):
    o = f' opacity="{op}"' if op is not None else ""
    return f'<rect x="{x*C}" y="{y*C}" width="{w*C}" height="{h*C}" fill="{fill}"{o}/>'

# name: body half-width, build, hair, hair tips, hair bottom-row shade, spike height, aura colour, bolts, bolt colour
LEVELS = {
    "low":       (9, "fat",    "#FFE14A", "#FFE14A", "#F2C230", 5,  "#FFE680", 0, None),
    "medium":    (7, "chub",   "#C98A0B", "#E0A21A", "#9A6604", 6,  "#FFC21A", 2, "#9FE8FF"),
    "high":      (7, "muscle", "#FFD84A", "#FFE88A", "#D8A41A", 10, "#FFD23A", 4, "#9FE8FF"),
    "xhigh":     (7, "muscle", "#E8283A", "#FF5A66", "#B3122A", 5,  "#FF4A5A", 4, "#FFB0B8"),
    "max":       (7, "muscle", "#2EC8FF", "#8AE4FF", "#1C8FD6", 5,  "#3AB0FF", 4, "#E0FAFF"),
    "ultracode": (7, "muscle", "#F4F6FA", "#FFFFFF", "#B8BEC8", 5,  "#E8EEFF", 6, "#FFE14D"),
}
TOP, BOT = 15, 25  # body rows [TOP, BOT)

def body(half, build):
    x0, w = 16 - half, half * 2
    s = []
    legs = (11, 13, 18, 20)
    if build in ("fat", "chub"):
        s.append(R(x0 + 1, TOP, w - 2, BOT - TOP, ORANGE))       # rounded: trimmed corners
        s.append(R(x0, TOP + 1, w, BOT - TOP - 2, ORANGE))
        if build == "fat":
            s.append(R(x0 - 1, TOP + 4, w + 2, 4, ORANGE))         # belly overhang
            s.append(R(11, TOP + 5, 10, 5, BELLY))                 # hanging belly patch
            s.append(R(10, TOP + 6, 12, 3, BELLY))
            s.append(R(12, BOT, 8, 1, BELLY))                      # sticks out below the body line
            s.append(R(15, TOP + 7, 2, 1, ORANGE_D))               # belly button
            legs = (9, 11, 20, 22)                                 # legs moved out around the hanging belly
        else:
            s.append(R(14, BOT, 4, 1, ORANGE))                     # 1-cell tummy bump
        xl, xr = x0 - (1 if build == "fat" else 0), x0 + w + (1 if build == "fat" else 0)
        s.append(R(xl - 2, TOP + 4, 2, 2, ORANGE))                 # stubby arms
        s.append(R(xr, TOP + 4, 2, 2, ORANGE))
    else:
        # muscle: shoulders as wide as low's body, narrow waist
        s.append(R(x0 - 2, TOP, w + 4, 4, ORANGE))
        s.append(R(x0 - 1, TOP + 4, w + 2, 1, ORANGE))
        s.append(R(x0, TOP + 5, w, BOT - TOP - 5, ORANGE))
        s.append(R(11, TOP + 3, 3, 2, PEC))                        # pec slabs
        s.append(R(18, TOP + 3, 3, 2, PEC))
        for yy in (TOP + 5, TOP + 7, TOP + 9):                     # 2x3 ab grid
            s.append(R(13, yy, 2, 1, AB)); s.append(R(17, yy, 2, 1, AB))
        ay = TOP + 4
        for sx, d in ((x0 - 6, -1), (x0 + w + 2, 1)):
            s.append(R(sx, ay - 1, 4, 3, ORANGE))                  # upper arm
            s.append(R(sx + 1, ay - 2, 2, 1, ORANGE_L))            # bicep peak
            s.append(R(sx, ay + 1, 4, 1, ORANGE_D))                # underside shade
            fx = sx if d < 0 else sx + 2                           # forearm up at the far end
            s.append(R(fx, ay - 5, 2, 4, ORANGE))
            s.append(R(fx, ay - 6, 2, 1, ORANGE_D))                # fist
    s.append(R(12, TOP + 1, 2, 2, EYE))                            # eyes (the banner notches)
    s.append(R(18, TOP + 1, 2, 2, EYE))
    for lx in legs:
        s.append(R(lx, BOT, 1, 2, ORANGE))
    return s

def hair_cells(half, col, tip, shade, h):
    """{(x, y): colour} for a band on the head plus 5 spikes with 2-cell bases."""
    x0, x1 = 16 - half + 1, 16 + half - 1                          # band [x0, x1)
    cells = {(x, TOP - 1): shade for x in range(x0, x1)}           # bottom row = shade only
    n = 5
    for i in range(n):
        bx = x0 + round(i * (x1 - x0 - 2) / (n - 1))
        hh = h + (1 if i == 2 else 0) - (1 if i in (0, 4) else 0)
        lean = (-1 if i < 2 else 1) if i != 2 else 0
        for k in range(hh):
            ww = 2 if k < hh - 1 else 1
            shift = (k * 2) // 3 if i in (0, 4) else k // 3             # outer spikes lean harder
            xx = bx + lean * shift + (1 if ww == 1 and lean >= 0 else 0)
            for dx in range(ww):
                cells[(xx + dx, TOP - 2 - k)] = tip if k >= hh - 2 else col
        for x in range(bx, bx + 2):                                # fill the gap between band and spike
            cells.setdefault((x, TOP - 1), shade)
    for x in range(x0, x1):                                        # solid hair mass above the band
        cells.setdefault((x, TOP - 2), col)
    return cells

def outline(cells):
    out = set()
    for (x, y) in cells:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            gap = (nx - 1, ny) in cells and (nx + 1, ny) in cells   # 1-cell gap between spikes: leave open
            if (nx, ny) not in cells and ny < TOP and not gap:
                out.add((nx, ny))
    return [R(x, y, 1, 1, OUTLINE) for x, y in sorted(out)]

def bolt(x, y, flip, col):
    d = -1 if flip else 1
    pts = [(x, y), (x + 3*d, y + 2), (x + 1*d, y + 3), (x + 4*d, y + 6)]
    pts = [(min(31, max(1, a)), min(31, max(1, b))) for a, b in pts]  # keep inside 8..248 px
    p = " ".join(f"{a*C},{b*C}" for a, b in pts)
    return (f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="8" '
            f'stroke-linejoin="miter" opacity="0.9"/>'
            f'<polyline points="{p}" fill="none" stroke="#FFFFFF" stroke-width="3"/>')

BOLT_SPOTS = [(1, 5, False), (31, 6, True), (1, 21, False), (31, 22, True), (6, 1, False), (26, 1, True)]

def svg(name):
    half, build, hc, ht, hs, sp, ac, nb, bc = LEVELS[name]
    lvl = list(LEVELS).index(name)
    aop = round(0.25 + lvl * 0.09, 2)                              # 0.25 .. 0.70
    grow = lvl                                                     # flames widen and rise per level
    top = TOP - 2 - sp
    rx = half + 6 + (2 if build == "muscle" else 0) + lvl // 2
    fx0, fx1 = 16 - half - 2 - grow // 2, 16 + half + 2 + grow // 2
    ft = max(1, top - 1 - grow // 2)
    xs = [fx0 + (fx1 - fx0) * j / 8 for j in range(9)]           # tips on even j, dips on odd j
    tips = [ft + 6, None, ft + 2, None, ft, None, ft + 2, None, ft + 6]
    pts = [(fx0 - 1, 27)] + [(x, tips[j] if j % 2 == 0 else top + 6) for j, x in enumerate(xs)] + [(fx1 + 1, 27)]
    flame = " ".join(f"{a*C:.0f},{b*C:.0f}" for a, b in pts)
    aura = (f'<defs><filter id="b" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="8"/></filter>'
            f'<filter id="f" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="3"/></filter></defs>'
            f'<ellipse filter="url(#b)" opacity="{aop}" cx="128" cy="{(top + 27) * C / 2 + 8}" '
            f'rx="{rx * C}" ry="{(27 - top) * C / 2 + 16}" fill="{ac}"/>'
            f'<polygon filter="url(#f)" opacity="{aop}" points="{flame}" fill="{ac}"/>')
    cells = hair_cells(half + (1 if build == "muscle" else 0) - (1 if build == "fat" else 0), hc, ht, hs, sp)
    parts = [aura]
    if name == "ultracode":
        parts += outline(cells)
    parts += body(half, build)
    parts += [R(x, y, 1, 1, c) for (x, y), c in sorted(cells.items())]
    parts += [bolt(x, y, f, bc) for x, y, f in BOLT_SPOTS[:nb]]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" '
            'shape-rendering="crispEdges">' + "".join(parts) + "</svg>\n")

def main():
    names = list(LEVELS)
    rsvg = "/opt/homebrew/bin/rsvg-convert"
    bodies = []
    for n in names:
        txt = svg(n)
        with open(os.path.join(HERE, f"{n}.svg"), "w") as f:
            f.write(txt)
        subprocess.run([rsvg, "-w", "256", "-h", "256", "-o", os.path.join(HERE, f"{n}.png"),
                        os.path.join(HERE, f"{n}.svg")], check=True)
        bodies.append(txt.split(">", 1)[1].rsplit("</svg>", 1)[0])
    def uniq(b, tag):  # filter ids must not collide inside one sheet
        return (b.replace('id="b"', f'id="b{tag}"').replace("url(#b)", f"url(#b{tag})")
                 .replace('id="f"', f'id="f{tag}"').replace("url(#f)", f"url(#f{tag})"))
    # 256px row, label, then 48px and 32px rows as a legibility check
    W, H = 6 * 272 + 16, 256 + 60 + 48 + 16 + 32 + 40
    cells = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
             f'<rect width="{W}" height="{H}" fill="#0E0E0E"/>']
    for i, (n, b) in enumerate(zip(names, bodies)):
        x = 16 + i * 272
        for tag, (sx, sy, sz) in (("L", (x, 16, 256)), ("M", (x + 80, 320, 48)), ("S", (x + 150, 328, 32))):
            cells.append(f'<svg x="{sx}" y="{sy}" width="{sz}" height="{sz}" viewBox="0 0 256 256" '
                         f'shape-rendering="crispEdges">{uniq(b, n + tag)}</svg>')
        cells.append(f'<text x="{x + 128}" y="300" fill="#DDDDDD" font-family="monospace" '
                     f'font-size="22" text-anchor="middle">{n}</text>')
    sp = os.path.join(HERE, "sheet.svg")
    with open(sp, "w") as f:
        f.write("".join(cells) + "</svg>\n")
    subprocess.run([rsvg, "-o", os.path.join(HERE, "sheet.png"), sp], check=True)
    assert all(os.path.getsize(os.path.join(HERE, f"{n}.png")) > 1000 for n in names)

if __name__ == "__main__":
    main()
