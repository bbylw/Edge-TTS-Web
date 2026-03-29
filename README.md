# Edge-TTS Web 应用

基于微软 Edge TTS 的本地文本转语音工具，使用 FastAPI 后端 + 纯 HTML 前端。

## 功能特性

- **文本转语音**：支持中文普通话和美国英语
- **语音名称汉化**：中文语音显示友好中文名称（如"晓晓"、"云希"等）
- **语速调节**：支持 -50% 到 +50% 的语速调整
- **音量调节**：支持 -50% 到 +50% 的音量调整
- **在线播放**：内置音频播放器，生成后可立即播放
- **MP3 下载**：支持下载生成的音频文件

## 支持的语音列表

### 中文普通话

| 语音名称 | 显示名 | 性别 |
|---------|--------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 |
| zh-CN-XiaoyiNeural | 晓伊 | 女 |
| zh-CN-YunjianNeural | 云健 | 男 |
| zh-CN-YunxiNeural | 云希 | 男 |
| zh-CN-YunxiaNeural | 云夏 | 男 |
| zh-CN-YunyangNeural | 云扬 | 男 |

### 中文方言

| 语音名称 | 显示名 | 性别 | 方言 |
|---------|--------|------|------|
| zh-CN-liaoning-XiaobeiNeural | 辽宁-小北 | 女 | 辽宁话 |
| zh-CN-shaanxi-XiaoniNeural | 陕西-小妮 | 女 | 陕西话 |

### 英语(美国)

| 语音名称 | 性别 |
|---------|------|
| en-US-AriaNeural | 女 |
| en-US-AnaNeural | 女 |
| en-US-ChristopherNeural | 男 |
| en-US-EricNeural | 男 |
| en-US-GuyNeural | 男 |
| en-US-JennyNeural | 女 |
| en-US-MichelleNeural | 女 |
| en-US-RogerNeural | 男 |
| en-US-SteffanNeural | 男 |

## 快速开始

### 环境要求

- Python 3.6+

### 安装依赖

```bash
pip install edge-tts fastapi uvicorn
```

### 启动服务

```bash
python server.py
```

### 访问应用

打开浏览器访问：http://localhost:8000

## 项目结构

```
.
├── server.py      # FastAPI 后端服务
├── index.html     # 前端页面（纯 HTML/CSS/JS）
└── README.md      # 项目文档
```

### server.py

FastAPI 后端服务，提供以下功能：
- 语音列表获取（过滤中文和英文语音）
- 文本转语音 API
- 静态文件服务（index.html）

### index.html

纯前端页面，包含：
- 现代化深色主题 UI
- 语音选择下拉框（按语言分组）
- 语速/音量滑块调节
- 音频播放和下载功能

## API 文档

### GET /

返回前端页面。

**响应**：HTML 页面

---

### GET /api/voices

获取可用语音列表。

**响应**：
```json
[
  {
    "Name": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)",
    "ShortName": "zh-CN-XiaoxiaoNeural",
    "Gender": "Female",
    "Locale": "zh-CN",
    "DisplayName": "晓晓"
  }
]
```

---

### POST /api/tts

文本转语音接口。

**请求体**：
```json
{
  "text": "要转换的文本内容",
  "voice": "zh-CN-XiaoxiaoNeural",
  "rate": "+0%",
  "volume": "+0%"
}
```

**参数说明**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| text | string | 是 | - | 要转换的文本内容 |
| voice | string | 否 | zh-CN-XiaoxiaoNeural | 语音名称 |
| rate | string | 否 | +0% | 语速调节，格式：±N% |
| volume | string | 否 | +0% | 音量调节，格式：±N% |

**响应**：音频流（audio/mpeg）

## 技术栈

- **后端**：
  - [edge-tts](https://github.com/rany2/edge-tts) - 微软 Edge TTS 的 Python 封装
  - [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
  - [Uvicorn](https://www.uvicorn.org/) - ASGI 服务器

- **前端**：
  - HTML5
  - CSS3（自定义样式，无第三方 CSS 框架）
  - Vanilla JavaScript（无第三方 JS 框架）

## 致谢

感谢 [edge-tts](https://github.com/rany2/edge-tts) 项目提供的微软 Edge TTS 接口封装。
