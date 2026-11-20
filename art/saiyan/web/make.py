# prompts.html: prompt + ảnh mẫu để tạo tay trên chatgpt.com/images (Claude, Codex/GPT, agy)
# python3 make.py
import html, pathlib

HERE = pathlib.Path(__file__).parent
STYLE = ("2D anime power-up illustration, thick clean black outlines, flat cel shading with 2-3 tones, no gradients on the body, "
         "centred, full body, facing the viewer, fierce determined look. Plain flat solid #0E0E0E background, nothing else, "
         "no text, no human, no existing anime character. Square 1:1 with margin around the figure.")
HAIR = ("The hair is a big anime power-up hairdo covering the WHOLE top of the head edge to edge - 6 to 8 thick sharp spikes "
        "fanning upward and outward, darker shade side and lighter highlight side; never a small tuft or a crown.")
KEEP = ("Keep the creature's body EXACTLY as in the attached image: same body, muscles, arms, legs, eyes, black outline, size "
        "and position. Change ONLY the hair and the effects described here. Keep the plain flat #0E0E0E background and the same style.")
LEVEL = {
    "low": "FAT and simply ROUND body, one even colour, no belly patch. Short spiky GOLDEN-YELLOW hair. A calm thin golden outline glow. No lightning.",
    "medium": "Hair: sharper spiky hair in a DEEP DARK GOLD. Effects: only a thin golden outline glow and 2-3 tiny blue-white electric sparks near the hair. No flames.",
    "high": "Hair: very LONG golden-yellow spiky mane flowing down behind the body almost to the ground, no eyebrows. Effects: only a thin golden outline glow and 4-5 small yellow electric sparks. Restrained.",
    "xhigh": "Hair: SHORT spiky CRIMSON RED hair. Effects: a soft red-orange divine flame aura and a few red embers floating.",
    "max": "Hair: SHORT upright spiky bright CYAN-BLUE hair. Effects: a sharp blue flame aura with a white core and glowing blue sparkles.",
    "ultracode": "Hair: SHORT spiky SILVER-WHITE hair; eyes glow silver-white. Effects: a tall silvery-white and pale blue flame aura with floating light particles, calm and god-like, the most radiant of all.",
}
CHAR = {
    "Codex (GPT)": ("a small charcoal-black rounded cube creature whose face is a glowing white terminal prompt '>_' (the '>' and '_' are its eyes "
                    "and mouth), tiny stubby arms sticking out left and right, four tiny square legs, a thin teal (#10A37F) rim light"),
    "agy (Antigravity)": ("a small Google-blue (#4285F4) sphere creature that floats a little above the ground (anti-gravity), two white oval eyes, "
                          "a thin orbiting ring around its middle, tiny stubby arms, no legs, a soft shadow below it"),
}

cards = []


def card(title, refs, text):
    imgs = "".join(f'<img src="{r}" title="{r}">' if r.endswith(".png") else f'<span>{r}</span>' for r in refs)
    cards.append(f'<section><h3>{html.escape(title)}</h3><div class=refs>{imgs or "<i>không cần ảnh</i>"}</div>'
                 f'<pre>{html.escape(text)}</pre><button onclick="navigator.clipboard.writeText(this.previousSibling.innerText);'
                 f'this.textContent=\'đã copy\'">copy prompt</button></section>')


# Claude: 4 cấp còn thiếu, sửa trên ảnh thân có sẵn
cards.append("<h2>1. Claude - sửa trên ảnh (đính kèm đúng ảnh trong ô)</h2>")
for lv, ref in [("medium", "3-than-gay.png"), ("high", "2-than-max.png"), ("xhigh", "2-than-max.png"), ("ultracode", "2-than-max.png")]:
    card(f"Claude · {lv}", [ref], f"{KEEP} {LEVEL[lv]}")

for i, (name, desc) in enumerate(CHAR.items(), 2):
    cards.append(f"<h2>{i}. {name} - tạo nhân vật trước, rồi 6 cấp</h2>")
    card(f"{name} · nhân vật gốc", ["4-mau-low.png"],
         f"Design an original mascot: {desc}. No hair yet, standing calmly. Match the drawing style of the attached image "
         f"(outline weight, cel shading, background) but NOT its character. {STYLE}")
    for lv in LEVEL:
        body = {"low": "Make the body FAT and round.", "medium": "Make the body lean and toned with subtle muscles.",
                }.get(lv, "Make the body HEAVILY MUSCULAR - big pecs, six-pack, bulging arms.")
        card(f"{name} · {lv}", ["(ảnh nhân vật gốc vừa tạo)", "5-mau-max.png" if lv != "low" else "4-mau-low.png"],
             f"Image 1 is the mascot, Image 2 is a style reference for the power-up look only. Draw the mascot from Image 1 "
             f"powering up, same face and colours. {body} {HAIR} {LEVEL[lv]} {STYLE}")

(HERE / "prompts.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Prompt ngọc rồng</title><style>
body{{background:#0E0E0E;color:#E8E6E3;font:13px -apple-system,system-ui;max-width:900px;margin:0 auto;padding:16px}}
h1{{font-size:26px}}h2{{color:#E08A6D;font-size:20px;margin:28px 0 8px}}h3{{margin:0 0 6px;font-size:16px}}
section{{background:#1A1918;border-radius:8px;padding:12px;margin:10px 0}}
.refs{{display:flex;gap:8px;margin-bottom:8px;color:#B5AFA8}}.refs img{{height:90px;border-radius:4px;background:#000}}
pre{{white-space:pre-wrap;background:#0E0E0E;padding:10px;border-radius:6px;margin:0 0 8px}}
button{{background:#D97757;color:#0E0E0E;border:0;border-radius:6px;padding:6px 12px;font-weight:600;cursor:pointer}}
</style><h1>Prompt + ảnh mẫu cho chatgpt.com/images</h1>
<p>Kéo ảnh trong thư mục này vào ô chat, dán prompt. Tên ảnh ghi trong từng ô. Tạo xong lưu về <code>art/saiyan/web/out/</code> đặt tên kiểu <code>claude-medium.png</code>, <code>codex-max.png</code>.</p>
{''.join(cards)}""")
print("ok", len(cards))
