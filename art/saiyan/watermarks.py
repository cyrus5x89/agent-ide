# Hình mờ góc dưới phải theo agent + effort: art/saiyan/wm/<agent>-<level>.png (ide-tint đặt làm nền khung iTerm)
# python3 art/saiyan/watermarks.py
import pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
OUT = HERE / "wm"
OUT.mkdir(exist_ok=True)
BG = (14, 14, 14)
SRC = {("claude", "low"): HERE / "raw-low.png", ("claude", "max"): HERE / "raw-max.png"}
for agent in ("claude", "codex", "agy"):
    for level in ("low", "medium", "high", "xhigh", "max", "ultracode"):
        img = Image.open(SRC.get((agent, level), HERE / f"web/out/{agent}-{level}.png")).convert("RGB").resize((440, 440), Image.LANCZOS)
        img = Image.blend(Image.new("RGB", img.size, BG), img, 0.2)
        canvas = Image.new("RGB", (1600, 1000), BG)
        canvas.paste(img, (1600 - 440 - 40, 1000 - 440 - 20))
        canvas.save(OUT / f"{agent}-{level}.png", optimize=True)
print("ok", len(list(OUT.glob("*.png"))))
