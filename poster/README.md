No problem – let me provide the **README.md** content that reflects the change (posts stored in `./posts` folder). I'll keep it concise and focused.

---

# Automated Bluesky Post Scheduler

Automates posting scheduled Markdown content to a local web app (Bluesky thread splitter/poster).  
Scans `./posts/` for `.md` files, schedules unscheduled ones into `posts.csv` (one per day), then posts today's scheduled content.

## Features

- 📅 Reads schedule from `posts.csv` (format: `post,time` with `time` as `YYYYMMDDHHMM`).
- 🤖 Automatically schedules new `.md` files from `./posts/` into the next available daily slots (Mon–Sun).
- 🔁 Idempotent – never reposts the same file (uses `posted.log`).
- 🔐 Bluesky credentials from environment variables (no hardcoding).
- 🌐 Automates `http://localhost:3000/` login, paste, Split, Post.
- 📸 Takes a screenshot on failure for debugging.

## Prerequisites

- Python 3.8+
- Playwright (`pip install playwright && playwright install chromium`)
- Local web app running at `http://localhost:3000/` with:
  - Login: `<input id="username">`, `<input id="appPassword">`, submit button
  - Post area: `<textarea id="content">`, `<button id="splitButton">`, `<button id="postButton">`

## Installation

1. Save the script as `auto_post.py` (or `auto_post_scheduler.py`).
2. Install dependencies:
   ```bash
   pip install playwright
   playwright install chromium
   ```
3. Create a folder named `posts` in the same directory as the script – this is where your `.md` post files go.
4. Set environment variables (see below).

## Configuration

### 1. Environment Variables (Bluesky credentials)

| Variable            | Description                                 |
|---------------------|---------------------------------------------|
| `BSKY_USERNAME`     | Your Bluesky handle (e.g., `user.bsky.social`) |
| `BSKY_APP_PASSWORD` | An [app password](https://bsky.app/settings/app-passwords) |

**Set them permanently** (choose one method):

#### Linux / macOS (`~/.bashrc`, `~/.zshrc`, or `~/.profile`)
```bash
export BSKY_USERNAME="your.handle.bsky.social"
export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```
Then `source ~/.bashrc`.

#### Windows (Command Prompt – persistent)
```cmd
setx BSKY_USERNAME "your.handle.bsky.social"
setx BSKY_APP_PASSWORD "xxxx-xxxx-xxxx-xxxx"
```
Restart terminal.

#### Windows (PowerShell – persistent)
```powershell
[Environment]::SetEnvironmentVariable("BSKY_USERNAME", "your.handle.bsky.social", "User")
[Environment]::SetEnvironmentVariable("BSKY_APP_PASSWORD", "xxxx-xxxx-xxxx-xxxx", "User")
```

#### Temporary (any OS – for testing)
```bash
export BSKY_USERNAME="your.handle.bsky.social"
export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
python auto_post.py
```

### 2. CSV Schedule File (`posts.csv`)

The script creates `posts.csv` automatically if missing. It contains rows like:

```csv
post,time
2026-04-06-post.md,202604061100
2026-04-07-another.md,202604071100
```

- `post`: filename of the Markdown file (must be inside `./posts/`).
- `time`: scheduled date and time in `YYYYMMDDHHMM`. Only the **date part** is compared to today.

### 3. Markdown Files (in `./posts/`)

Place all your `.md` post files inside the `posts` folder (created automatically if missing).

**Why?**  
- Prevents accidentally scheduling `README.md` or other Markdown files in the root directory.
- Keeps your posts organised.

Example structure:
```
your-project/
├── auto_post.py
├── posts.csv
├── posted.log          (created automatically)
└── posts/
    ├── 2026-04-06-first-post.md
    ├── 2026-04-07-second.md
    └── ...
```

## Automatic Scheduling of New Posts

Every time the script runs, it:

1. Scans `./posts/*.md` for files **not yet listed** in `posts.csv`.
2. For each unscheduled file, it finds the **next free day** (starting from tomorrow) that has no scheduled post.
3. Appends a new row to `posts.csv` with the default hour **11:00** (configurable).
4. Then proceeds to post today’s scheduled content (if any).

**Example**  
Today is April 6. `posts.csv` already has a post for April 6. You add two new files to `./posts/`.  
Running the script will schedule them on April 7 and April 8 (both at 11:00), then post the April 6 content.

### Customising the default hour

Edit the script variable:
```python
DEFAULT_POST_HOUR = 1100   # 11:00 AM (24‑hour format: 1430 = 2:30 PM)
```

## Usage

Run manually:
```bash
python auto_post.py
```

### Scheduling with cron (Linux/macOS)

Run every 10 minutes:
```cron
*/10 * * * * cd /path/to/script && python auto_post.py >> auto_post.log 2>&1
```

### Windows Task Scheduler

- Trigger: Daily, repeat every 10 minutes.
- Action: Start `python` with argument `auto_post.py`, start in script directory.

## Troubleshooting

| Problem                                   | Solution                                                                          |
|-------------------------------------------|-----------------------------------------------------------------------------------|
| `ERROR: Please set BSKY_USERNAME...`      | Environment variables not set – see Configuration.                               |
| `No .md files found in './posts'`         | Create the `posts` folder and put your `.md` files there.                        |
| `ERROR: Markdown file ... not found`      | The file listed in `posts.csv` is not inside `./posts/`. Move it there.          |
| Timeout waiting for `#username`           | Web app not running at `http://localhost:3000/` or login page differs.           |
| `No success indicator found`              | Success message uses a different CSS class – update the selector in the script.  |
| Script works manually but not in cron     | Use absolute paths in cron and load environment variables (e.g., `source ~/.profile` before the command). |

## Security Notes

- App password is stored only in environment variables – never in the script.
- `posted.log` and `error_screenshot.png` are created locally – do not commit them to version control.
- On shared servers, restrict permissions: `chmod 600 auto_post.py`.

## License

GPLv3