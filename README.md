# URL-Extract Skill

[English](README_EN.md) | 中文

URL-Extract 是一个面向 AI 工作流的链接提取 Skill。它将受支持网页中的公开视频、音频或漫画保存到本地，让能够读取本地媒体的 AI 继续进行画面检查、OCR、音频识别或转写。

> 本仓库为公开仓库，可直接查看代码并从 Releases 下载 Windows 发行版。

## 它能做什么

- 从链接或完整分享文案中自动找出真正的网页地址。
- 下载视频与音频，并合并为可直接播放的本地文件。
- Skill 使用适合 AI 读取的精简码率；独立 Python 文件默认下载最高码率。
- 把最终本地路径交给 AI，用于读取画面中的小字、分析音频或执行本地转写。
- 首次运行自动检查并安装缺失依赖。

URL-Extract 本身负责“提取和下载”。AI 是否能够理解画面与声音，取决于调用它的 AI 客户端是否具备视频读取、OCR 或转写能力。

## Skill 与 Python 文件的码率区别

| 使用方式 | 默认策略 | 用途 |
|---|---|---|
| URL-Extract Skill | `ai-readable` | 保留平台可提供的最高分辨率，再选择该分辨率下的最低可用码率；音频优先至少 64 kbps。降低文件大小和 AI 读取成本，同时尽量保留画面小字。 |
| 独立 `url-extract-for-Windows.py` | `highest` | 默认选择最高可用码率，适合保存原始高质量视频。 |

“AI 可读最低码率”不是下载最低分辨率。画面分辨率优先保留最高，只降低同分辨率下的码率。如果平台没有提供可靠的分辨率信息，程序会回退到最高码率，避免得到无法识别小字的低清画面。

## 支持的平台

| 平台 | 支持内容 |
|---|---|
| B站 / Bilibili | 视频、`b23.tv` 短链接、完整分享文案 |
| 抖音 / Douyin | 公开视频、短链接、完整分享文案 |
| YouTube | 普通视频、Shorts |
| X / Twitter | 包含公开视频的帖子 |
| Pornhub | 公开内容视频页面 |
| MissAV | 公开内容视频页面 |
| 51吃瓜 | `51cg1.com` 的公开视频帖子 |
| 18comic | 已获授权的单部 `/photo/<数字ID>` 作品，输出 PDF |

V1.0 不支持绕过登录、验证码、付费墙、年龄或地区限制、私密权限和 DRM。网页结构变化也可能导致某个平台暂时解析失败。

## 下载 Windows V1.0

1. 打开仓库的 [Releases](https://github.com/roxys0847/url-extract-skill/releases)。
2. 选择 `URL-Extract for Windows V1.0`。
3. 在 Assets 中下载 `url-extract-for-Windows.py`。

也可以从仓库的 `dist` 目录取得同一文件。当前发行版只提供 Windows 版本。

V1.0 文件 SHA-256：

```text
A9C9BA187C4AF877F61FF4A36DBD3F4E01C3A9B73771E3CF9ED8DD2B5472385A
```

## 系统要求

- Windows 10/11，x86-64。
- Python 3.11 或更高版本。
- 首次安装依赖时能够访问 PyPI、GitHub Releases 和 Playwright 浏览器下载服务。
- 解析目标平台时能够正常访问该平台。

不需要安装 Git。Deno、FFmpeg、Chromium 以及 Python 依赖由程序检查并自动准备。

固定版本的 Python 依赖包括：

- `yt-dlp==2026.8.19`
- `yt-dlp-ejs==0.8.0`
- `pycryptodomex==3.23.0`
- `httpx==0.28.1`
- `playwright==1.62.0`
- `Pillow==12.3.0`
- `pypdf==6.18.0`

程序还会准备 Deno 2.9.6、Windows 版 FFmpeg 和 Playwright Chromium。相关文件保存在当前用户目录下的 `.url-extract` 运行环境中，不会写入 Python 安装目录。

## Python 文件使用方法

### 1. 交互输入

在文件所在目录打开 PowerShell：

```powershell
py ".\url-extract-for-Windows.py"
```

出现提示后，粘贴链接或完整分享文案并按回车。

独立运行不指定质量参数时，默认下载最高码率。也可以手动使用 Skill 相同的 AI-readable 策略：

```powershell
py ".\url-extract-for-Windows.py" --quality ai-readable "<链接或完整分享文案>"
```

如果系统没有 `py` 命令，但 `python --version` 显示 3.11 或更高版本，可以把下文命令中的 `py` 替换为 `python`。

### 2. 直接传入链接或分享文案

```powershell
py ".\url-extract-for-Windows.py" "https://www.bilibili.com/video/BV..."
```

链接前后即使包含中文标题、复制提示或 Markdown 包装，程序也会尝试提取其中第一个受支持的链接。

### 3. 检查运行环境

此命令只检查，不下载或安装：

```powershell
py ".\url-extract-for-Windows.py" --check-env
```

- `ENV_CHECK_READY`：当前环境已准备好。
- `ENV_CHECK_INCOMPLETE`：仍有依赖或工具缺失。正常运行一次程序，让它自动安装。
- 网络检查是连通性提示，不代表所有平台都一定可访问。

### 4. 检查单文件完整性

```powershell
py ".\url-extract-for-Windows.py" --self-test
```

显示 `SELF_TEST_OK` 表示内嵌视频与漫画核心通过本地校验。

## 首次运行

第一次正常处理链接时，程序会依次检查 Python 组件、Deno、FFmpeg 和 Chromium，并只安装缺少的部分。准备完成后可能显示：

```text
首次运行环境已准备完成，请重新运行程序并再次输入链接。
```

这是正常流程。请关闭本次运行，再用同一个链接运行一次。

## 保存位置

```text
C:\Users\<当前用户名>\Downloads\URL-Extract\视频
C:\Users\<当前用户名>\Downloads\URL-Extract\漫画
```

视频按网页标题命名；漫画按作品标题生成 PDF。已有同名文件时，程序会使用不冲突的新文件名，不会直接覆盖。

## 安装 Skill

先下载或克隆本仓库。使用 ZIP 下载时不需要 Git。以下命令需要在仓库根目录执行。

### 安装到 Codex

个人 Skill 目录：

```text
C:\Users\<当前用户名>\.codex\skills\url-extract
```

PowerShell 安装命令：

```powershell
$target = Join-Path $env:USERPROFILE ".codex\skills\url-extract"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Path ".\skill\url-extract\*" -Destination $target -Recurse -Force
```

完成后重新启动 Codex。

### 安装到 Claude Code

此方式适用于支持本地 Skills 的 Claude Code，不适用于普通 claude.ai 网页聊天。

个人 Skill 目录：

```text
C:\Users\<当前用户名>\.claude\skills\url-extract
```

PowerShell 安装命令：

```powershell
$target = Join-Path $env:USERPROFILE ".claude\skills\url-extract"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Path ".\skill\url-extract\*" -Destination $target -Recurse -Force
```

完成后重新启动 Claude Code，或新建一个会话让它重新发现 Skill。

### 调用示例

向 Codex 或 Claude Code 发送受支持平台的链接，并要求下载、检查画面、读取音频或本地转写：

示例：

```text
使用 url-extract 下载这个链接，然后读取视频中的画面文字并转写音频：<链接>
```

Skill 内已附带相同的 Windows Python 文件，但会固定传入 `--quality ai-readable`。它先下载“最高分辨率内的最低码率”版本，再由 AI 使用可用的媒体工具读取。用户单独运行 `.py` 时不传该参数，仍然默认最高码率。

## 常见报错

### “请检查网络代理后重新运行”

程序无法访问依赖下载地址或目标平台。请确认：

- 浏览器能否打开 GitHub、PyPI 和目标网页。
- 防火墙、安全软件或校园/公司网络是否拦截 Python。
- 系统网络需要代理时，Python 是否也能使用该代理。

临时为当前 PowerShell 设置代理的示例：

```powershell
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
py ".\url-extract-for-Windows.py"
```

请把地址和端口替换为你自己的代理配置。不要把代理账号、密码、Cookie 或 Token 发到聊天或提交到仓库。

### 找不到 Python 或版本过低

安装 64 位 Python 3.11 或更高版本，并在安装时启用 `Add Python to PATH`。随后运行：

```powershell
py --version
```

### `can't open file` / 找不到文件

命令中的路径不正确。目录路径可能包含空格，建议使用英文双引号包住完整路径：

```powershell
py "D:\下载目录\url-extract-for-Windows.py" --check-env
```

### `unrecognized arguments: --check-env`

你运行的是较早版本。请从本仓库 Releases 重新下载 V1.0，并确认实际运行的文件路径。

### Deno、FFmpeg 或 Chromium 准备失败

先运行 `--check-env` 查看失败项目，再检查 GitHub Releases、PyPI 和 Playwright 下载服务是否可访问。修复网络或代理后重新正常运行，程序会继续补齐缺失项目。

### 某个平台仍然解析失败

- 确认链接是公开且仍然有效的具体作品页面。
- 在浏览器中确认该页面无需登录、验证码、付费或地区解锁。
- 尝试粘贴平台生成的完整分享文案。
- 更新到最新 Release 后重试。

如果仍失败，请提交 Issue，并附上平台、脱敏后的公开链接、Python 版本、`--check-env` 输出和完整错误文字。不要上传 Cookie、授权头或私人内容。

## 合规与安全

仅处理公开内容或你已获授权访问和下载的内容。请遵守当地法律、版权、隐私规定及平台条款。成人内容仅限达到法定年龄且有权访问的用户。URL-Extract 不用于绕过访问控制或 DRM。

程序不会要求 GitHub Token，也不应要求你提交浏览器 Cookie。临时媒体地址可能包含签名参数，请勿公开分享。
