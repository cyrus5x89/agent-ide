#!/bin/zsh
# macOS: theme iTerm2 + lệnh `ide` + skill cho Claude Code / Codex / agy
set -e
cd "${0:A:h}"
DP="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
LOCAL="$HOME/.config/claude-ide-dragonball/iterm-local.json"   # phím tắt riêng của máy, không đưa vào repo

command -v uv >/dev/null || { echo "cần uv: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
mkdir -p "$DP" ~/.local/bin
python3 - themes/iterm2/claude-ide.json "$LOCAL" "$DP/claude-ide.json" <<'PY'
import json, os, sys
d = json.load(open(sys.argv[1]))
# hình mờ Claude + ngọc rồng ở góc dưới phải (ảnh nền đen sẵn, khớp màu nền)
d["Profiles"][0].update({"Background Image Location": os.path.abspath("art/dragonball/watermark.png"),
                         "Background Image Mode": 3, "Blend": 1.0})
if os.path.exists(sys.argv[2]):
    d["Profiles"][0].update(json.load(open(sys.argv[2])))
json.dump(d, open(sys.argv[3], "w"), indent=1)
PY
for f in ide ide-tint pv pvx; do ln -sf "$PWD/bin/$f" ~/.local/bin/$f; done
chmod +x bin/ide bin/ide-tint bin/pv

# đặt làm profile mặc định (cửa sổ do CC Switch mở cũng ăn theme) + làm mờ khung không focus
for i in {1..30}; do
  /Applications/iTerm.app/Contents/Resources/utilities/it2 profile list 2>/dev/null | grep -q claude-ide-0001 && break; sleep 0.2
done
uv run --quiet --python 3.14 --with iterm2 python - <<'PY'
import iterm2
async def main(c):
    for p in await iterm2.PartialProfile.async_query(c):
        if p.guid == "claude-ide-0001":
            await p.async_make_default()
iterm2.run_until_complete(main)
PY
defaults write com.googlecode.iterm2 DimInactiveSplitPanes -bool true
defaults write com.googlecode.iterm2 SplitPaneDimmingAmount -float 0.25

if command -v npx >/dev/null; then
  npx --yes skills add "$PWD" --skill ide --agent claude-code codex antigravity-cli -g -y
fi
echo "xong: mở tab mới rồi gõ  ide claude  (hoặc ! ide trong agent đang chạy)"
