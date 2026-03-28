import requests
import json
import os
import sys
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：核心神經對接配置
# ==========================================

# 加載隱形密鑰：
# 本地運行時讀取 .env 檔案；Zeabur 部署時讀取 Variables 設定。
load_dotenv()
API_KEY = os.getenv("DIFY_API_KEY") 

# 您的 Zeabur 私有伺服器座標
BASE_URL = "https://eijidify.zeabur.app/v1"

# 預設投彈目標 (本地 MP3 檔案路徑)
# 您可以將此路徑改為您常用的檔名，或在執行時動通傳入
AUDIO_FILE_PATH = "amway_training.mp3" 

# 指揮官識別碼
USER_ID = "Eiji_Commander"

def run_strategic_audit():
    """
    執行全流程：檔案上傳 -> Zeabur 工作流啟動 -> 戰略戰報回收
    """
    if not API_KEY:
        print("❌ [Error]：物理斷路！找不到 DIFY_API_KEY。")
        print("請檢查本地 .env 檔案或 Zeabur 的環境變數設定。")
        return

    print(f"🛡️ [紅瞳重工]：啟動戰略審計管線...")

    # 檢查本地檔案是否存在
    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"❌ [Error]：找不到彈藥！請確認音檔是否存在於路徑: {AUDIO_FILE_PATH}")
        return

    # --- 第一步：將檔案投送到 Zeabur 彈藥庫 (Upload File) ---
    upload_url = f"{BASE_URL}/files/upload"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        print(f"📦 [Step 1]：正在上傳音軌至 Zeabur 伺服器...")
        with open(AUDIO_FILE_PATH, "rb") as file:
            # 檔案裝填，識別為 audio/mpeg 格式
            files = {"file": (os.path.basename(AUDIO_FILE_PATH), file, "audio/mpeg")}
            upload_response = requests.post(upload_url, headers=headers, files=files)
            upload_response.raise_for_status()
            
        file_data = upload_response.json()
        file_id = file_data.get("id")
        print(f"✅ [Step 1]：上傳成功。檔案 ID: {file_id}")

        # --- 第二步：觸發 Gemini 1.5 Pro 多模態工作流 (Run Workflow) ---
        workflow_url = f"{BASE_URL}/workflows/run"
        
        # ⚠️ 這裡的 "audio_input" 必須與您 Dify『開始』節點設定的變數名稱完全一致
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
        
        print(f"🚀 [Step 2]：正在喚醒雲端 Gemini 聽覺神經...")
        workflow_response = requests.post(
            workflow_url, 
            headers=json_headers, 
            data=json.dumps(payload)
        )
        workflow_response.raise_for_status()
        
        result = workflow_response.json()
        
        # --- 第三步：解析並噴發戰報 (Output Retrieval) ---
        if result.get("status") == "succeeded":
            outputs = result.get("data", {}).get("outputs", {})
            
            # 自動掃描可能的輸出標籤名稱 (適配不同版本的命名)
            report = (
                outputs.get("戰報") or 
                outputs.get("戰略審計報告") or 
                outputs.get("text") or 
                str(outputs)
            )
            
            print("\n" + "🔥" * 25)
            print("紅瞳重工：深度戰略審計報表噴發")
            print("🔥" * 25 + "\n")
            print(report)
            print("\n" + "="*50)
            print("🛡️ [任務達成]：生存算力已成功回收。")
        else:
            print(f"❌ [Error]：工作流運行失敗。")
            print(f"錯誤代碼: {result.get('error')}")

    except Exception as e:
        print(f"❌ [Error]：系統焊接點斷路。詳細訊息: {str(e)}")

if __name__ == "__main__":
    run_strategic_audit()
