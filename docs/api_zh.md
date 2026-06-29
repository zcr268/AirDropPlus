# API

[English](api.md) | [← 返回 README](readme_zh.md)

## 0. 请求头参数
| 参数名          | 类型   | 说明                                                                                              |
|-----------------|--------|---------------------------------------------------------------------------------------------------|
| ShortcutVersion | String | 快捷指令版本，须与 config.ini 中的 'version' 匹配。                                                |
| Authorization   | String | 密钥，须与 config.ini 中 'key' 的前两段匹配。例如 config.ini 中版本为 1.5.1，则此处填 1.5。        |

## 1. 发送文件
> 从手机端向 PC 发送文件。
### URL
[POST] /file

请求体：Form

| 参数名 | 类型 | 说明         |
|--------|------|--------------|
| file   | File | 要发送的文件 |

### 返回
- 返回类型：JSON
- 返回内容：
    ```json
    {
        "success": true,
        "msg": "发送成功",
        "data": null
    }
    ```
## 2. 获取文件
> 获取 PC 上的文件
### URL
[GET] /file/[path]

| 参数名 | 类型   | 说明                  |
|--------|--------|-----------------------|
| path   | String | 文件路径的 Base64 编码 |
### 返回
- 返回类型：File

## 3. 发送剪贴板
> 向 PC 发送剪贴板
### URL
[POST] /clipboard
### 请求参数
- 请求体：Form

| 参数名    | 类型   | 说明           |
|-----------|--------|----------------|
| clipboard | String | 手机剪贴板内容 |

### 返回
- 返回类型：JSON
- 返回内容：
    ```json
    {
        "success": true,
        "msg": "发送成功",
        "data": null
    }
    ```
## 4. 获取剪贴板内容
> 获取 PC 上的剪贴板内容
### URL
[GET] /clipboard
### 返回
- 返回类型：JSON
- 返回内容：
  - 当剪贴板为文本时：
    ```json
    {
        "success": true,
        "msg": "",
        "data": {
          "type": "text",
          "data": "clipboard_text"
        } 
    }
    ```
  - 当剪贴板为文件时：
      ```json
      {
          "success": true,
          "msg": "",
          "data": {
            "type": "file",
            "data": ["file1_path_base64", "file2_path_base64", "file3_path_base64"]
          }
      }
      ```
  - 当剪贴板为图片时：
      ```json
      {
          "success": true,
          "msg": "",
          "data": {
            "type": "img",
            "data": "img_base64_code"
          }
      }
      ```
## 5. 测试
> 测试连接
### URL
[GET] /
### 返回
- 返回类型：Text
- 返回内容：Hello world!
