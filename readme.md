<div align="center">

# AirDrop Plus

**Effortless file transfer and clipboard sync between Windows and iOS — powered by Python and Apple Shortcuts.**

[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![iOS](https://img.shields.io/badge/iOS-Shortcuts-black.svg)](https://support.apple.com/guide/shortcuts/welcome/ios)
[![Python](https://img.shields.io/badge/python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20中文%20%7C%20Русский-orange.svg)](src/translations)

English | [中文](docs/readme_zh.md)

</div>

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Support](#support)
- [License](#license)

## Features

- 📤 **Send files** from iPhone to PC with a single tap on a Shortcut.
- 📥 **Receive files** from the PC clipboard straight to your iPhone.
- 📝 **Clipboard sync** for text, images, and files in both directions.
- 🔔 **Interactive Windows notifications** — open, reveal, or copy received files directly from the toast.
- 🌐 **Works over LAN or hotspot** — no internet, no data usage, no third-party servers.
- 🌍 **Multilingual UI** — English, 简体中文, and Русский, with automatic system-language detection.
- ⚙️ **Web-based settings** served locally for quick configuration.

## Requirements

| Dependency      | Version  | Notes                                          |
|-----------------|----------|------------------------------------------------|
| Python          | 3.10+    | Runtime                                        |
| flask           | 3.0.0    | HTTP server                                    |
| pillow          | 10.1.0   | Image handling                                 |
| pystray         | 0.19.5   | System tray icon                               |
| windows-toasts  | 1.3.1    | Interactive notifications                      |
| pyperclip       | 1.8.2    | Clipboard access                               |
| Babel           | 2.14.0   | Build-time only (`pybabel` extract/compile)    |
| pyinstaller     | 6.2.0    | Build-time only (packaging)                    |

> AirDrop Plus is **Windows-only** on the PC side and pairs with an iOS Shortcut on the phone side.

## Installation

### Run from source

```bash
git clone https://github.com/<your-account>/AirDropPlus.git
cd AirDropPlus
pip install -r requirements.txt
python src/AirDropPlus.py
```

On first run, copy the config template — the app reads `src/config/config.ini`:

```bash
cp src/config/config.ini.example src/config/config.ini
```

### Build a standalone executable

```bash
python src/build.py
```

The packaged `AirDropPlus.exe` is generated under `src/dist/`.

## Usage

### 0. Network

- Your iPhone and PC must be on the same LAN, or one can connect to the other's hotspot.
- Transferring over a hotspot does **not** consume cellular data.

### 1. Install Bonjour on PC (optional)

Bonjour lets you reach the PC via `hostname.local` instead of an IP address. The latest Bonjour may fail to resolve `hostname.local` — use an older version if so.

<div align="center"><img src="docs/images/windows_device_name.png" alt="Windows device name" width="35%"></div>

### 2. Start AirDropPlus

Launch `AirDropPlus.exe` (or `python src/AirDropPlus.py`). When the firewall prompt appears, click **Allow**.

<div align="center"><img src="docs/images/network.png" alt="Allow network access" width="35%"></div>

### 3. Configure

Right-click the tray icon and open **Settings** to configure the key, port, and save path.

### 4. Get the iOS Shortcut

Shortcut version: **1.5.4** — https://www.icloud.com/shortcuts/c499c9a3d9b04e189cce38d9560b3e2e

<div align="center"><img src="docs/images/shortcut_QRcode.png" alt="Shortcut QR code" width="35%"></div>

### 5. Set up the Shortcut

- **host**: `hostname.local`
- **port**: same port as the PC-side settings
- **key**: same key as the PC-side settings

<div align="center"><img src="docs/images/shortcut_conf.png" alt="Shortcut configuration" width="35%"></div>

If your PC can't be reached via `hostname.local`, use its IP address instead. Fill in your WiFi-name / PC-IP combinations for every scenario in the list below.

<div align="center"><img src="docs/images/shortcut_conf_2.png" alt="Shortcut IP configuration" width="35%"></div>

### 6. Add the shortcut to Control Center

Add the 'AirDrop Plus' shortcut to Control Center.

<div align="center"><img src="docs/images/control_centor.png" alt="Control Center" width="35%"></div>

### 7. Lift the file-count limit

*iPhone → Settings → Apps → Shortcuts → Advanced → Allow Sharing Large Amounts of Data.* Skipping this causes errors when sending multiple images.

### 8. Try it out

**Send files** — add the 'AirDrop Plus' shortcut to the share sheet, then tap it.

<div align="center">
  <img src="docs/images/edit_actions.png" alt="Edit actions" width="35%">
  <img src="docs/images/edit_actions_2.png" alt="Edit actions" width="35%">
</div>
<div align="center">
  <img src="docs/images/send_file.png" alt="Send file" width="35%">
  <img src="docs/images/send_file_pc.png" alt="Received on PC" width="35%">
</div>

**Send text** — copy the text, trigger the shortcut, then tap **Send**.

**Receive files or text** — trigger the shortcut, then tap **Receive** to pull from the PC clipboard.

<div align="center"><img src="docs/images/shortcut_menu.png" alt="Shortcut menu" width="40%"></div>

## Troubleshooting

<details>
<summary><b>Shortcut times out</b></summary>

1. Check that the LAN allows device-to-device traffic (campus networks often block it).
2. Verify the port in the PC settings matches the port set in the Shortcut.
3. Ensure the Shortcut's hostname matches **the PC's hostname** (no Chinese characters, avoid `-`). Try swapping `hostname.local` for the **IP address**.
4. Check whether the firewall is blocking the configured port. Remove all AirDropPlus-related firewall entries, restart AirDropPlus, and allow the network prompt.

<div align="center">
  <img src="docs/images/firewall.png" alt="Firewall" width="50%">
  <img src="docs/images/network.png" alt="Network prompt" width="35%">
</div>
</details>

<details>
<summary><b>No notification after startup, but the process is running</b></summary>

The PC's Windows version may be too old for interactive notifications. Switch to basic notifications in the settings.

<div align="center"><img src="docs/images/basic_notify.png" alt="Basic notifications" width="40%"></div>
</details>

## API Reference

AirDrop Plus exposes a small HTTP API consumed by the iOS Shortcut. See the full reference:

- 📖 [API Reference (English)](docs/api.md)
- 📖 [API 参考 (中文)](docs/api_zh.md)

A [Bruno](https://www.usebruno.com/) request collection for testing is included under [`api/`](api/).

## Project Structure

```
AirDropPlus/
├── src/                  # All source code, config and resources
│   ├── AirDropPlus.py    # Entry point
│   ├── server.py         # Flask server and routes
│   ├── config.py         # Config loading / saving
│   ├── i18n.py           # gettext-based i18n
│   ├── clipboard.py notifier.py result.py utils.py
│   ├── build.py          # PyInstaller packaging script
│   ├── babel.cfg         # pybabel extraction config
│   ├── config/           # config.ini (local) + config.ini.example (template)
│   ├── static/           # icon.ico
│   ├── templates/        # settings.html
│   └── translations/     # gettext translations (en/ru/zh)
├── docs/                 # Chinese README, API docs and images
│   ├── readme_zh.md
│   ├── api.md / api_zh.md
│   └── images/
├── api/                  # Bruno API test collection
├── requirements.txt
├── readme.md
└── LICENSE
```

## Support

If this project saves you time, consider buying the author a coffee. ☕

<div align="center">
  <table>
    <tr>
      <td align="center"><b>Alipay</b></td>
      <td align="center"><b>WeChat Pay</b></td>
    </tr>
    <tr>
      <td align="center"><img src="docs/images/alipay.png" alt="Alipay" width="180"></td>
      <td align="center"><img src="docs/images/wechatpay.png" alt="WeChat Pay" width="180"></td>
    </tr>
  </table>
</div>

## License

Released under the [MIT License](LICENSE).

