import requests
import json
import os
import sys
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 6.6
# 搭載：暴力讀取核心 (Force-Reader) & 物理裝甲對齊
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標設定
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略審計指揮中心 6.6</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lamejs/1.2.1/lame.all.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; --intel-blue: #00d4ff; --gold: #ffd700; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { border-left: 5px solid var(--danger-red); padding: 15px 20px; margin-bottom: 30px; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { font-size: 24px; margin: 0; color: #fff; letter-spacing: 1px; }

        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 30px; border-radius: 8px; text-align: center; }
        
        .intel-board { display: none; background: #000; border: 1px dashed var(--intel-blue); padding: 15px; margin: 20px 0; text-align: left; font-family: 'Courier New', monospace; }
        .intel-item { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 13px; }
        .intel-value { color: var(--intel-blue); font-weight: bold; }

        .progress-section { margin: 20px 0; display: none; }
        .progress-label { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 5px; color: var(--main-green); font-family: 'Courier New'; }
        .progress-container { width: 100%; background: #000; border: 1px solid #333; height: 14px; position: relative; border-radius: 7px; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: var(--main-green); transition: width 0.3s; }

        input[type="file"] { margin: 20px 0; color: #888; border: 1px solid #333; padding: 10px; width: 100%; background: #0a0b10; }
        button { background: var(--main-green); color: #000; border: none; padding: 18px 40px; font-weight: 800; cursor: pointer; border-radius: 4px; font-size: 16px; width: 100%; }
        button:disabled { background: #222; color: #444; }
        
        .status-log { font-family: 'Courier New', monospace; font-size: 11px; color: var(--main-green); margin-top: 15px; text-align: left; height: 120px; overflow-y: auto; border: 1px solid #222; padding: 10px; background: #050505; }
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 40px; border-radius: 8px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略審計指揮中心 6.6</h1>
            <div style="color: var(--main-green); font-size: 12px;">SYSTEM: FORCE-READER ACTIVE</div>
        </div>

        <div class="control-panel">
            <input type="file" id="fileInput" accept="audio/*">
            <div class="intel-board" id="intelBoard">
                <div class="intel-item"><span>音軌時長:</span> <span class="intel-value" id="duration">-</span></div>
                <div class="intel-item"><span>預計解析耗時:</span> <span class="intel-value" id="estWaitTime" style="color:var(--gold)">-</span></div>
            </div>

            <button id="submitBtn" disabled>等待裝填載荷...</button>
            
            <div id="progressZone">
                <div class="progress-section" id="sectionCompress"><div class="progress-label"><span>STAGE 1: 物理降維</span><span id="txtCompress">0%</span></div><div class="progress-container"><div class="progress-bar" id="barCompress"></div></div></div>
                <div class="progress-section" id="sectionUpload"><div class="progress-label"><span>STAGE 2: 投彈傳輸</span><span id="txtUpload">0%</span></div><div class="progress-container"><div class="progress-bar" id="barUpload"></div></div></div>
                <div class="progress-section" id="sectionAnalysis"><div class="progress-label"><span>STAGE 3: 戰略解析</span><span id="txtAnalysis">等待中</span></div><div class="progress-container"><div class="progress-bar" id="barAnalysis" style="background:#ffd700"></div></div></div>
            </div>
            <div class="status-log" id="statusLog">>>> 系統初始化完成，等待主公指令。</div>
        </div>
        <div id="report-container"><div id="result-content"></div></div>
    </div>

    <script>
        let estWaitSecGlobal = 0;
        const log = (msg) => {
            const div = document.getElementById('statusLog');
            div.innerHTML += `<br>>>> ${new Date().toLocaleTimeString()} | ${msg}`;
            div.scrollTop = div.scrollHeight;
        };

        // 檢查 LameJS 載入狀態
        window.onload = () => {
            if (typeof lamejs === 'undefined') {
                log("❌ 警告：MP3 壓縮引擎未載入，請檢查網路連線。");
            } else {
                log("✅ 壓縮引擎裝填完畢。");
            }
        };

        const fileInput = document.getElementById('fileInput');
        const submitBtn = document.getElementById('submitBtn');

        fileInput.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            log(`已偵測檔案: ${file.name} (${(file.size/1024/1024).toFixed(2)}MB)`);
            
            const audio = new Audio();
            const objectUrl = URL.createObjectURL(file);
            audio.src = objectUrl;
            audio.onloadedmetadata = () => {
                const durationSec = audio.duration;
                estWaitSecGlobal = Math.round((durationSec * 0.08) + 15);
                document.getElementById('intelBoard').style.display = 'block';
                document.getElementById('duration').innerText = `${Math.floor(durationSec/60)}分${Math.round(durationSec%60)}秒`;
                document.getElementById('estWaitTime').innerText = `~ ${estWaitSecGlobal} 秒`;
                submitBtn.disabled = false;
                submitBtn.innerText = "啟動全鏈路審計";
                URL.revokeObjectURL(objectUrl);
            };
            audio.onerror = () => {
                log("❌ 檔案格式讀取失敗，請確認是否為有效音檔。");
                submitBtn.disabled = true;
            };
        };

        async function compressToMonoMP3(file) {
            document.getElementById('sectionCompress').style.display = 'block';
            log("正在進行 STAGE 1：物理降維...");
            const audioCtx = new AudioContext();
            const arrayBuffer = await file.arrayBuffer();
            const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
            const mp3encoder = new lamejs.Mp3Encoder(1, audioBuffer.sampleRate, 48);
            const samples = audioBuffer.getChannelData(0);
            
            const int16Samples = new Int16Array(samples.length);
            for (let i = 0; i < samples.length; i++) {
                int16Samples[i] = Math.max(-1, Math.min(1, samples[i])) * 0x7FFF;
            }

            const bufferSize = 1152;
            const mp3Data = [];
            for (let i = 0; i < int16Samples.length; i += bufferSize) {
                const chunk = int16Samples.subarray(i, i + bufferSize);
                const mp3buf = mp3encoder.encodeBuffer(chunk);
                if (mp3buf.length > 0) mp3Data.push(mp3buf);
                if (i % (bufferSize * 500) === 0) {
                    const percent = Math.round((i / int16Samples.length) * 100);
                    document.getElementById('barCompress').style.width = percent + '%';
                    document.getElementById('txtCompress').innerText = percent + '%';
                }
            }
            const endBuf = mp3encoder.flush();
            if (endBuf.length > 0) mp3Data.push(endBuf);
            document.getElementById('barCompress').style.width = '100%';
            log("STAGE 1 完成。");
            return new File([new Blob(mp3Data, { type: 'audio/mp3' })], "payload.mp3");
        }

        submitBtn.onclick = async () => {
            submitBtn.style.display = 'none';
            try {
                const compressedFile = await compressToMonoMP3(fileInput.files[0]);
                document.getElementById('sectionUpload').style.display = 'block';
                log("正在進行 STAGE 2：投彈傳輸...");
                
                const formData = new FormData();
                formData.append('file', compressedFile);

                const xhr = new XMLHttpRequest();
                xhr.upload.onprogress = (e) => {
                    if (e.lengthComputable) {
                        const percent = Math.round((e.loaded / e.total) * 100);
                        document.getElementById('barUpload').style.width = percent + '%';
                        document.getElementById('txtUpload').innerText = percent + '%';
                    }
                };

                xhr.onload = () => {
                    if (xhr.status === 200) {
                        startAnalysisProgress();
                        const data = JSON.parse(xhr.responseText);
                        if (data.status === 'success') {
                            finishAnalysisProgress(data.report);
                        } else {
                            log("❌ 伺服器報錯: " + data.error);
                            submitBtn.style.display = 'block';
                        }
                    } else {
                        log(`❌ 傳輸失敗 (HTTP ${xhr.status}): ${xhr.responseText}`);
                        submitBtn.style.display = 'block';
                    }
                };
                xhr.open('POST', '/upload-and-run', true);
                xhr.send(formData);
            } catch (err) {
                log("❌ 致命錯誤: " + err);
                submitBtn.style.display = 'block';
            }
        };

        let analysisInterval;
        function startAnalysisProgress() {
            document.getElementById('sectionAnalysis').style.display = 'block';
            log("正在進行 STAGE 3：戰略解析中...");
            let current = 0;
            analysisInterval = setInterval(() => {
                current += 1;
                let percent = Math.min(Math.round((current / estWaitSecGlobal) * 100), 98);
                document.getElementById('barAnalysis').style.width = percent + '%';
                document.getElementById('txtAnalysis').innerText = `處理中: ${percent}%`;
            }, 1000);
        }

        function finishAnalysisProgress(report) {
            clearInterval(analysisInterval);
            document.getElementById('barAnalysis').style.width = '100%';
            document.getElementById('txtAnalysis').innerText = '100%';
            document.getElementById('result-content').innerHTML = marked.parse(report);
            document.getElementById('report-container').style.display = 'block';
            log("任務達成，戰報已生成。");
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT

@app.post("/upload-and-run")
async def upload_and_run(file: UploadFile = File(...)):
    # 物理感應器檢查
    if not API_KEY:
        return {"status": "failed", "error": "Server API_KEY Missing"}
    
    try:
        # 1. 讀取音軌載荷
        log_server("正在讀取檔案流...")
        file_content = await file.read()
        if not file_content:
            return {"status": "failed", "error": "Empty file received"}
        
        # 2. 上傳至 Dify
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        files = {"file": (file.filename, file_content, file.content_type)}
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        # 3. 觸發 工作流
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
        workflow_response.raise_for_status()
        
        data = workflow_response.json().get("data", {})
        outputs = data.get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or outputs.get("text") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": f"Server Logic Error: {str(e)}"}

def log_server(msg):
    print(f">>> SERVER LOG | {msg}")

if __name__ == "__main__":
    target_port = int(os.environ.get("PORT", 8080))
    # 使用字串 "main:app" 確保 uvicorn 能正確熱重載與解析路徑
    uvicorn.run("main:app", host="0.0.0.0", port=target_port, reload=False)
