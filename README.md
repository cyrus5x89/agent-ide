# agent-ide

Biến iTerm2 (macOS) và Windows Terminal thành bố cục kiểu IDE cho các CLI agent: Claude Code, Codex, agy, Gemini, opencode, aider, Copilot, Cursor.

```
┌──────────────┬──────┐
│ agent        │ yazi │
├──────────────┤      │
│ shell        │      │
└──────────────┴──────┘
```

- Theme **Claude IDE**: nền đen ấm `#1F1E1D`, điểm nhấn cam `#D97757`, JetBrains Mono Nerd Font, nền mờ nhẹ + blur, khung không focus tối đi. Được đặt làm profile mặc định, nên cửa sổ do CC Switch mở cũng ăn theme.
- Lệnh `ide`: `ide claude` / `ide codex` / `ide agy` … chia khung rồi chạy agent; `ide` không tham số chỉ chia khung quanh khung đang đứng (trong agent gõ `! ide`). Tab đổi màu theo agent (iTerm2).
- Skill `ide` cho Claude Code, Codex, agy: bảo agent "chia khung IDE" là nó tự chạy `ide`.

## Cài

macOS: `./install.sh` · Windows: `pwsh ./install.ps1`

Cần `uv`, khuyên có `yazi` và JetBrains Mono Nerd Font. Claude Code cũng cài được dạng plugin: `/plugin marketplace add cyrus5x89/agent-ide`.

## Thêm lệnh

Sửa bảng `AGENTS` đầu file `bin/ide` (tên gõ → lệnh, màu tab). `SIDE` / `BOTTOM` đổi lệnh chạy ở cột phải / khung dưới.
