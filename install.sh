#!/bin/zsh
# macOS + iTerm2: theme, màu theo effort, hình mờ, khung preview (cần plugin trình duyệt của iTerm2), lệnh `ide`,
# skill cho Claude Code / Codex / agy
set -e
cd "${0:A:h}"
DP="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
LOCAL="$HOME/.config/claude-ide-dragonball/iterm-local.json"   # phím tắt riêng của máy, không đưa vào repo

[[ -d /Applications/iTerm.app ]] || { echo "cần iTerm2: brew install --cask iterm2"; exit 1; }
command -v uv >/dev/null || { echo "cần uv: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
mkdir -p ~/.local/bin
for f in ide ide-tint pv pvx; do ln -sf "$PWD/bin/$f" ~/.local/bin/$f; done
chmod +x bin/ide bin/ide-tint bin/pv bin/pv-serve

mkdir -p "$DP"
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

# đặt làm profile mặc định (cửa sổ do CC Switch mở cũng ăn theme) + làm mờ khung không focus
for i in {1..30}; do
  /Applications/iTerm.app/Contents/Resources/utilities/it2 profile list 2>/dev/null | grep -q claude-ide-0001 && break; sleep 0.2
done
uv run --quiet --python 3.14 --with iterm2 python - <<'PY' || echo "chưa đặt được profile mặc định: mở iTerm2, bật Settings › General › Magic › Python API rồi chạy lại"
import iterm2
async def main(c):
    for p in await iterm2.PartialProfile.async_query(c):
        if p.guid == "claude-ide-0001":
            await p.async_make_default()
iterm2.run_until_complete(main)
PY
defaults write com.googlecode.iterm2 DimInactiveSplitPanes -bool true
defaults write com.googlecode.iterm2 SplitPaneDimmingAmount -float 0.25

[[ -d ~/Applications/iTermBrowserPlugin.app || -d /Applications/iTermBrowserPlugin.app ]] || echo "
muốn có khung preview: cài plugin trình duyệt của iTerm2. Mở 1 profile kiểu Browser trong iTerm2,
iTerm2 hiện 'Browser Plugin Missing' kèm nút tải. Chưa cài thì ide vẫn chạy agent, chỉ không có preview."

if command -v npx >/dev/null; then
  npx --yes skills add "$PWD" --skill ide --agent claude-code codex antigravity-cli -g -y
fi
echo "xong: mở tab mới rồi gõ  ide claude  (hoặc ! ide trong agent đang chạy)"
