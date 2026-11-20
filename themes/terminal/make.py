# Tạo "Claude IDE Dragonball.terminal" cho Terminal.app (cùng bảng màu với theme iTerm2)
# uv run --python 3.14 --with pyobjc-framework-Cocoa python themes/terminal/make.py
import json, pathlib, plistlib
from AppKit import NSColor, NSFont, NSKeyedArchiver

HERE = pathlib.Path(__file__).parent
src = json.load(open(HERE.parent / "iterm2/claude-ide.json"))["Profiles"][0]


def color(c):
    ns = NSColor.colorWithSRGBRed_green_blue_alpha_(c["Red Component"], c["Green Component"], c["Blue Component"], 1.0)
    return bytes(NSKeyedArchiver.archivedDataWithRootObject_requiringSecureCoding_error_(ns, True, None)[0])


names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
p = {"name": "Claude IDE Dragonball", "type": "Window Settings", "ProfileCurrentVersion": 2.07,
     "BackgroundColor": color(src["Background Color"]), "TextColor": color(src["Foreground Color"]),
     "TextBoldColor": color(src["Bold Color"]), "CursorColor": color(src["Cursor Color"]),
     "SelectionColor": color(src["Selection Color"]), "CursorType": 2, "CursorBlink": False,
     "FontAntialias": True, "UseBrightBold": True, "columnCount": 120, "rowCount": 34, "shellExitAction": 1}
for i, n in enumerate(names):
    p[f"ANSI{n}Color"] = color(src[f"Ansi {i} Color"])
    p[f"ANSIBright{n}Color"] = color(src[f"Ansi {i + 8} Color"])
font = NSFont.fontWithName_size_("JetBrainsMonoNFM-Regular", 14) or NSFont.userFixedPitchFontOfSize_(14)
p["Font"] = bytes(NSKeyedArchiver.archivedDataWithRootObject_requiringSecureCoding_error_(font, True, None)[0])
with open(HERE / "Claude IDE Dragonball.terminal", "wb") as fh:
    plistlib.dump(p, fh)
print("ok")
