# raw-<lv>.png → <lv>.svg (nền trong suốt) + <lv>.png + sheet.png
# uv run --python 3.12 --with vtracer --with pillow --with scipy --with numpy python vectorize.py  (vtracer crash trên 3.14)
import pathlib, subprocess
import vtracer
from body import body_box
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
LEVELS = ["low", "medium", "high", "xhigh", "max", "ultracode"]
# lưới 18x18 ô, mỗi ô 32px. Đo theo THÂN (không tính tóc, hào quang): thân cao bao nhiêu ô, chân thân đứng ở hàng 15
CELL, GRID, FOOT = 32, 18, 15
BODY = {"low": 5, "medium": 5, "high": 6, "xhigh": 6, "max": 6, "ultracode": 6}

for lv in LEVELS:
    raw = HERE / f"raw-{lv}.png"
    if not raw.exists():
        continue
    im = Image.open(raw).convert("RGB")
    w, h = im.size
    # xoá nền bằng flood fill từ 4 góc, để viền đen của nhân vật không bị xoá theo
    mask = im.copy()
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(mask, xy, (255, 0, 255), thresh=40)
    rgba = im.convert("RGBA")
    rgba.putdata([(0, 0, 0, 0) if m == (255, 0, 255) else p for p, m in zip(rgba.getdata(), mask.getdata())])
    # phóng cho thân cao đúng BODY ô, căn giữa theo thân, chân thân ở hàng FOOT
    bx0, by0, bx1, by1 = body_box(im)
    k = BODY[lv] * CELL / (by1 - by0)
    big = rgba.resize((round(w * k), round(h * k)), Image.LANCZOS)
    size = GRID * CELL
    ox, oy = round(size / 2 - (bx0 + bx1) / 2 * k), round(FOOT * CELL - by1 * k)
    rgba = Image.new("RGBA", (size, size))
    rgba.paste(big, (ox, oy), big)
    cut = big.getbbox()
    lost = [n for n, v in (("trái", ox + cut[0] < 0), ("phải", ox + cut[2] > size), ("trên", oy + cut[1] < 0), ("dưới", oy + cut[3] > size)) if v]
    if lost:
        print(f"cảnh báo: {lv} tràn lưới phía {', '.join(lost)}")
    tmp = HERE / f".{lv}.png"
    rgba.save(tmp)
    vtracer.convert_image_to_svg_py(str(tmp), str(HERE / f"{lv}.svg"), colormode="color", hierarchical="stacked",
                                    mode="spline", filter_speckle=6, color_precision=6, layer_difference=24,
                                    corner_threshold=60, length_threshold=4.0, splice_threshold=45, path_precision=2)
    tmp.unlink()
    subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", HERE / f"{lv}.svg", "-o", HERE / f"{lv}.png"], check=True)

done = [lv for lv in LEVELS if (HERE / f"{lv}.svg").exists()]
cells = "".join(f'<image x="{i * 270 + 7}" y="10" width="256" height="256" href="{lv}.svg"/>'
                f'<text x="{i * 270 + 135}" y="292" fill="#CFCAC3" font-family="Menlo" font-size="20" text-anchor="middle">{lv}</text>'
                for i, lv in enumerate(done))
(HERE / "sheet.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{len(done) * 270}" height="310">'
                                f'<rect width="100%" height="100%" fill="#0E0E0E"/>{cells}</svg>')
subprocess.run(["rsvg-convert", HERE / "sheet.svg", "-o", HERE / "sheet.png"], check=True)
step = 256 / GRID
lines = "".join(f'<path d="M{i * 270 + 7 + j * step:.1f} 10v256M{i * 270 + 7} {10 + j * step:.1f}h256"/>'
                for i in range(len(done)) for j in range(GRID + 1))
(HERE / "sheet-grid.svg").write_text((HERE / "sheet.svg").read_text().replace(
    "</svg>", f'<g stroke="#D97757" stroke-opacity=".35" stroke-width=".6" fill="none">{lines}</g></svg>'))
subprocess.run(["rsvg-convert", HERE / "sheet-grid.svg", "-o", HERE / "sheet-grid.png"], check=True)
assert all((HERE / f"{lv}.png").stat().st_size > 1000 for lv in done)
print("ok", done)
