---
name: ide
description: Open an IDE-style preview pane (iTerm2 browser) beside the running agent - file list of the current folder, click to play video/images - and show files, renders or URLs in it with pv. Use when the user says ide, layout IDE, chia khung, preview, xem video bên cạnh, mở trình duyệt trong terminal, or "make the terminal look like an IDE".
---

# ide

Run once from your shell tool, with no arguments:

```bash
ide
```

It keeps your own pane as the main pane and opens an iTerm2 browser pane on the right listing the current folder; clicking a video or image plays it. To show something specific instead, run `pv <file|url|folder>` (for example `pv out/render.mp4` or `pv localhost:3000`); `pvx` closes the pane. Running either again replaces the preview, it never stacks panes. Windows Terminal has no browser pane, so there `ide` does nothing useful.

If `ide` is not found, the user has not run the installer: `git clone https://github.com/cyrus5x89/claude-ide-dragonball && ./claude-ide-dragonball/install.sh` (macOS) or `install.ps1` (Windows).

Never pass an agent name from inside an agent: `ide claude` starts a second agent in your pane.
