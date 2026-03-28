import requests
import json
import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 3.0
load_dotenv()
app = FastAPI()
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺美化介面 ---
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>紅瞳重工 | 戰略審計中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0f0f0f; color: #00ff41; font-family: 'Courier New', Courier, monospace; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { border: 2px solid #00ff41; padding: 40px; background: rgba(0, 20, 0, 0.9); box-shadow: 0 0 20px #00ff41; max-width: 600px; width: 90%; text-align: center; }
        h1 { border-bottom: 1px solid #00ff41; padding-bottom: 10px; font-size: 24px; }
        .status { color: #fff; margin-bottom: 20px; font-size: 14px; }
        input[type="file"] { background: #222; color: #00ff41; border: 1px dashed #00ff41; padding: 20px; width: 100%; margin: 20px 0; cursor: pointer; }
        button { background: #00ff41; color: #000; border: none; padding: 15px 30px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 20px #fff; }
        #result { margin-top: 30px; text-align: left; white-space: pre-wrap; font-size: 14px; color: #ddd; border-top: 1px solid #333; padding-top: 20px; }
        .loading { display: none; color: #ffeb3b; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>[AS-CORE-STRATEGIST] 戰略審計中心</h1>
        <p class="status">指揮官 ID: {commander} | 系統狀態: 在線</p>
        
        <form id="uploadForm">
            <input type="file" name="file" id="fileInput" accept="audio/*" required>
            <br>
            <button type="submit" id="submitBtn">啟動深度審計</button>
        </form>

        <div id="loading" class="loading">📡 正在進行多模態神經解析，請稍候... (約30-60秒)</div>
        <div id="result"></div>
    </div>

    <script>
        const form = document.getElementById('uploadForm');
        const btn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        const resultDiv = document.getElementById('result');

        form.onsubmit = async (e) => {
            e.preventDefault();
            btn.style.display = 'none';
            loading.style.display = 'block';
            resultDiv.innerText = '';

            const formData = new FormData(form);
            try {
                const response = await fetch('/upload-and-run', { method: 'POST', body: formData });
                const data = await response.json();
                if (data.status === 'success') {
                    resultDiv.innerHTML = "<h3>🔥 審計戰報噴發：</h3>" + data.report;
                } else {
                    resultDiv.innerText = "❌ 錯誤：" + (data.error || "未知故障");
                }
            } catch (err) {
                resultDiv.innerText = "❌ 連線中斷";
            } finally {
                btn.style.display = 'inline-block';
                loading.style.display = 'none';
            }
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
        return {"status": "failed", "error": "DIFY_API_KEY Missing"}

    try:
        # 1. 直接讀取上傳的檔案並轉發給 Dify
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        
        # 使用讀取緩衝區，避免在大文件上崩潰
        file_content = await file.read()
        files = {"file": (file.filename, file_content, file.content_type)}
        
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        # 2. 觸發 Workflow
        workflow_url = f"{BASE_URL}/workflows/run"
        payload = {
            "inputs": {
                "audio_input": {
                    "transfer_method": "local_file",
                    "upload_file_id": file_id,
                    "type": "document"
                }
            },
            "response_mode": "blocking",
            "user": USER_ID
        }
        
        json_headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        workflow_response = requests.post(workflow_url, headers=json_headers, data=json.dumps(payload))
        workflow_response.raise_for_status()
        
        # 3. 回收報表
        outputs = workflow_response.json().get("data", {}).get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
