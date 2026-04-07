#!/usr/bin/env python3
import asyncio
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

from playwright.async_api import async_playwright

# ==================== CONFIGURATION ====================
CSV_PATH = Path("posts.csv")
POSTS_DIR = Path("./posts")               # directory containing .md files
LOCAL_URL = "http://localhost:3000/"
DEFAULT_POST_HOUR = 1100            # HHMM format, e.g., 1100 = 11:00

# Credentials from environment variables
USERNAME = os.getenv("BSKY_USERNAME")
APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

# For idempotency: keep track of already posted files
POSTED_LOG = Path("posted.log")

# ==================== VALIDATION ====================
if not USERNAME or not APP_PASSWORD:
    print("ERROR: Please set BSKY_USERNAME and BSKY_APP_PASSWORD environment variables.")
    sys.exit(1)

# ==================== HELPER FUNCTIONS ====================
def already_posted(filename: str) -> bool:
    """Return True if this post has been successfully posted before."""
    if not POSTED_LOG.exists():
        return False
    with open(POSTED_LOG, "r") as f:
        return filename.strip() in {line.strip() for line in f}

def mark_posted(filename: str) -> None:
    """Record that a post has been successfully published."""
    with open(POSTED_LOG, "a") as f:
        f.write(f"{filename}\n")

def get_scheduled_dates() -> set[str]:
    """Return a set of dates (YYYYMMDD) that already have a scheduled post in posts.csv."""
    dates = set()
    if not CSV_PATH.exists():
        return dates
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                time_str = row.get("time", "").strip()
                if time_str and len(time_str) >= 8:
                    dates.add(time_str[:8])
    except Exception as e:
        print(f"WARNING: Could not read CSV for scheduling: {e}")
    return dates

def get_scheduled_filenames() -> set[str]:
    """Return a set of filenames already listed in posts.csv."""
    filenames = set()
    if not CSV_PATH.exists():
        return filenames
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                post_file = row.get("post", "").strip()
                if post_file:
                    filenames.add(post_file)
    except Exception as e:
        print(f"WARNING: Could not read CSV for filename check: {e}")
    return filenames

def append_schedule(filename: str, date_yyyymmdd: str) -> None:
    """Append a new row to posts.csv with the given date and DEFAULT_POST_HOUR."""
    time_str = f"{date_yyyymmdd}{DEFAULT_POST_HOUR:04d}"
    file_exists = CSV_PATH.exists()
    try:
        with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["post", "time"])
            writer.writerow([filename, time_str])
        print(f"Scheduled {filename} on {date_yyyymmdd} at {DEFAULT_POST_HOUR//100:02d}:{DEFAULT_POST_HOUR%100:02d}")
    except Exception as e:
        print(f"ERROR: Could not append to CSV: {e}")

def schedule_unscheduled_md_files() -> None:
    """
    Scan POSTS_DIR for .md files. For each file not already in posts.csv,
    assign the next available day (starting from tomorrow) that is not already
    occupied by a scheduled post. Append to posts.csv.
    """
    # Get all .md files in POSTS_DIR
    md_files = {f.name for f in POSTS_DIR.glob("*.md") if f.is_file()}
    if not md_files:
        print("No .md files found. Nothing to schedule.")
        return

    scheduled_filenames = get_scheduled_filenames()
    unscheduled = md_files - scheduled_filenames
    if not unscheduled:
        print("All .md files are already scheduled.")
        return

    print(f"Found {len(unscheduled)} unscheduled file(s).")

    # Get already occupied dates
    occupied_dates = get_scheduled_dates()

    # Start from tomorrow
    cursor = datetime.now().date() + timedelta(days=1)
    for md_file in sorted(unscheduled):   # deterministic order
        # Find next free day
        while cursor.strftime("%Y%m%d") in occupied_dates:
            cursor += timedelta(days=1)
        date_str = cursor.strftime("%Y%m%d")
        append_schedule(md_file, date_str)
        occupied_dates.add(date_str)      # mark this day as used for next files
        cursor += timedelta(days=1)       # move to next day (once per day)

# ==================== ORIGINAL POSTING LOGIC ====================
def get_today_scheduled() -> tuple[str, str] | None:
    """
    Read posts.csv and return (filename, content) of the post scheduled for today.
    The 'time' column is expected as YYYYMMDDHHMM. Only the date part (YYYYMMDD) is compared.
    Returns None if no post is scheduled for today or if already posted.
    """
    today_yyyymmdd = datetime.now().strftime("%Y%m%d")
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                post_file = row.get("post", "").strip()
                time_str = row.get("time", "").strip()
                if not post_file or not time_str:
                    continue
                scheduled_date = time_str[:8]
                if scheduled_date == today_yyyymmdd:
                    if already_posted(post_file):
                        print(f"INFO: {post_file} already posted, skipping.")
                        continue
                    md_path = POSTS_DIR / post_file
                    if not md_path.exists():
                        print(f"ERROR: Markdown file {md_path} not found.")
                        continue
                    content = md_path.read_text(encoding='utf-8')
                    return (post_file, content)
    except Exception as e:
        print(f"ERROR reading CSV: {e}")
    return None

async def post_to_localhost(content: str) -> bool:
    """Automate login, split, and post. Returns True on success."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("Navigating to", LOCAL_URL)
            await page.goto(LOCAL_URL, timeout=15000)

            # Login
            await page.wait_for_selector("#username", timeout=10000)
            await page.fill("#username", USERNAME)
            print("Username entered.")
            await page.fill("#appPassword", APP_PASSWORD)
            print("Password entered.")
            await page.click("button[type='submit']")
            print("Login button clicked.")

            # Wait for post interface
            await page.wait_for_selector("#content", timeout=15000)
            print("Login successful.")

            # Paste content
            await page.fill("#content", content)
            print("Content pasted.")

            # Split
            await page.click("#splitButton")
            print("Split button clicked.")
            await asyncio.sleep(2)   # adjust as needed

            # Post
            await page.click("#postButton")
            print("Post button clicked.")

            # Wait for success message
            try:
                await page.wait_for_selector(
                    ".success-message, .toast-success, .alert-success",
                    timeout=15000
                )
                print("SUCCESS: Post confirmed.")
                return True
            except Exception:
                print("WARNING: No success indicator found, but buttons were clicked.")
                return True

        except Exception as e:
            print(f"ERROR during automation: {e}")
            await page.screenshot(path="error_screenshot.png")
            print("Screenshot saved as error_screenshot.png")
            return False
        finally:
            await browser.close()

# ==================== MAIN ====================
async def main():
    # Step 1: Automatically schedule any unscheduled .md files
    schedule_unscheduled_md_files()

    # Step 2: Proceed with today's posting (if any)
    scheduled = get_today_scheduled()
    if scheduled is None:
        print("No post scheduled for today (or already posted). Exiting.")
        return

    filename, content = scheduled
    print(f"Found scheduled post: {filename}")
    success = await post_to_localhost(content)
    if success:
        mark_posted(filename)
        print("Posting completed and recorded.")
    else:
        print("Posting failed. The post will be retried on next run.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())