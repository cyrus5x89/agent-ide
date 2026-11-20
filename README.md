# agent-ide

An IDE-style layout and a warm Claude theme for CLI coding agents in iTerm2 (macOS) and Windows Terminal: Claude Code, Codex, Antigravity (agy), Gemini, opencode, aider, Copilot, Cursor.

[Tiếng Việt](README.vi.md)

```
┌──────────────┬──────┐
│ agent        │ yazi │
├──────────────┤      │
│ shell        │      │
└──────────────┴──────┘
```

- **Claude IDE theme**: warm near-black `#1F1E1D`, Claude orange `#D97757`, JetBrains Mono Nerd Font, light blur, unfocused panes dimmed. Set as the default profile, so windows opened by other launchers (CC Switch, etc.) get it too.
- **`ide` command**: splits the current tab, then starts the agent in the main pane. Plain `ide` only splits, so inside a running agent type `! ide`. The tab takes the agent's colour (iTerm2).
- **`ide` skill** for Claude Code, Codex and agy: say "give me the IDE layout" and the agent runs `ide` itself.

## Install

```bash
git clone https://github.com/cyrus5x89/agent-ide && ./agent-ide/install.sh   # macOS
pwsh ./agent-ide/install.ps1                                                  # Windows
```

Needs `uv`; `yazi` and JetBrains Mono Nerd Font recommended. Claude Code plugin (skill only, no theme or `ide` command):

```
/plugin marketplace add cyrus5x89/agent-ide
/plugin install agent-ide@agent-ide
```

## Presets

Anything after the preset is passed to the agent, e.g. `ide ccy --model opus` or `ide cx -m gpt-6.1`. Full list: `ide --help`.

| Type | Runs | What it does |
|---|---|---|
| `ide claude` | `claude` | Claude Code, asks before risky actions |
| `ide cc` | `claude` | same as claude |
| `ide ccy` | `claude --dangerously-skip-permissions` | never asks; full trust, use in repos you can reset |
| `ide cca` | `claude --permission-mode auto` | auto mode: a classifier approves safe actions, asks on risky ones |
| `ide cce` | `claude --permission-mode acceptEdits` | auto-accept file edits, still asks for shell commands |
| `ide ccp` | `claude --permission-mode plan` | plan mode: reads and plans, changes nothing until you approve |
| `ide ccc` | `claude --continue` | continue the last conversation in this folder |
| `ide ccr` | `claude --resume` | pick an older conversation to resume |
| `ide ccw` | `claude --worktree` | work in a fresh git worktree, your branch stays clean |
| `ide codex` | `codex` | Codex CLI, default approvals |
| `ide cx` | `codex` | same as codex |
| `ide cxa` | `codex --approve-for-me` | auto-review approvals inside the workspace sandbox |
| `ide cxy` | `codex --dangerously-bypass-approvals-and-sandbox` | no approvals and no sandbox; full trust |
| `ide cxr` | `codex resume --last` | continue the last Codex session |
| `ide agy` | `agy` | Antigravity CLI |
| `ide agyy` | `agy --dangerously-skip-permissions` | Antigravity, auto-approve every tool |
| `ide agyc` | `agy --continue` | continue the last Antigravity conversation |
| `ide gemini` | `gemini` | Gemini CLI |
| `ide opencode` | `opencode` | opencode |
| `ide aider` | `aider` | aider |
| `ide copilot` | `copilot` | GitHub Copilot CLI |
| `ide cursor` | `cursor-agent` | Cursor agent CLI |

**Which permission mode?** Start with `ccp` (plan) to read an unfamiliar repo, `cca` or `cce` for everyday work, and `ccy` / `cxy` / `agyy` only where nothing can hurt you: a fresh worktree (`ccw`), a container, or a repo you can `git reset`. Those three skip every confirmation, including deletes and pushes.

## Customise

Edit the `AGENTS` table at the top of `bin/ide`: `name: (command, tab colour, English note, Vietnamese note)`. `SIDE` and `BOTTOM` set what runs in the right column and the bottom pane.
