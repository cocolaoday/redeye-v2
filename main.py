from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os

app = FastAPI()

# 焊接 Gemini 能源
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.get("/")
async def root():
    return {"status": "online", "system": "Red-Eye Audio Engine v1.0"}

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        # 1. 讀取主公上傳的音檔
        audio_content = await file.read()
        
        # 2. 呼叫 Gemini 進行語音分析
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            "請將這段音訊轉成文字，並總結出 3 個核心重點。使用繁體中文。",
            {"mime_type": "audio/mp3", "data": audio_content}
        ])
        
        return {
            "filename": file.filename,
            "analysis": response.text,
            "status": "success"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
