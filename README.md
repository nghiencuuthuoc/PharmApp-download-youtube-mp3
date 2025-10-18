# PharmApp — YouTube MP3 Downloader (Batch & Queue)

A small, pragmatic toolkit to **collect YouTube URLs** (from a playlist or a channel) and **download audio as MP3** using [yt-dlp]. It includes simple **queue-based, multi-worker** scripts (.bat/.ps1 helpers on Windows) so you can process long URL lists reliably.

> **Educational use only.** Respect YouTube’s Terms of Service and local laws. Only download content you have the right to save.

---

## ✨ Features

- **URL collectors**  
  - From a **playlist** → `1_get_url_yt_input_pl_v1.py`  
  - From a **channel** → `1_get_yt_urls_input_channel.py`  
  - Handy .bat wrappers for quick runs on Windows.
- **One-file downloads** from `url_yt.txt` → `2_down_mp3_url_yt_v2.py` (interactive prompts).
- **Queue-based parallel workers** for large batches  
  - Prepare & deduplicate queue → `prepare_queue.ps1` / `prepare_queue.bat`  
  - Pop the next URL atomically → `url_queue_pop.py`  
  - Launch multiple workers → `launch_workers.bat` / `worker_queue.bat`.
- **Works offline** once the URLs are listed. No accounts or API keys required.
- **Plain Python** with minimal dependencies.

---

## 🗂️ Repository layout

```
PharmApp-download-youtube-mp3/
├─ 0_how_use.md                  # Quick notes / usage (VN)
├─ 1_get_url_yt_input_pl.bat     # Windows helper for playlist grabber
├─ 1_get_url_yt_input_pl_v1.py   # Playlist URL collector (Python)
├─ 1_get_yt_urls_input_channel.bat
├─ 1_get_yt_urls_input_channel.py# Channel URL collector (Python)
├─ 1_get_yt_urls_option.bat      # Batch helper / options
├─ 2_down_mp3_url_yt_v2.py       # Download MP3 from urls (interactive)
├─ launch_workers.bat            # Spawn multiple download workers
├─ prepare_queue.bat             # Create queue file from url_yt.txt
├─ prepare_queue.ps1             # PowerShell variant of queue prep
├─ url_queue_pop.py              # Atomic pop from queue for workers
├─ url_yt.txt                    # Example URL list
├─ url_yt.zip                    # Compressed sample of URL list
└─ url_yt_queue.txt              # Work queue (generated)
```

> _Tip:_ Keep your `url_yt.txt` in UTF‑8. One URL per line.

---

## 📦 Requirements

- **Python 3.9+**
- **yt-dlp** (audio/video downloader)  
- **FFmpeg** (required for audio extraction & MP3 encoding)

```bash
# Windows (PowerShell) via pipx (recommended)
pip install --upgrade yt-dlp

# macOS (Homebrew)
brew install yt-dlp ffmpeg

# Debian/Ubuntu
sudo apt-get update && sudo apt-get install -y yt-dlp ffmpeg
```

> If `yt-dlp` is installed without a package manager, ensure it’s on your `PATH` and update regularly.

---

## 🚀 Quick start

### 1) Collect URLs
**Playlist**
```bash
python 1_get_url_yt_input_pl_v1.py
# Follow the prompts, paste the playlist URL → writes to url_yt.txt
```

**Channel**
```bash
python 1_get_yt_urls_input_channel.py
# Follow prompts → writes to url_yt.txt
```

### 2) Download MP3 (single worker)
```bash
python 2_down_mp3_url_yt_v2.py
# The script will ask for:
#   - Language (if relevant)
#   - The full path to url_yt.txt
#   - Output folder
#   - Whether to download subtitles or video (if supported)
#   - Overwrite/skip behavior
```

### 3) Queue-based parallel downloads (Windows)
For long lists, use the queue workflow:

```powershell
# Prepare the queue from url_yt.txt (dedupe/shuffle as needed)
.\prepare_queue.ps1

# OR (cmd)
prepare_queue.bat

# Launch multiple workers (each pops the next URL from the queue)
launch_workers.bat
# Alternatively, use worker_queue.bat which calls url_queue_pop.py
```

Each worker will repeatedly call `url_queue_pop.py` to fetch the next URL from `url_yt_queue.txt`, then run `2_down_mp3_url_yt_v2.py` against it. This avoids collisions and makes parallelizing safe.

---

## ⚙️ Notes & tips

- **FFmpeg is required** for MP3 extraction. Install it and keep it on your `PATH`.
- **Filenames**: The downloader uses yt‑dlp output templates inside the Python script. If you need _Title [VideoID] - YYYY-MM-DD.mp3_ naming, search for the output template string in `2_down_mp3_url_yt_v2.py` and adjust it (e.g., `-o "%(title)s [%(id)s] - %(upload_date>%Y-%m-%d)s.%(ext)s"`).
- **Resume / skip**: Prefer “skip if exists” for large queues to make the flow idempotent.
- **Windows paths**: When prompted for paths, avoid trailing backslashes or wrap them in quotes, e.g. `E:\PhatHoc\Dalai_Lama\` → `"E:\PhatHoc\Dalai_Lama\"` if entering in Python string form.

---

## ❗ Legal

This project is provided for **personal, lawful, educational use** only. You are responsible for complying with **YouTube’s Terms of Service** and local copyright law. Do **not** download or distribute content without permission from the rights holder.

---

## 🛠️ Troubleshooting

- **`ffmpeg not found`** → Install FFmpeg and ensure it’s on PATH (`ffmpeg -version`).
- **`HTTP 403/410`** → Update yt‑dlp: `python -m pip install -U yt-dlp`.
- **Weird characters in filenames** → Ensure UTF‑8 locale; consider sanitizing titles in the script.
- **Windows path errors (WinError 123)** → Avoid illegal characters like `<>:"|?*` in folder/file names.

---

## 🗺️ Roadmap ideas

- Add `requirements.txt` & `pyproject.toml`.
- Provide a cross‑platform CLI wrapper (`pharm-dlp`) for consistent prompts.
- Optional embedding of **ID3 metadata** and thumbnail cover via FFmpeg/yt‑dlp flags.
- Add **Dockerfile** for reproducible runs on Linux/macOS/Windows.

---

## 🤝 Contributing

PRs welcome! Please open an issue first if you plan larger changes (CLI args, output templates, queue format, etc.).

---

## 📄 License

_No license file currently in the repository._ Consider adding **MIT** or **Apache‑2.0** so others know how they can reuse contributions.

---

## 🙏 Credits

- Built on top of the excellent **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** and **FFmpeg**.
- Part of the **PharmApp** tooling ecosystem.
