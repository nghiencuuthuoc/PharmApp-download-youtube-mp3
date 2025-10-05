# -*- coding: utf-8 -*-
"""
2_down_mp3_url_yt_v2.py — v2.1 (2025-10-04)

Updates vs v2.0:
- Restore legacy flags: --force-inet4, --cookies-from-browser, --proxy, --throttled-rate,
  --username, --password, --twofactor (batch-friendly).
- Keep "skip if exists" unless --overwrite is set.
"""

import argparse, os, sys, textwrap
from typing import List, Tuple, Optional

try:
    import yt_dlp
except Exception:
    print("❌ yt-dlp is not installed. Install with:\n  python -m pip install -U --pre yt-dlp")
    raise

BANNER = r"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
YouTube Audio Downloader (Resilient) — v2.1
- iOS/Android player_client to avoid SABR
- Expanded format fallbacks
- Skip existing files unless --overwrite
- Legacy flags restored (--force-inet4, --cookies-from-browser, ...)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

def read_lines_maybe_file(target: str) -> List[str]:
    if os.path.exists(target) and os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            return [ln.strip() for ln in f if ln.strip()]
    return [target.strip()]

def ensure_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def build_base_opts(args) -> dict:
    postprocessors = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": args.codec,
        "preferredquality": args.quality,
    }]

    opts = {
        "outtmpl": os.path.join(args.output, "%(title)s.%(ext)s"),
        "noplaylist": not args.allow_playlist,
        "quiet": args.quiet,
        "no_warnings": False,
        "postprocessors": postprocessors,
        "prefer_ffmpeg": True,
        "keepvideo": False,
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 5,
        "overwrites": args.overwrite,
        "ignoreerrors": True,
        "extract_flat": False,
        "extractor_args": {"youtube": {"player_client": ["ios", "android", "web"]}},
    }

    if args.ffmpeg:
        opts["ffmpeg_location"] = args.ffmpeg
    if args.force_inet4:
        opts["force_inet4"] = True
    if args.cookies_from_browser:
        opts["cookiesfrombrowser"] = (args.cookies_from_browser,)
    if args.proxy:
        opts["proxy"] = args.proxy
    if args.throttled_rate:
        opts["throttledratelimit"] = args.throttled_rate
    if args.username:
        opts["username"] = args.username
    if args.password:
        opts["password"] = args.password
    if args.twofactor:
        opts["twofactor"] = args.twofactor

    return opts

def list_formats(url: str, opts: dict) -> None:
    local = opts.copy()
    local["listformats"] = True
    local.pop("postprocessors", None)
    with yt_dlp.YoutubeDL(local) as ydl:
        ydl.download([url])

def expected_filename(url: str, outtmpl: str, codec: str) -> Optional[str]:
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "simulate": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "unknown")
            base = outtmpl.rsplit("%(title)s", 1)[0]
            return os.path.join(base, f"{title}.{codec}")
    except Exception:
        return None

def download_one(url: str, base_opts: dict, format_candidates: List[str],
                 simulate: bool, overwrite: bool, codec: str) -> Tuple[bool, Optional[str]]:
    predicted = expected_filename(url, base_opts["outtmpl"], codec)
    if predicted and os.path.exists(predicted) and not overwrite:
        print(f"⏭️  Skipped (already exists): {os.path.basename(predicted)}")
        return True, None

    last_err = None
    for idx, fmt in enumerate(format_candidates, start=1):
        opts = base_opts.copy()
        opts["format"] = fmt
        if simulate:
            opts["simulate"] = True
        print(f"\n→ Trying format [{idx}/{len(format_candidates)}]: {fmt}")
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            print("✅ Success with format:", fmt)
            return True, None
        except yt_dlp.utils.DownloadError as e:
            last_err = str(e)
            print(f"⚠️  Failed with format '{fmt}': {last_err}")
        except Exception as e:
            last_err = repr(e)
            print(f"⚠️  Unexpected error with format '{fmt}': {last_err}")
    return False, last_err

def parse_args():
    p = argparse.ArgumentParser(
        prog="2_down_mp3_url_yt_v2.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Download audio from YouTube with resilient fallbacks and safe skipping.

            Examples:
              python 2_down_mp3_url_yt_v2.py urls.txt -o ./out --codec mp3 --quality 192 --force-inet4
              python 2_down_mp3_url_yt_v2.py "https://youtu.be/XXXX" --list-formats
        """)
    )
    p.add_argument("target", help="YouTube URL or text FILE of URLs (one per line).")
    p.add_argument("-o", "--output", default="./", help="Output folder (default: ./)")
    p.add_argument("--codec", default="mp3", choices=["mp3", "m4a", "opus", "wav", "flac"])
    p.add_argument("--quality", default="192", help="Bitrate hint (128/160/192/320)")
    p.add_argument("--ffmpeg", default=None, help="Path to ffmpeg/ffprobe folder")
    p.add_argument("--overwrite", action="store_true", help="Overwrite if file exists")
    p.add_argument("--allow-playlist", action="store_true", help="Allow full playlist")
    p.add_argument("--quiet", action="store_true", help="Less logs")

    # Restored network/auth helpers (batch compatibility)
    p.add_argument("--force-inet4", action="store_true", help="Force IPv4")
    p.add_argument("--cookies-from-browser", default=None, help="chrome/chromium/firefox/edge")
    p.add_argument("--proxy", default=None, help="HTTP(S) proxy, e.g. http://127.0.0.1:8888")
    p.add_argument("--throttled-rate", default=None, help="e.g., 100K or 1M")
    p.add_argument("--username", default=None)
    p.add_argument("--password", default=None)
    p.add_argument("--twofactor", default=None)

    # Debug helpers
    p.add_argument("--list-formats", action="store_true", help="List formats for the first URL and exit")
    p.add_argument("--simulate", action="store_true", help="Simulate (no download)")
    return p.parse_args()

def main():
    print(BANNER)
    args = parse_args()
    ensure_folder(args.output)
    urls = read_lines_maybe_file(args.target)
    if not urls:
        print("❌ No URL found."); sys.exit(1)

    base_opts = build_base_opts(args)
    format_candidates = [
        "bestaudio[ext=m4a]/bestaudio[acodec^=opus]/bestaudio/best",
        "bestaudio*",
        "bestvideo+bestaudio/best",
        "best"
    ]

    if args.list_formats:
        print("=== Listing formats for:", urls[0])
        try:
            list_formats(urls[0], base_opts)
        except Exception as e:
            print("❌ Failed to list formats:", e)
            print("\nTip: Update yt-dlp nightly: python -m pip install -U --pre yt-dlp")
            sys.exit(2)
        sys.exit(0)

    failures = []
    for i, url in enumerate(urls, 1):
        print(f"\n==================== [{i}/{len(urls)}] ====================")
        print("URL:", url)
        ok, err = download_one(url, base_opts, format_candidates,
                               simulate=args.simulate, overwrite=args.overwrite, codec=args.codec)
        if not ok:
            print("❌ Error for:", url)
            failures.append((url, err))

    if failures:
        print("\n==================== SUMMARY: FAILURES ====================")
        for url, err in failures:
            print(f"- {url}\n  {err}\n")
        sys.exit(3)

    print("\n✅ All done.")

if __name__ == "__main__":
    main()
