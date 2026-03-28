import requests, json, os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 7.1
# 鋼鐵強化版：解決 500 錯誤 | 錯誤自動診斷
# 搭載引擎：Gemini 3.1 Flash
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標 (請確認 Zeabur 的 Variables 裡有這些 Key)
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺強化控制艙 (採用分段焊接，避開 Python 3.13 語法黑洞) ---
def get_ui():
    part1 = """<!DOCTYPE html><html lang="zh-TW"><head><meta charset="UTF-8"><title>紅瞳重工 | 戰略指揮中心</title>"""
    part2 = """<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>"""
    part3 = """<style>:root{--main-green:#00ff41;--danger-red:#ff3e3e;--bg-black:#0a0b10;--card-bg:#14171f}body{background:var(--bg-black);color:#e0e0e0;font-family:system-ui,sans-serif;margin:0;padding:10px}"""
    part4 = """.container{width:100%;max-width:900px;margin:0 auto;box-sizing:border-box}.header{border-left:5px solid var(--danger-red);padding:10px 15px;margin:20px 0;background:linear-gradient(90deg,#1a1c23 0%,transparent 100%)}"""
    part5 = """h1{color:#fff;margin:0;font-size:clamp(18px,5vw,24px);text-transform:uppercase;letter-spacing:2px}.engine-tag{display:inline-block;background:#000;color:var(--main-green);padding:2px 8px;border-radius:3px;font-size:10px;margin-top:8px;border:1px solid var(--main-green);font-family:monospace}"""
    part6 = """.control-panel{background:var(--card-bg);border:1px solid #2a2d3a;padding:25px;border-radius:12px;text-align:center}.upload-box{border:2px dashed #333;padding:40px 10px;margin-bottom:20px;border-radius:8px}"""
    part7 = """button{background:var(--main-green);color:#000;border:none;padding:18px;font-weight:900;cursor:pointer;border-radius:8px;font-size:18px;width:100%}.progress-container{display:none;width:100%;background:#000;height:12px;margin-top:20px;border-radius:6px;overflow:hidden;border:1px solid #333}"""
    part8 = """.progress-bar{width:0%;height:100%;background:var(--main-green)}#report-container{display:none;background:var(--card-bg);border:1px solid #2a2d3a;padding:20px;border-radius:12px;margin-top:25px}.table-wrapper{width:100%;overflow-x:auto;margin:20px 0;border:1px solid #333}"""
    part9 = """table{border-collapse:collapse;min-width:600px;width:100%}th,td{padding:12px;border:1px solid #2a2d3a;font-size:14px}th{background:#1a1c23;color:var(--main-green)}blockquote{border-left:4px solid var(--danger-red);background:#1a1c23;padding:15px;margin:20px 0;font-style:italic}</style></head>"""
    part10 = """<body><div class="container"><div class="header"><h1>紅瞳重工 戰略指揮中心</h1><div class="engine-tag">ENGINE: GEMINI 3.1 FLASH // V7.1 STEEL</div></div>"""
    part11 = """<div class="control-panel"><form id="uploadForm"><div class="upload-box"><input type="file" name="file" id="fileInput" accept="audio/*" required></div><button type="submit" id="submitBtn">啟動多模態審計發射</button></form>"""
    part12 = """<div class="progress-container" id="progressContainer"><div class="progress-bar" id="progressBar"></div></div><div id="progressText" style="margin-top:10px;font-size:12px;color:var(--main-green);font-family:monospace"></div></div>"""
    part13 = """<div id="report-container"><div id="result-content"></div><button id="downloadBtn" style="background:#333;color:#fff;margin-top:30px;font-size:14px;padding:12px;border-radius:5px;width:100%;border:1px solid #444;cursor:pointer">📥 存為 HTML 戰術資產</button></div></div>"""
    part14 = """<script>const form=document.getElementById('uploadForm'),btn=document.getElementById('submitBtn'),progressBar=document.getElementById('progressBar'),progressContainer=document.getElementById('progressContainer'),progressText=document.getElementById('progressText'),reportContainer=document.getElementById('report-container'),resultContent=document.getElementById('result-content'),downloadBtn=document.getElementById('downloadBtn');"""
    part15 = """form.onsubmit=(e)=>{e.preventDefault();const f=document.getElementById('fileInput').files[0];if(!f)return;btn.style.display='none';progressContainer.style.display='block';reportContainer.style.display='none';const fd=new FormData();fd.append('file',f);const xhr=new XMLHttpRequest();"""
    part16 = """xhr.upload.onprogress=(ev)=>{const p=Math.round((ev.loaded/ev.total)*100);progressBar.style.width=p+'%';progressText.innerText='>>> UPLOADING: '+p+'%';};xhr.onload=()=>{const d=JSON.parse(xhr.responseText);if(xhr.status===200&&d.status==='success'){let h=marked.parse(d.report).replace(/<table/g,'<div class="table-wrapper"><table').replace(/<\\/table>/g,'</table></div>');resultContent.innerHTML=h;reportContainer.style.display='block';progressText.innerText='>>> 審計完成。';}else{alert("故障: "+JSON.stringify(d.error));btn.style.display='block';}};xhr.open('POST','/upload-and-run',true);xhr.send(fd);};"""
    part17 = """downloadBtn.onclick=()=>{const c=resultContent.innerHTML;const h=`<html><head><meta charset="UTF-8"><style>body{background:#0a0b10;color:#e0e0e0;font-family:sans-serif;padding:20px}table{border-collapse:collapse;width:100%;margin:20px 0}th,td{border:1px solid #333;padding:12px}th{background:#1a1c23;color:#00ff41}blockquote{border-left:4px solid #ff3e3e;background:#14171f;padding:15px}</style></head><body>${c}</body></html>`;const b=new Blob([h],{type:'text/html'});const l=document.createElement('a');l.href=URL.createObjectURL(b);l.download=`紅瞳戰報_${new Date().getTime()}.html`;l.click();};</script></body></html>"""
    return part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16 + part17

@app.get("/", response_class=HTMLResponse)
async def index():
    try:
        return get_ui()
    except Exception as e:
        return f"<h1>[紅瞳重工] 內核解碼故障</h1><p>{str(e)}</p>"

@app.post("/upload-and-run")
async def upload_and_run(file: UploadFile = File(...)):
    if not API_KEY:
        return {"status": "failed", "error": "環境變數 DIFY_API_KEY 缺失，請檢查 Zeabur 設定"}
    try:
        # 上傳到 Dify
        f_data = await file.read()
        up_res = requests.post(
            f"{BASE_URL}/files/upload", 
            headers={"Authorization": f"Bearer {API_KEY}"}, 
            files={"file": (file.filename, f_data, file.content_type)},
            timeout=30
        )
        up_res.raise_for_status()
        f_id = up_res.json().get("id")
        
        # 觸發工作流
        payload = {
            "inputs": {"audio_input": [{"transfer_method": "local_file", "upload_file_id": f_id, "type": "audio"}]},
            "response_mode": "blocking", "user": USER_ID
        }
        wf_res = requests.post(
            f"{BASE_URL}/workflows/run", 
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, 
            data=json.dumps(payload),
            timeout=120
        )
        wf_res.raise_for_status()
        
        data = wf_res.json()
        # 這裡的 '戰報' 必須與您 Dify 輸出節點的變數名一致
        report = data.get("data", {}).get("outputs", {}).get("戰報", "未偵測到輸出數據，請檢查 Dify 節點命名。")
        return {"status": "success", "report": report}
    except requests.exceptions.RequestException as e:
        return {"status": "failed", "error": f"API 通訊失敗: {str(e)}"}
    except Exception as e:
        return {"status": "failed", "error": f"系統內部故障: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
