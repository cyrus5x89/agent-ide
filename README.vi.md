# agent-ide

Bố cục kiểu IDE và theme Claude tông ấm cho các CLI agent trên iTerm2 (macOS) và Windows Terminal: Claude Code, Codex, Antigravity (agy), Gemini, opencode, aider, Copilot, Cursor.

[English](README.md)

```
┌──────────────┬──────┐
│ agent        │ yazi │
├──────────────┤      │
│ shell        │      │
└──────────────┴──────┘
```

- **Theme Claude IDE**: nền đen ấm `#1F1E1D`, cam Claude `#D97757`, font JetBrains Mono Nerd, nền mờ nhẹ, khung không dùng thì tối đi. Đặt làm profile mặc định nên cửa sổ do CC Switch hay app khác mở cũng có theme.
- **Lệnh `ide`**: chia tab đang đứng rồi chạy agent ở khung chính. Gõ `ide` không kèm gì thì chỉ chia khung, nên trong agent đang chạy gõ `! ide`. Tab đổi màu theo agent (iTerm2).
- **Skill `ide`** cho Claude Code, Codex, agy: nói "chia khung IDE" là agent tự chạy `ide`.

## Cài

```bash
git clone https://github.com/cyrus5x89/agent-ide && ./agent-ide/install.sh   # macOS
pwsh ./agent-ide/install.ps1                                                  # Windows
```

Cần `uv`; nên có `yazi` và font JetBrains Mono Nerd. Plugin Claude Code (chỉ có skill, không có theme và lệnh `ide`):

```
/plugin marketplace add cyrus5x89/agent-ide
/plugin install agent-ide@agent-ide
```

## Lệnh có sẵn

Gõ thêm gì sau tên lệnh thì được chuyển thẳng cho agent, ví dụ `ide ccy --model opus` hay `ide cx -m gpt-6.1`. Xem hết: `ide --help vi`.

| Gõ | Chạy | Làm gì |
|---|---|---|
| `ide claude` | `claude` | Claude Code, hỏi trước khi làm việc rủi ro |
| `ide cc` | `claude` | giống claude |
| `ide ccy` | `claude --dangerously-skip-permissions` | không hỏi gì cả; chỉ dùng ở repo khôi phục được |
| `ide cca` | `claude --permission-mode auto` | tự duyệt việc an toàn, vẫn hỏi việc nguy hiểm |
| `ide cce` | `claude --permission-mode acceptEdits` | tự nhận sửa file, lệnh shell vẫn hỏi |
| `ide ccp` | `claude --permission-mode plan` | chỉ đọc và lên kế hoạch, duyệt rồi mới sửa |
| `ide ccc` | `claude --continue` | tiếp cuộc trò chuyện gần nhất ở thư mục này |
| `ide ccr` | `claude --resume` | chọn cuộc trò chuyện cũ để mở lại |
| `ide ccw` | `claude --worktree` | làm trong git worktree mới, nhánh đang dùng không bị đụng |
| `ide codex` | `codex` | Codex CLI, duyệt mặc định |
| `ide cx` | `codex` | giống codex |
| `ide cxa` | `codex --approve-for-me` | tự duyệt trong sandbox của thư mục làm việc |
| `ide cxy` | `codex --dangerously-bypass-approvals-and-sandbox` | không hỏi, không sandbox; tin hoàn toàn |
| `ide cxr` | `codex resume --last` | tiếp phiên Codex gần nhất |
| `ide agy` | `agy` | Antigravity CLI |
| `ide agyy` | `agy --dangerously-skip-permissions` | Antigravity, tự duyệt mọi công cụ |
| `ide agyc` | `agy --continue` | tiếp cuộc trò chuyện agy gần nhất |
| `ide gemini` | `gemini` | Gemini CLI |
| `ide opencode` | `opencode` | opencode |
| `ide aider` | `aider` | aider |
| `ide copilot` | `copilot` | GitHub Copilot CLI |
| `ide cursor` | `cursor-agent` | Cursor agent CLI |

**Chọn chế độ quyền nào?** Repo lạ thì mở `ccp` (chỉ lên kế hoạch) để đọc trước. Làm việc hằng ngày thì `cca` hoặc `cce`. `ccy` / `cxy` / `agyy` chỉ dùng ở chỗ hỏng cũng không sao: worktree mới (`ccw`), container, hoặc repo `git reset` lại được. Ba lệnh này bỏ qua mọi bước xác nhận, kể cả xoá file và push.

## Tuỳ chỉnh

Sửa bảng `AGENTS` đầu file `bin/ide`: `tên: (lệnh, màu tab, ghi chú tiếng Anh, ghi chú tiếng Việt)`. `SIDE` và `BOTTOM` là lệnh chạy ở cột phải và khung dưới.
