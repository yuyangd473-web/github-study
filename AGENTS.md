# AGENTS.md

Personal learning repo for Git/Python (owner `dyy`). Treat it as a simple study project, not a production app.

## Layout

- `python/calculator.py` — the real program: an interactive Chinese-language CLI calculator.
- `python/计算器获取数字部分.py` — a scratch/learning snippet (number-input helpers). Not part of the app.
- `python/src/python/__init__.py` — unrelated scaffolding stub (prints "Hello from python!"); ignore it.
- `tatus` — stray committed file containing `git log` output with ANSI codes. Not source; don't edit it.

## Tooling

- Managed by `uv`; Python **3.14** required (`python/.python-version`, `requires-python = ">=3.14"`).
- No tests, linter, typecheck, or CI config.
- `[tool.uv] package = false`; `[project.scripts] python = "python:main"` is misleading/unused.

## Commands

Run from `python/`:

```bash
uv run python calculator.py
```

The program is interactive (reads stdin); there is no non-interactive entrypoint.

## Packaging (Windows .exe)

- PyInstaller is a dev dependency group (`uv run pyinstaller ...`).
- `calculator.spec`, `build/`, `dist/`, `.venv/` are **not tracked** (`.gitignore` ignores `*.spec`, `build/`, `dist/`). The README references `dist/calculator.exe`, but it does not exist in a fresh clone.
- To rebuild, generate the spec first: `uv run pyinstaller calculator.py` (then `uv run pyinstaller calculator.spec`).

## Conventions / gotchas

- UI strings, prompts, and comments are in Chinese; source filenames may contain Chinese characters (use quotes/UTF-8-safe tooling on Windows).
- Branch `main` is primary; `study` is an older stale branch.
- Commit messages are short one-liners, often referencing the README (learning-journal style).
