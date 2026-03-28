import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 3.5 終極版
# ==========================================

# 1. 啟動環境與伺服器
load_dotenv()
app = FastAPI()

# 配置數據 (對齊主公的 Zeabur 陣地)
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺美化控制艙 (HTML UI) ---
# 此介面讓主公直接從電腦投擲 MP3 檔案，無需預存於 GitHub
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>紅瞳重工 | 戰略審計中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0b0e14; color: #00ff41; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { border: 2px solid #00ff41; padding: 40px; background: rgba(0, 15, 0, 0.9); box-shadow: 0 0 30px rgba(0, 255, 65, 0.2); max-width: 700px; width: 90%; text-align: center; border-radius: 5px; }
        h1 { border-bottom: 2px solid #00ff41; padding-bottom: 15px; font-size: 26px; letter-spacing: 2px; }
        .status { color: #888; margin-bottom: 30px; font-size: 13px; font-weight: bold; }
        .upload-box { background: #1a1a1a; border: 1px dashed #00ff41; padding: 30px; margin: 20px 0; border-radius: 5px; transition: 0.3s; }
        .upload-box:hover { background: #222; border-style: solid; }
        input[type="file"] { color: #00ff41; cursor: pointer; }
        button { background: #00ff41; color: #000; border: none; padding: 15px 40px; font-weight: 900; cursor: pointer; font-size: 18px; margin-top: 20px; transition: 0.3s; width: 100%; }
        button:hover { background: #fff; box-shadow: 0 0 25px #fff; }
        #result { margin-top: 30px; text-align: left; white-space: pre-wrap; font-size: 15px; color: #e0e0e0; line-height: 1.6; border-top: 1px solid #333; padding-top: 20px; }
        .loading { display: none; color: #ffeb3b; font-weight: bold; margin: 20px 0; animation: blink 1.2s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #444; padding: 8px; color: #fff; font-size: 14px; }
        th { background: #222; color: #00ff41; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[AS-CORE-STRATEGIST] 戰略審計中心</h1>
        <p class="status">COMMANDER: {commander} | SYSTEM: ONLINE | MODE: DIRECT-SYNC</p>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-box">
                <input type="file" name="file" id="fileInput" accept="audio/*" required>
            </div>
            <button type="submit" id="submitBtn">啟動深度神經審計</button>
        </form>

        <div id="loading" class="loading">📡 正在進行多模態解碼與人性架構審計，請勿關閉頁面...</div>
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
            resultDiv.innerHTML = '';

            const formData = new FormData(form);
            try {
                const response = await fetch('/upload-and-run', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.status === 'success') {
                    // 使用簡單的正則或 HTML 解析器來處理 Markdown 換行
                    const formattedReport = data.report.replace(/\\n/g, '<br>');
                    resultDiv.innerHTML = "<h3>🔥 深度審計戰報噴發：</h3>" + formattedReport;
                } else {
                    resultDiv.innerHTML = "❌ <b>部署故障：</b><br>" + JSON.stringify(data.error, null, 2);
                }
            } catch (err) {
                resultDiv.innerText = "❌ 物理連線中斷，請檢查網路或伺服器日誌。";
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
    """呈現視覺化控制艙"""
    return HTML_CONTENT.replace("{commander}", USER_ID)

@app.post("/upload-and-run")
async def upload_and_run(file: UploadFile = File(...)):
    """
    執行物理路徑：本地檔案接收 -> Dify 檔案上傳 -> Workflow 陣列觸發 -> 回收戰報
    """
    if not API_KEY:
        return {"status": "failed", "error": "環境變數 DIFY_API_KEY 缺失"}

    try:
        # 🛡️ 第一步：將接收到的檔案轉發給 Dify 彈藥庫
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        
        file_content = await file.read()
        files = {"file": (file.filename, file_content, file.content_type)}
        
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        # 🚀 第二步：觸發 Dify 工作流 (修正為 Array[File] 格式)
        workflow_url = f"{BASE_URL}/workflows/run"
        
        # ⚠️ 這裡必須封裝在 [ ] 陣列中，以對齊 Dify 畫布的欄位定義
        payload = {
            "inputs": {
                "audio_input": [
                    {
                        "transfer_method": "local_file",
                        "upload_file_id": file_id,
                        "type": "audio"
                    }
                ]
            },
            "response_mode": "blocking",
            "user": USER_ID
        }
        
        json_headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        workflow_response = requests.post(workflow_url, headers=json_headers, data=json.dumps(payload))
        
        # 🔍 若發生 400 錯誤，精準捕捉其具體原因
        if workflow_response.status_code != 200:
            return {"status": "failed", "error": workflow_response.json()}
            
        workflow_response.raise_for_status()
        
        # 🔥 第三步：回收最終審計戰報
        result = workflow_response.json()
        outputs = result.get("data", {}).get("outputs", {})
        
        # 自動適配輸出標籤
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or outputs.get("text") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": str(e)}

# Zeabur 通車配置：自動監聽指定端口
if __name__ == "__main__":
    import uvicorn
    # Zeabur 會動態注入 PORT 變數，預設為 8080
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
