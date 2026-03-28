import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 4.0 視覺權威版
# ==========================================

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺強化控制艙 (HTML + CSS + Markdown Parser) ---
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
        body { background: var(--bg-black); color: #e0e0e0; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        
        /* 標題區塊 */
        .header { border-left: 5px solid var(--danger-red); padding-left: 20px; margin-bottom: 40px; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); padding-top: 10px; padding-bottom: 10px; }
        h1 { color: #fff; margin: 0; letter-spacing: 3px; font-size: 28px; text-transform: uppercase; }
        .status-bar { font-size: 12px; color: var(--main-green); font-family: 'Courier New', monospace; margin-top: 5px; }

        /* 上傳控制區 */
        .upload-zone { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 30px; border-radius: 8px; text-align: center; margin-bottom: 30px; transition: 0.3s; }
        .upload-zone:hover { border-color: var(--main-green); box-shadow: 0 0 15px rgba(0, 255, 65, 0.1); }
        input[type="file"] { margin-bottom: 20px; color: #888; }
        button { background: var(--main-green); color: #000; border: none; padding: 15px 40px; font-weight: 800; cursor: pointer; border-radius: 4px; font-size: 16px; transition: 0.3s; width: 100%; }
        button:hover { background: #fff; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255,255,255,0.2); }

        /* 戰報輸出區 */
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 40px; border-radius: 8px; position: relative; overflow: hidden; }
        #report-container::before { content: "TOP SECRET / AUDIT REPORT"; position: absolute; top: 10px; right: 10px; font-size: 10px; color: #333; }
        
        /* Markdown 樣式優化 */
        #result-content h1, #result-content h2, #result-content h3 { color: var(--main-green); border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 30px; }
        #result-content table { width: 100%; border-collapse: collapse; margin: 20px 0; background: #0f1117; }
        #result-content th { background: #1a1c23; color: var(--main-green); text-align: left; padding: 12px; border: 1px solid #2a2d3a; }
        #result-content td { padding: 12px; border: 1px solid #2a2d3a; font-size: 14px; }
        #result-content blockquote { border-left: 4px solid var(--main-green); background: #1a1c23; margin: 20px 0; padding: 15px 20px; font-style: italic; color: #fff; }
        #result-content strong { color: var(--danger-red); }
        #result-content hr { border: 0; border-top: 1px solid #333; margin: 40px 0; }

        .loading { display: none; text-align: center; color: var(--main-green); padding: 20px; font-family: 'Courier New', monospace; }
        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略解析系統</h1>
            <div class="status-bar">STATUS: ACTIVE // USER: {commander} // PROTOCOL: AS-CORE-4.0</div>
        </div>

        <div class="upload-zone">
            <form id="uploadForm">
                <input type="file" name="file" id="fileInput" accept="audio/*" required>
                <button type="submit" id="submitBtn">啟動多模態神經審計</button>
            </form>
        </div>

        <div id="loading" class="loading"><span class="blink">>>> 正在截獲音軌... 啟動 Gemini 1.5 Pro 神經網絡... 正在進行人性解碼...</span></div>

        <div id="report-container">
            <div id="result-content"></div>
            <button onclick="window.print()" style="margin-top:40px; background:#333; color:#fff; font-size:12px; padding:10px;">匯出戰術存檔 (Print to PDF)</button>
        </div>
    </div>

    <script>
        const form = document.getElementById('uploadForm');
        const btn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        const reportContainer = document.getElementById('report-container');
        const resultContent = document.getElementById('result-content');

        form.onsubmit = async (e) => {
            e.preventDefault();
            btn.style.display = 'none';
            loading.style.display = 'block';
            reportContainer.style.display = 'none';

            const formData = new FormData(form);
            try {
                const response = await fetch('/upload-and-run', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.status === 'success') {
                    // 使用 marked 解析 Markdown 並渲染到 HTML
                    resultContent.innerHTML = marked.parse(data.report);
                    reportContainer.style.display = 'block';
                    // 平滑滾動到結果
                    reportContainer.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert("❌ 系統故障：" + JSON.stringify(data.error));
                }
            } catch (err) {
                alert("❌ 物理連線中斷");
            } finally {
                btn.style.display = 'block';
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
        # 1. 檔案上傳
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        file_content = await file.read()
        files = {"file": (file.filename, file_content, file.content_type)}
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        # 2. 觸發 Workflow (Array[File] 格式)
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
            
        # 3. 回收報表
        outputs = workflow_response.json().get("data", {}).get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or outputs.get("text") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
