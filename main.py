import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 5.1
# 修正 Python 3.13 轉義崩潰 | 響應式適配
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標設定
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# 使用 r""" 原始字串，防止 \t 等字元被誤認為轉義字元
HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略指揮中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 10px; -webkit-font-smoothing: antialiased; }
        .container { width: 100%; max-width: 900px; margin: 0 auto; box-sizing: border-box; }
        .header { border-left: 4px solid var(--danger-red); padding: 10px 15px; margin: 20px 0; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { color: #fff; margin: 0; letter-spacing: 1px; font-size: clamp(18px, 5vw, 26px); text-transform: uppercase; }
        .engine-tag { display: inline-block; background: #000; color: var(--main-green); padding: 2px 8px; border-radius: 3px; font-size: 10px; margin-top: 8px; border: 1px solid var(--main-green); font-family: monospace; }
        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 20px; border-radius: 12px; text-align: center; }
        .upload-box { border: 2px dashed #333; padding: 30px 10px; margin-bottom: 20px; border-radius: 8px; }
        input[type="file"] { width: 100%; font-size: 14px; color: #888; }
        button { background: var(--main-green); color: #000; border: none; padding: 18px; font-weight: 800; cursor: pointer; border-radius: 8px; font-size: 16px; width: 100%; transition: 0.2s; }
        .progress-container { display: none; width: 100%; background: #000; height: 12px; margin-top: 20px; border-radius: 6px; overflow: hidden; border: 1px solid #333; }
        .progress-bar { width: 0%; height: 100%; background: var(--main-green); transition: width 0.1s; }
        .progress-text { margin-top: 8px; font-size: 12px; color: var(--main-green); font-family: monospace; }
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 20px; border-radius: 12px; margin-top: 25px; }
        .table-wrapper { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 20px 0; }
        table { border-collapse: collapse; min-width: 500px; width: 100%; }
        th, td { padding: 12px; border: 1px solid #2a2d3a; font-size: 14px; text-align: left; }
        th { background: #1a1c23; color: var(--main-green); }
        blockquote { border-left: 4px solid var(--danger-red); background: #1a1c23; padding: 15px; margin: 20px 0; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略指揮中心</h1>
            <div class="engine-tag">CORE: GEMINI 3.1 FLASH // V5.1 P-3.13 READY</div>
        </div>
        <div class="control-panel">
            <form id="uploadForm">
                <div class="upload-box"><input type="file" name="file" id="fileInput" accept="audio/*" required></div>
                <button type="submit" id="submitBtn">啟動多模態審計發射</button>
            </form>
            <div class="progress-container" id="progressContainer"><div class="progress-bar" id="progressBar"></div></div>
            <div class="progress-text" id="progressText"></div>
        </div>
        <div id="report-container"><div id="result-content"></div></div>
    </div>
    <script>
        const form = document.getElementById('uploadForm');
        const btn = document.getElementById('submitBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const reportContainer = document.getElementById('report-container');
        const resultContent = document.getElementById('result-content');

        form.onsubmit = (e) => {
            e.preventDefault();
            const file = document.getElementById('fileInput').files[0];
            if (!file) return;
            btn.style.display = 'none';
            progressContainer.style.display = 'block';
            reportContainer.style.display = 'none';
            const formData = new FormData();
            formData.append('file', file);
            const xhr = new XMLHttpRequest();
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = percent + '%';
                    progressText.innerText = `>>> UPLOADING: ${percent}%`;
                }
            };
            xhr.onload = () => {
                const data = JSON.parse(xhr.responseText);
                if (xhr.status === 200 && data.status === 'success') {
                    let rawHtml = marked.parse(data.report);
                    let shieldedHtml = rawHtml.replace(/<table/g, '<div class="table-wrapper"><table').replace(/<\/table>/g, '</table></div>');
                    resultContent.innerHTML = shieldedHtml;
                    reportContainer.style.display = 'block';
                    progressText.innerText = '>>> 審計報告已噴發。';
                    reportContainer.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert("❌ 戰區故障: " + JSON.stringify(data.error));
                    btn.style.display = 'block';
                }
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
    if not API_KEY: return {"status": "failed", "error": "API_KEY Missing"}
    try:
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        file_content = await file.read()
        files = {"file": (file.filename, file_content, file.content_type)}
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        workflow_url = f"{BASE_URL}/workflows/run"
        payload = {
            "inputs": {"audio_input": [{"transfer_method": "local_file", "upload_file_id": file_id, "type": "audio"}]},
            "response_mode": "blocking",
            "user": USER_ID
        }
        json_headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        workflow_response = requests.post(workflow_url, headers=json_headers, data=json.dumps(payload))
        
        outputs = workflow_response.json().get("data", {}).get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or str(outputs)
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # 強制使用 Zeabur 注入的 PORT，防止端口衝突
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
