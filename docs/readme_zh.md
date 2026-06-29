<div align="center">

# AirDrop Plus

**在 Windows 与 iOS 之间轻松传输文件、同步剪贴板 —— 由 Python 与 Apple 快捷指令驱动。**

[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![iOS](https://img.shields.io/badge/iOS-Shortcuts-black.svg)](https://support.apple.com/guide/shortcuts/welcome/ios)
[![Python](https://img.shields.io/badge/python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../LICENSE)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20中文%20%7C%20Русский-orange.svg)](../src/translations)

[English](../readme.md) | 中文

</div>

---

## 目录

- [功能特性](#功能特性)
- [依赖](#依赖)
- [安装](#安装)
- [使用](#使用)
- [问题排查](#问题排查)
- [API 参考](#api-参考)
- [项目结构](#项目结构)
- [赞赏支持](#赞赏支持)
- [许可证](#许可证)

## 功能特性

- 📤 **发送文件** —— 在 iPhone 上一键触发快捷指令，将文件传到 PC。
- 📥 **接收文件** —— 把 PC 剪贴板里的文件直接取到 iPhone。
- 📝 **剪贴板同步** —— 文本、图片、文件双向同步。
- 🔔 **交互式 Windows 通知** —— 收到文件后可直接在通知里打开、定位或复制。
- 🌐 **局域网 / 热点直连** —— 无需联网、不耗流量、不经过第三方服务器。
- 🌍 **多语言界面** —— 英语、简体中文、Русский，并自动匹配系统语言。
- ⚙️ **网页版设置** —— 本地提供配置页面，快速调整。

## 依赖

| 依赖            | 版本     | 说明                                     |
|-----------------|----------|------------------------------------------|
| Python          | 3.10+    | 运行环境                                 |
| flask           | 3.0.0    | HTTP 服务                                |
| pillow          | 10.1.0   | 图片处理                                 |
| pystray         | 0.19.5   | 系统托盘图标                             |
| windows-toasts  | 1.3.1    | 交互式通知                               |
| pyperclip       | 1.8.2    | 剪贴板访问                               |
| Babel           | 2.14.0   | 仅构建期需要（`pybabel` 抽取 / 编译）    |
| pyinstaller     | 6.2.0    | 仅构建期需要（打包）                     |

> PC 端仅支持 **Windows**，需配合 iPhone 上的快捷指令使用。

## 安装

### 从源码运行

```bash
git clone https://github.com/<your-account>/AirDropPlus.git
cd AirDropPlus
pip install -r requirements.txt
python src/AirDropPlus.py
```

首次运行前复制配置模板 —— 程序读取 `src/config/config.ini`：

```bash
cp src/config/config.ini.example src/config/config.ini
```

### 打包成独立可执行文件

```bash
python src/build.py
```

打包后的 `AirDropPlus.exe` 生成在 `src/dist/` 目录下。

## 使用

### 0. 网络

- iPhone 和 PC 必须在同一局域网下，或一方连接另一方的热点。
- 通过热点传输**不消耗**蜂窝数据。

### 1. 在 PC 上安装 Bonjour（可选）

Bonjour 让你通过 `hostname.local` 而非 IP 地址访问 PC。最新版 Bonjour 可能无法解析 `hostname.local`，遇到时请降级使用旧版本。

<div align="center"><img src="images/windows_device_name.png" alt="Windows 设备名" width="35%"></div>

### 2. 启动 AirDropPlus

启动 `AirDropPlus.exe`（或 `python src/AirDropPlus.py`）。弹出防火墙提示时，点击**允许**。

<div align="center"><img src="images/network.png" alt="允许网络访问" width="35%"></div>

### 3. 配置

右键托盘图标，打开**设置**，配置密钥、端口和保存路径。

### 4. 在 iPhone 上获取快捷指令

快捷指令版本：**1.5.4** —— https://www.icloud.com/shortcuts/c499c9a3d9b04e189cce38d9560b3e2e

<div align="center"><img src="images/shortcut_QRcode.png" alt="快捷指令二维码" width="35%"></div>

### 5. 设置快捷指令

- **host**：`hostname.local`
- **port**：与 PC 端设置中相同的端口
- **key**：与 PC 端设置中相同的密钥

<div align="center"><img src="images/shortcut_conf.png" alt="快捷指令配置" width="35%"></div>

如果 PC 不支持 `hostname.local` 访问，可改用 PC 的 IP 地址。在下面的列表中填写你所有场景下的 WiFi 名称与 PC IP 组合。

<div align="center"><img src="images/shortcut_conf_2.png" alt="快捷指令 IP 配置" width="35%"></div>

### 6. 选择触发方式（三选一）

1. **轻点背面** —— *设置 → 辅助功能 → 触控 → 轻点背面*，双击手机背面触发。
2. **操作按钮** —— iPhone 15 Pro 及更新机型可通过侧边操作按钮触发。
   <div align="center"><img src="images/action_button.png" alt="操作按钮" width="35%"></div>
3. **控制中心** —— 新版 iOS 可将 'AirDrop Plus' 快捷指令添加到控制中心。
   <div align="center"><img src="images/control_centor.png" alt="控制中心" width="35%"></div>

### 7. 解除文件数量限制

*iPhone → 设置 → App → 快捷指令 → 高级 → 允许共享大量数据。* 不设置会导致发送多张图片时报错。

### 8. 功能测试

**发送文件** —— 将 'AirDrop Plus' 快捷指令添加到共享菜单，然后点击它。

<div align="center">
  <img src="images/edit_actions.png" alt="编辑操作" width="35%">
  <img src="images/edit_actions_2.png" alt="编辑操作" width="35%">
</div>
<div align="center">
  <img src="images/send_file.png" alt="发送文件" width="35%">
  <img src="images/send_file_pc.png" alt="PC 端收到" width="35%">
</div>

**发送文本** —— 复制文本，触发快捷指令，点击 **Send**。

**接收文件或文本** —— 触发快捷指令，点击 **Receive**，从 PC 剪贴板拉取内容。

<div align="center"><img src="images/shortcut_menu.png" alt="快捷指令菜单" width="40%"></div>

## 问题排查

<details>
<summary><b>快捷指令超时</b></summary>

1. 检查局域网是否通畅（校园网常禁止设备间通信）。
2. 确认 PC 端设置中的端口与快捷指令中设置的端口一致。
3. 确保快捷指令里的设备名与 **PC 主机名**一致（不要含中文，尽量避免 `-`）。可尝试把 `hostname.local` 换成 **IP 地址**。
4. 检查防火墙是否拦截了配置的端口。移除所有 AirDropPlus 相关的防火墙条目，重启 AirDropPlus，并在弹框中允许网络访问。

<div align="center">
  <img src="images/firewall.png" alt="防火墙" width="50%">
  <img src="images/network.png" alt="网络提示" width="35%">
</div>
</details>

<details>
<summary><b>启动后无通知，但后台进程仍在运行</b></summary>

可能是 Windows 版本太低，不支持交互式通知。在设置中切换为基本通知样式。

<div align="center"><img src="images/basic_notify.png" alt="基本通知" width="40%"></div>
</details>

## API 参考

AirDrop Plus 提供一套供 iOS 快捷指令调用的小型 HTTP API。完整参考见：

- 📖 [API 参考（中文）](api_zh.md)
- 📖 [API Reference (English)](api.md)

仓库的 [`api/`](../api/) 目录下附带了用于测试的 [Bruno](https://www.usebruno.com/) 请求集合。

## 项目结构

```
AirDropPlus/
├── src/                  # 全部源代码、配置与资源
│   ├── AirDropPlus.py    # 程序入口
│   ├── server.py         # Flask 服务与路由
│   ├── config.py         # 配置读取 / 保存
│   ├── i18n.py           # 基于 gettext 的国际化
│   ├── clipboard.py notifier.py result.py utils.py
│   ├── build.py          # PyInstaller 打包脚本
│   ├── babel.cfg         # pybabel 文案抽取配置
│   ├── config/           # config.ini（本地）+ config.ini.example（模板）
│   ├── static/           # icon.ico
│   ├── templates/        # settings.html
│   └── translations/     # gettext 翻译（en/ru/zh）
├── docs/                 # 中文 README、API 文档与图片
│   ├── readme_zh.md
│   ├── api.md / api_zh.md
│   └── images/
├── api/                  # Bruno API 测试集合
├── requirements.txt
├── readme.md
└── LICENSE
```

## 赞赏支持

如果这个项目帮你省了时间，欢迎请作者喝杯咖啡。☕

<div align="center">
  <table>
    <tr>
      <td align="center"><b>支付宝</b></td>
      <td align="center"><b>微信</b></td>
    </tr>
    <tr>
      <td align="center"><img src="images/alipay.png" alt="支付宝" width="180"></td>
      <td align="center"><img src="images/wechatpay.png" alt="微信" width="180"></td>
    </tr>
  </table>
</div>

## 许可证

基于 [MIT License](../LICENSE) 发布。

