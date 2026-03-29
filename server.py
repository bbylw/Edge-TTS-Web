from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import edge_tts
from pathlib import Path

app = FastAPI(title="TTS Server", description="Edge TTS API Server")

BASE_DIR = Path(__file__).parent

# 中文语音显示名称映射表
ZH_CN_DISPLAY_NAMES = {
    "zh-CN-XiaoxiaoNeural": "晓晓",
    "zh-CN-XiaoyiNeural": "晓伊",
    "zh-CN-YunjianNeural": "云健",
    "zh-CN-YunxiNeural": "云希",
    "zh-CN-YunxiaNeural": "云夏",
    "zh-CN-YunyangNeural": "云扬",
    "zh-CN-liaoning-XiaobeiNeural": "辽宁-小北",
    "zh-CN-shaanxi-XiaoniNeural": "陕西-小妮",
}


class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoxiaoNeural"
    rate: str = "+0%"
    volume: str = "+0%"


@app.get("/")
async def root():
    """返回 index.html 文件"""
    index_path = BASE_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)


@app.get("/api/voices")
async def get_voices():
    """获取所有可用语音列表"""
    try:
        voices = await edge_tts.list_voices()
        voices = [v for v in voices if v["Locale"].startswith("zh-CN") or v["Locale"] == "en-US"]
        # 为每个语音添加 DisplayName 字段
        for v in voices:
            v["DisplayName"] = ZH_CN_DISPLAY_NAMES.get(v["ShortName"], v["ShortName"])
        return voices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list voices: {str(e)}")


@app.post("/api/tts")
async def text_to_speech(req: TTSRequest):
    """文本转语音，返回音频流"""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        async def audio_stream():
            communicate = edge_tts.Communicate(
                text=req.text,
                voice=req.voice,
                rate=req.rate,
                volume=req.volume
            )
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]

        return StreamingResponse(
            audio_stream(),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=tts.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
