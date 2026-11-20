---
name: ide
description: Split the current iTerm2 or Windows Terminal tab into an IDE layout around the running agent - agent pane, file explorer (yazi) on the right, a shell below. Use when the user says ide, layout IDE, chia khung, mở file explorer bên cạnh, or "make the terminal look like an IDE".
---

# ide

Run once from your shell tool, with no arguments:

```bash
ide
```

It keeps your own pane as the main pane, adds yazi on the right and an empty shell below, both in the current directory. If the tab is already split in iTerm2, it does nothing. In Windows Terminal it splits again on every call, so check with the user before running it twice.

If `ide` is not found, the user has not run the installer: `git clone https://github.com/cyrus5x89/agent-ide && ./agent-ide/install.sh` (macOS) or `install.ps1` (Windows).

Never pass an agent name from inside an agent: `ide claude` starts a second agent in your pane.
