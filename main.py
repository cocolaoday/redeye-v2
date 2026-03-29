import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 4.5
# 搭載 Gemini 3.1 Flash 戰略引擎
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標設定
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺強化指揮艙 (HTML + Progress Sensor) ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略審計指揮中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        
        .header { border-left: 5px solid var(--danger-red); padding: 15px 20px; margin-bottom: 30px; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { color: #fff; margin: 0; letter-spacing: 2px; font-size: 24px; }
        .engine-tag { display: inline-block; background: #333; color: var(--main-green); padding: 2px 8px; border-radius: 3px; font-size: 10px; margin-top: 5px; border: 1px solid var(--main-green); }

        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 30px; border-radius: 8px; text-align: center; }
        
        /* 物理進度條 */
        .progress-container { display: none; width: 100%; background: #000; border: 1px solid #333; height: 20px; margin: 20px 0; position: relative; border-radius: 10px; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: linear-gradient(90deg, #004411, var(--main-green)); transition: width 0.1s; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 0; left: 0; font-size: 12px; line-height: 20px; color: #fff; font-weight: bold; }

        input[type="file"] { margin: 20px 0; color: #888; }
        button { background: var(--main-green); color: #000; border: none; padding: 15px 40px; font-weight: 800; cursor: pointer; border-radius: 4px; font-size: 16px; transition: 0.3s; width: 100%; }
        button:hover { background: #fff; box-shadow: 0 0 20px rgba(255,255,255,0.4); }

        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 40px; border-radius: 8px; margin-top: 30px; }
        #result-content table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        #result-content th, #result-content td { border: 1px solid #2a2d3a; padding: 12px; font-size: 14px; }
        #result-content th { background: #1a1c23; color: var(--main-green); }
        #result-content blockquote { border-left: 4px solid var(--main-green); background: #1a1c23; padding: 15px; margin: 20px 0; color: #fff; }
        
        .loading-text { display: none; color: var(--main-green); font-family: 'Courier New', monospace; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略審計指揮中心</h1>
            <div class="engine-tag">CORE ENGINE: GEMINI 3.1 FLASH</div>
        </div>

        <div class="control-panel">
            <form id="uploadForm">
                <input type="file" name="file" id="fileInput" accept="audio/*" required>
                <button type="submit" id="submitBtn">啟動多模態審計發射</button>
            </form>

            <div class="progress-container" id="progressContainer">
                <div class="progress-bar" id="progressBar"></div>
                <div class="progress-text" id="progressText">0%</div>
            </div>
            <div class="loading-text" id="loadingText">>>> 正在通過 Zeabur 網關... 啟動 Gemini 3.1 Flash 解析中...</div>
        </div>

        <div id="report-container">
            <div id="result-content"></div>
        </div>
    </div>

    <script>
        const form = document.getElementById('uploadForm');
        const btn = document.getElementById('submitBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const loadingText = document.getElementById('loadingText');
        const reportContainer = document.getElementById('report-container');
        const resultContent = document.getElementById('result-content');

        form.onsubmit = (e) => {
            e.preventDefault();
            const file = document.getElementById('fileInput').files[0];
            if (!file) return;

            // 歸零顯示
            btn.style.display = 'none';
            progressContainer.style.display = 'block';
            reportContainer.style.display = 'none';
            progressBar.style.width = '0%';
            progressText.innerText = '0%';

            const formData = new FormData();
            formData.append('file', file);

            const xhr = new XMLHttpRequest();

            // 監聽物理上傳進度
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = percent + '%';
                    progressText.innerText = `上傳中: ${percent}% (${(event.loaded / 1024 / 1024).toFixed(2)}MB / ${(event.total / 1024 / 1024).toFixed(2)}MB)`;
                    if (percent === 100) {
                        loadingText.style.display = 'block';
                        progressText.innerText = '投彈成功，等待 Gemini 3.1 Flash 回報...';
                    }
                }
            };

            xhr.onload = () => {
                const data = JSON.parse(xhr.responseText);
                if (xhr.status === 200 && data.status === 'success') {
                    resultContent.innerHTML = marked.parse(data.report);
                    reportContainer.style.display = 'block';
                    loadingText.style.display = 'none';
                } else {
                    alert("❌ 審計失敗: " + JSON.stringify(data.error));
                    btn.style.display = 'block';
                }
            };

            xhr.onerror = () => {
                alert("❌ 物理連線中斷");
                btn.style.display = 'block';
            };

            xhr.open('POST', '/upload-and-run', true);
            xhr.send(formData);
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT.replace("{commander}", USER_ID)

@app.post("/upload-and-run")
async def upload_and_run(file: UploadFile = File(...)):
    if not API_KEY:
        return {"status": "failed", "error": "API_KEY Missing"}
    try:
        # 1. 檔案上傳至 Dify
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        file_content = await file.read()
        files = {"file": (file.filename, file_content, file.content_type)}
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        # 2. 觸發 Gemini 3.1 Flash 工作流
        workflow_url = f"{BASE_URL}/workflows/run"
        payload = {
            "inputs": {
                "audio_input": [{"transfer_method": "local_file", "upload_file_id": file_id, "type": "audio"}]
            },
            "response_mode": "blocking",
            "user": USER_ID
        }
        json_headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        workflow_response = requests.post(workflow_url, headers=json_headers, data=json.dumps(payload))
        
        if workflow_response.status_code != 200:
            return {"status": "failed", "error": workflow_response.json()}
            
        # 3. 解析結果
        outputs = workflow_response.json().get("data", {}).get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or outputs.get("text") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
