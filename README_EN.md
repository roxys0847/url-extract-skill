# URL-Extract Skill

English | [中文](README.md)

URL-Extract is a link extraction skill for AI workflows. It saves public video,
audio, or comic content from supported pages to local files so an AI client
with media-reading capabilities can inspect frames, run OCR, analyze audio, or
create a local transcript.

> This repository is currently private. A GitHub account with repository access
> must be signed in to view the code or download a Release.

## What it does

- Finds the actual supported URL inside a link or complete share message.
- Downloads video and audio and merges them into a playable local file.
- Selects the highest publicly available bitrate by default.
- Exports an authorized individual 18comic work as a highest-quality PDF.
- Returns the final local path for AI frame reading, OCR, audio analysis, or
  local transcription.
- Checks and installs missing dependencies on the first run.

URL-Extract performs extraction and downloading. Understanding the downloaded
audio and visuals requires an AI client that can read local media, run OCR, or
transcribe audio.

## Supported platforms

| Platform | Supported content |
|---|---|
| Bilibili | Videos, `b23.tv` short links, and complete share messages |
| Douyin | Public videos, short links, and complete share messages |
| YouTube | Standard videos and Shorts |
| X / Twitter | Posts containing public video |
| Pornhub | Public adult-video pages |
| MissAV | Public adult-video pages |
| 51吃瓜 | Public video posts on `51cg1.com` |
| 18comic | Authorized individual `/photo/<numeric-id>` works exported to PDF |

V1.0 does not bypass login, CAPTCHA, paywalls, age or regional restrictions,
private access, or DRM. A platform may temporarily stop working when its page
or media API changes.

## Download Windows V1.0

1. Open the repository's [Releases](https://github.com/roxys0847/url-extract-skill/releases).
2. Select `URL-Extract for Windows V1.0`.
3. Download `url-extract for Windows.py` from Assets.

The same file is available in the repository's `dist` directory. V1.0 is
Windows-only.

V1.0 SHA-256:

```text
82B645776BE9D8F87431C29AEE47D95D9ADA4D95AB54D671089348D7B4763A71
```

## Requirements

- Windows 10/11 on x86-64.
- Python 3.11 or later.
- First-run access to PyPI, GitHub Releases, and Playwright's browser download
  service.
- Network access to the requested source platform.

Git is not required. The program checks and prepares Deno, FFmpeg, Chromium,
and its Python packages automatically.

Pinned Python dependencies include:

- `yt-dlp==2026.8.19`
- `yt-dlp-ejs==0.8.0`
- `pycryptodomex==3.23.0`
- `httpx==0.28.1`
- `playwright==1.62.0`
- `Pillow==12.3.0`
- `pypdf==6.18.0`

The program also prepares Deno 2.9.6, a Windows FFmpeg build, and Playwright
Chromium. Runtime files are kept under `.url-extract` in the current user's
profile rather than the Python installation directory.

## Using the Python file

### Interactive input

Open PowerShell in the file's directory:

```powershell
py -3.11 ".\url-extract for Windows.py"
```

Paste a URL or complete share message when prompted.

If the `py` launcher is unavailable but `python --version` reports Python 3.11
or later, replace `py -3.11` with `python` in the commands below.

### Pass input directly

```powershell
py -3.11 ".\url-extract for Windows.py" "https://www.bilibili.com/video/BV..."
```

The input may contain a title, Chinese copy text, Markdown wrappers, or escaped
URL characters. The first supported URL is extracted.

### Check the environment

This command is read-only and does not install or download anything:

```powershell
py -3.11 ".\url-extract for Windows.py" --check-env
```

- `ENV_CHECK_READY`: the environment is ready.
- `ENV_CHECK_INCOMPLETE`: one or more components are missing. Run the program
  normally once so it can install them.
- The network check is a connectivity hint; it cannot guarantee that every
  source platform is reachable.

### Verify the single file

```powershell
py -3.11 ".\url-extract for Windows.py" --self-test
```

`SELF_TEST_OK` confirms that both embedded cores passed local integrity checks.

## First run

On the first normal link-processing run, the program checks the Python
packages, Deno, FFmpeg, and Chromium and installs only missing components. It
may then stop with this message:

```text
首次运行环境已准备完成，请重新运行程序并再次输入链接。
```

This is expected. Close that run and process the same link again.

## Output locations

```text
C:\Users\<current-user>\Downloads\URL-Extract\视频
C:\Users\<current-user>\Downloads\URL-Extract\漫画
```

Videos use the page title as the file name. Comics use the work title for the
PDF. Existing files are not silently overwritten; a non-conflicting file name
is selected.

## Install the Skill

1. Download the repository ZIP or clone it. Git is not required when using ZIP.
2. Copy the entire `skill\url-extract` directory to:

```text
C:\Users\<current-user>\.codex\skills\url-extract
```

3. Restart Codex so it discovers the Skill.
4. Send a supported link and ask the AI to download it, inspect frames, read
   audio, or transcribe locally.

Example:

```text
Use url-extract to download this link, read the visible text in the video, and transcribe its audio: <URL>
```

The Skill includes the same Windows Python file. It downloads the content first
and then lets the AI use available local-media tools.

## Troubleshooting

### `请检查网络代理后重新运行。`

The program could not reach a dependency host or the source platform. Verify:

- Your browser can open GitHub, PyPI, and the source page.
- A firewall, security product, school network, or company network is not
  blocking Python.
- Python can use the required proxy when the system network depends on one.

Example temporary proxy configuration for the current PowerShell session:

```powershell
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
py -3.11 ".\url-extract for Windows.py"
```

Replace the address and port with your own proxy settings. Never share proxy
credentials, cookies, or tokens in chat or commit them to the repository.

### Python is missing or too old

Install 64-bit Python 3.11 or later and enable `Add Python to PATH` during
installation. Then run:

```powershell
py --version
```

### `can't open file`

The path is wrong. Because the file name contains spaces, quote the complete
path:

```powershell
py -3.11 "D:\Downloads\url-extract for Windows.py" --check-env
```

### `unrecognized arguments: --check-env`

An older file is being executed. Download V1.0 again from Releases and confirm
the actual path passed to Python.

### Deno, FFmpeg, or Chromium setup failed

Run `--check-env`, identify the failed component, and verify access to GitHub
Releases, PyPI, and Playwright's download service. Fix the network or proxy and
run the program normally again; it will continue preparing missing components.

### A platform still fails to parse

- Confirm that the URL points to a public, valid work page.
- Open it in a browser and confirm that it does not require login, CAPTCHA,
  payment, or a region unlock.
- Try the platform's complete generated share message.
- Update to the latest Release and retry.

If it still fails, open an Issue with the platform, a redacted public URL, the
Python version, `--check-env` output, and the full error text. Do not attach
cookies, authorization headers, or private content.

## Legal and security boundaries

Process only public content or content you are authorized to access and
download. Follow applicable law, copyright and privacy requirements, and
platform terms. Adult-only sources are limited to users of legal age who are
authorized to access the requested content. URL-Extract is not a tool for
bypassing access controls or DRM.

The program does not require a GitHub token and should not ask for browser
cookies. Temporary media URLs may contain signed parameters and must not be
shared publicly.
