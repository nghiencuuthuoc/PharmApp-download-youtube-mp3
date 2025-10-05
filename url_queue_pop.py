# -*- coding: utf-8 -*-
"""
Atomic URL queue popper with file lock.
- Queue file: url_yt_queue.txt  (UTF-8, one URL per line)
- Lock file:  url_queue.lock
Usage:
    python url_queue_pop.py
If a URL is available, prints it to stdout (single line). If queue is empty, prints nothing.
"""
import os
import time

LOCK = "url_queue.lock"
QUEUE = "url_yt_queue.txt"


def acquire_lock(poll_sec: float = 0.1):
    while True:
        try:
            # O_CREAT|O_EXCL => create only if not exists (atomic)
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return
        except FileExistsError:
            time.sleep(poll_sec)


def release_lock():
    try:
        os.remove(LOCK)
    except FileNotFoundError:
        pass


def pop_one():
    acquire_lock()
    try:
        if not os.path.exists(QUEUE):
            return None
        with open(QUEUE, "r", encoding="utf-8", errors="ignore") as f:
            lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
        if not lines:
            # Empty the file as well
            open(QUEUE, "w", encoding="utf-8").close()
            return None
        url = lines[0]
        # Rewrite remaining lines
        with open(QUEUE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines[1:]))
            if len(lines) > 1:
                f.write("\n")
        return url
    finally:
        release_lock()


if __name__ == "__main__":
    url = pop_one()
    if url:
        # IMPORTANT: print without extra spaces
        print(url)
