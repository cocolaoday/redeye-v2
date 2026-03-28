import requests
import json
import os
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-EFFICIENCY 2.0 
# ==========================================

# 1. 初始化環境與伺服器
load_dotenv()
app = FastAPI()
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

@app.get("/")
def health_check():
    """讓 Zeabur 知道這個服務還活著"""
    return {"status": "Red-Eye System Online", "commander": USER_ID}

@app.get("/run")
def trigger_audit(audio_path: str = "amway_training.mp3"):
    """
    透過網址觸發：https://您的網址/run?audio_path=您的檔名.mp3
    """
    return run_strategic_audit(audio_path)

def run_strategic_audit(audio_file_path):
    if not API_KEY:
        return {"error": "DIFY_API_KEY Missing"}

    if not os.path.exists(audio_file_path):
        return {"error": f"File not found: {audio_file_path}"}

    # --- 第一步：檔案上傳 ---
    upload_url = f"{BASE_URL}/files/upload"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        with open(audio_file_path, "rb") as file:
            files = {"file": (os.path.basename(audio_file_path), file, "audio/mpeg")}
            upload_response = requests.post(upload_url, headers=headers, files=files)
            upload_response.raise_for_status()
            
        file_id = upload_response.json().get("id")

        # --- 第二步：觸發 Workflow ---
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
        
        json_headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        workflow_response = requests.post(workflow_url, headers=json_headers, data=json.dumps(payload))
        workflow_response.raise_for_status()
        
        # --- 第三步：回收戰報 ---
        result = workflow_response.json()
        outputs = result.get("data", {}).get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": str(e)}

# 啟動指令 (由 Zeabur 自動調用或本地測試使用)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
