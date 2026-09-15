---
name: url-extract
description: Use when a user provides a supported Bilibili, Douyin, YouTube, X/Twitter, Pornhub, MissAV, 51吃瓜, or authorized 18comic link and asks to download, inspect, read, or transcribe its public video, audio, frames, or comic pages on Windows.
---

# URL-Extract

Use the bundled Windows Python file to turn a supported public link or complete
share message into a local video or PDF. Once the file is local, use the AI
client's available media-reading or transcription tools to examine its audio,
frames, subtitles, and on-screen text.

Do not use iTingnao for supported URL-Extract links.

## Run

The bundled program is:

```text
scripts/url-extract for Windows.py
```

Require Windows x86-64 and Python 3.11 or later. Prefer the Python interpreter
already selected for the current workspace. Quote the script path because its
file name contains spaces.

Resolve the installed script path first:

```powershell
$urlExtract = Join-Path $env:USERPROFILE ".codex\skills\url-extract\scripts\url-extract for Windows.py"
```

Before the first download, check the environment without changing it:

```powershell
py -3.11 $urlExtract --check-env
```

Download from a URL or complete copied share message:

```powershell
py -3.11 $urlExtract "<URL or complete share text>"
```

If the Windows Python Launcher (`py`) is unavailable, use a verified Python
3.11+ interpreter and replace `py -3.11` with `python`.

If no argument is supplied, the program prompts for input. The first normal run
installs missing fixed-version dependencies and may stop with a request to run
the command again. Run it a second time with the same input.

## Handle the result

- Videos are written to `Downloads\URL-Extract\视频` under the current Windows
  user profile.
- Comics are written as highest-quality PDFs to
  `Downloads\URL-Extract\漫画`.
- The final stdout line is the absolute saved-file path.
- Use that local path for frame inspection, OCR, audio analysis, or local
  transcription only when the user asks for those actions.
- Do not summarize content unless requested.
- V1.0 has no metadata-only URL inspection mode; normal link processing
  downloads the media.

The downloader selects the highest available bitrate. It accepts complete share
messages containing captions, Chinese text, Markdown wrappers, and escaped URL
characters.

## Supported sources

- Bilibili video links and `b23.tv` short links
- Douyin video links and complete share messages
- YouTube videos and Shorts
- X/Twitter posts containing public video
- Pornhub and MissAV public adult-video pages
- Public 51吃瓜 video posts on `51cg1.com`
- Individual authorized `https://18comic.vip/photo/<id>` works, exported as PDF

## Troubleshoot

Run the read-only checks first:

```powershell
py -3.11 $urlExtract --check-env
py -3.11 $urlExtract --self-test
```

If dependency preparation fails or the program says
`请检查网络代理后重新运行。`, verify access to GitHub Releases, PyPI,
Playwright's browser download service, and the source platform. Configure the
user's approved HTTP/HTTPS proxy if their network requires one, then rerun.

Do not bypass login, CAPTCHA, paywalls, age or regional restrictions, private
access, or DRM. Report the actual error and limitation instead of claiming
success. Never print or retain cookies, authorization headers, or temporary
signed media URLs.

## Boundaries

Process only public content or content the user is authorized to access and
download. Respect applicable law, copyright, privacy, and platform terms. For
adult-only sources, require the user to be of legal age and authorized to access
the requested work.
