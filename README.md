# Job Radar on Claude Code — setup guide

This folder is your complete Job Radar project: the agent instructions, your 32 tracked vacancies, a local dashboard and the weekly run scripts. Everything runs on your own computer with Claude Code.

## What's in the folder

| Path | What it is |
|---|---|
| `CLAUDE.md` | Your profile, rules and the liveness lessons. Claude Code reads it automatically. |
| `.claude/skills/job-radar/SKILL.md` | The sweep itself. Start it with `/job-radar`. |
| `.claude/agents/ad-reader.md` | A helper that reads job pages (several run in parallel). |
| `.claude/settings.json` | Pre-approves web search, page reading, file edits and Python, so runs don't stop for permission. |
| `data/jobs.json` | Your tracker data (exported 18 Nov 2026). |
| `data/runs.json` | Run history. |
| `scripts/render.py` | Builds `tracker.html` from the data. |
| `scripts/validate.py` | Checks the data for mistakes. |
| `tracker.html` | Your dashboard. Double-click to open in a browser. |
| `run-weekly.sh` / `run-weekly.ps1` | Weekly run for macOS / Windows. |

## What to download

1. **Claude Code** (needs a Pro, Max, Team or Enterprise plan; the free plan doesn't include it).
   - macOS: open Terminal and run `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows: open PowerShell and run `irm https://claude.ai/install.ps1 | iex`
   - Optional on Windows: Git for Windows (https://git-scm.com/download/win), which Claude Code uses as its shell if present.
2. **Python 3** for the two small scripts.
   - macOS: usually already there. Check with `python3 --version`; if missing, install from https://www.python.org/downloads/
   - Windows: install from https://www.python.org/downloads/ and tick "Add python.exe to PATH" during setup.
3. **This folder.** Unzip it somewhere permanent, for example `Documents/job-radar`.

## Steps

1. **Check the install.** Open a new terminal and run `claude --version`.
2. **Open the project.** In the terminal: `cd ~/Documents/job-radar` (Windows: `cd $HOME\Documents\job-radar`), then run `claude`. The first time, a browser window asks you to log in with your Claude account. If asked whether to trust the folder, say yes.
3. **Windows only:** Python is called `python` or `py` there, not `python3`. Tell Claude once: "On this computer use `python` instead of `python3`", or edit the two mentions in `CLAUDE.md` and `SKILL.md`.
4. **First run, by hand.** Type `/job-radar recheck`. This re-verifies all 32 roles without searching for new ones, and it's a good test. Then type `/job-radar` for a full run.
5. **Open the dashboard.** Double-click `tracker.html`. The "Open" view hides closed roles.
6. **Change a status** by telling Claude, for example: "mark sportalliance-sf-admin-ba as Applied". Every card shows its id.
7. **Schedule it weekly** (choose one):
   - **Claude desktop app:** if you use it, its scheduled tasks can run on your computer. Create a weekly task that opens this folder with the prompt `/job-radar`. The computer has to be on and awake at that time.
   - **macOS cron:** run `chmod +x run-weekly.sh` once, then `crontab -e` and add this line (Thursday 07:10; change the path to yours):
     `10 7 * * 4 /bin/bash "$HOME/Documents/job-radar/run-weekly.sh"`
     A desktop notification appears when it finishes, and the log goes to `logs/`.
   - **Windows Task Scheduler:** Create Basic Task → Weekly, Thursday 07:10 → Start a program → program `powershell.exe`, arguments `-ExecutionPolicy Bypass -File "C:\Users\<you>\Documents\job-radar\run-weekly.ps1"`. A message box appears when it finishes.
   - Test the script once by hand before relying on the schedule.
8. **Turn off the old cloud task.** Once a local run works, disable "Job Radar weekly sweep" in the Claude app's scheduled tasks, so both don't run.

## Good to know

- Your computer must be on for scheduled runs. If it was asleep, run `/job-radar` by hand.
- You won't get phone push notifications any more. The notification appears on your computer instead.
- The old claude.ai tracker page stops updating once the cloud task is off. `tracker.html` replaces it.
- Memory from the Claude app doesn't carry over to Claude Code. Everything the agent needs about you is in `CLAUDE.md`, so update it when something changes (a new certificate, Polish level, new applications).
- Claude can't read LinkedIn or pracuj.pl pages; roles from there stay "unverified" until you check them yourself.
- Each run uses your plan's usage. A full sweep reads 30–60 pages; `/job-radar recheck` is lighter.
