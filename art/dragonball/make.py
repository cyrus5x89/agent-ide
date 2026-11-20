# Claude + 7 viên ngọc rồng: hero.svg (README) và watermark.png (hình mờ góc dưới phải của terminal)
# python3 make.py  (cần rsvg-convert)
import math, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
# mascot Claude Code dựng từ logo chữ khối trong terminal (18x6 ô, mắt là 2 lỗ)
CLAWD = ["...############...", "...##.######.##...", ".################.",
         "...############...", "....#.#....#.#....", ".................."]
# vị trí sao (đơn vị bán kính) cho 1..7 sao
STARS = {1: [(0, 0)], 2: [(-.28, -.15), (.28, .15)], 3: [(0, -.32), (-.3, .2), (.3, .2)],
         4: [(-.28, -.28), (.28, -.28), (-.28, .28), (.28, .28)],
         5: [(0, 0), (-.35, -.3), (.35, -.3), (-.35, .3), (.35, .3)],
         6: [(-.3, -.35), (.3, -.35), (-.42, 0), (.42, 0), (-.3, .35), (.3, .35)],
         7: [(0, 0), (-.3, -.38), (.3, -.38), (-.45, 0), (.45, 0), (-.3, .38), (.3, .38)]}


def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="#D9261C"/>'


def ball(cx, cy, r, n):
    s = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#orb)"/>'
         f'<ellipse cx="{cx - r * .32}" cy="{cy - r * .38}" rx="{r * .28}" ry="{r * .16}" fill="#FFF7D6" opacity=".75" '
         f'transform="rotate(-30 {cx - r * .32} {cy - r * .38})"/>')
    return s + "".join(star(cx + dx * r, cy + dy * r, r * (.32 if n <= 3 else .24 if n <= 5 else .19)) for dx, dy in STARS[n])


def clawd(x, y, cell):
    return "".join(f'<rect x="{x + c * cell}" y="{y + r * cell}" width="{cell}" height="{cell}" fill="#D97757"/>'
                   for r, row in enumerate(CLAWD) for c, ch in enumerate(row) if ch == "#")


def scene(x, y, s):
    # Claude ở giữa, 7 viên ngọc xếp vòng cung phía trên; hộp 600x400 nhân s
    out = clawd(x + 120 * s, y + 230 * s, 20 * s)
    for i in range(7):
        a = math.pi * (1.05 + i * .9 / 6 * 1)
        cx, cy = x + 300 * s + 250 * s * math.cos(a + math.pi * -.0), y + 300 * s + 230 * s * math.sin(a)
        out += ball(round(cx), round(cy), round(34 * s), i + 1)
    return out


DEFS = ('<defs><radialGradient id="orb" cx="38%" cy="32%" r="70%"><stop offset="0" stop-color="#FFE29A"/>'
        '<stop offset=".55" stop-color="#F5A623"/><stop offset="1" stop-color="#B85C00"/></radialGradient></defs>')

(HERE / "hero.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">'
                               f'{DEFS}{scene(0, 0, 1)}</svg>')
(HERE / "watermark.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000">{DEFS}'
                                    f'<rect width="1600" height="1000" fill="#0E0E0E"/>'
                                    f'<g opacity=".16">{scene(1180, 700, .65)}</g></svg>')
for name in ("hero", "watermark"):
    subprocess.run(["rsvg-convert", HERE / f"{name}.svg", "-o", HERE / f"{name}.png"], check=True)
print("ok")
