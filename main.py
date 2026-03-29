import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 5.5
# 搭載 時間維度預言機 (Temporal Predictor)
# ==========================================

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺強化指揮艙 (Full Intelligence Integration) ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略審計指揮中心 5.5</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lamejs/1.2.1/lame.all.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; --intel-blue: #00d4ff; --gold: #ffd700; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { border-left: 5px solid var(--danger-red); padding: 15px 20px; margin-bottom: 30px; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { font-size: 24px; margin: 0; color: #fff; letter-spacing: 1px; }

        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 30px; border-radius: 8px; text-align: center; }
        
        /* 戰略情報板強化版 */
        .intel-board { display: none; background: #000; border: 1px dashed var(--intel-blue); padding: 15px; margin: 20px 0; text-align: left; font-family: 'Courier New', monospace; }
        .intel-header { color: var(--intel-blue); border-bottom: 1px solid #333; margin-bottom: 10px; padding-bottom: 5px; font-weight: bold; }
        .intel-item { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 13px; }
        .intel-value { color: var(--intel-blue); font-weight: bold; }
        .highlight-gold { color: var(--gold) !important; }

        .progress-container { display: none; width: 100%; background: #000; border: 1px solid #333; height: 24px; margin: 20px 0; position: relative; border-radius: 12px; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: linear-gradient(90deg, #004411, var(--main-green)); transition: width 0.3s; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 0; left: 0; font-size: 12px; line-height: 24px; color: #fff; font-weight: bold; }

        input[type="file"] { margin: 20px 0; color: #888; border: 1px solid #333; padding: 10px; width: 100%; box-sizing: border-box; background: #0a0b10; }
        button { background: var(--main-green); color: #000; border: none; padding: 15px 40px; font-weight: 800; cursor: pointer; border-radius: 4px; font-size: 16px; width: 100%; transition: 0.3s; }
        button:disabled { background: #333; color: #666; cursor: not-allowed; }
        
        .status-log { font-family: 'Courier New', monospace; font-size: 11px; color: var(--main-green); margin-top: 15px; text-align: left; height: 100px; overflow-y: auto; border: 1px solid #222; padding: 10px; background: #050505; }
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 40px; border-radius: 8px; margin-top: 30px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略審計指揮中心</h1>
            <div style="color: var(--main-green); font-size: 12px;">SYSTEM STATUS: TEMPORAL PREDICTOR 5.5</div>
        </div>

        <div class="control-panel">
            <input type="file" id="fileInput" accept="audio/*">
            
            <div class="intel-board" id="intelBoard">
                <div class="intel-header">[ 戰略情報預判報告 ]</div>
                <div class="intel-item"><span>原始載荷重量:</span> <span class="intel-value" id="origSize">-</span></div>
                <div class="intel-item"><span>任務音軌時長:</span> <span class="intel-value" id="duration">-</span></div>
                <div class="intel-item"><span>預期壓縮體積:</span> <span class="intel-value" id="predSize">-</span></div>
                <div class="intel-item"><span>算力節省比例:</span> <span class="intel-value" id="saveRate">-</span></div>
                <div class="intel-item" style="margin-top: 10px; border-top: 1px solid #222; padding-top: 5px;">
                    <span>預計解析耗時:</span> <span class="intel-value highlight-gold" id="estWaitTime">-</span>
                </div>
            </div>

            <button id="submitBtn" disabled>等待載荷裝填...</button>
            
            <div class="progress-container" id="progressContainer">
                <div class="progress-bar" id="progressBar"></div>
                <div class="progress-text" id="progressText">準備中...</div>
            </div>
            <div class="status-log" id="statusLog">>>> 指揮中心待命，請主公部署任務。</div>
        </div>

        <div id="report-container">
            <div id="result-content"></div>
        </div>
    </div>

    <script>
        const log = (msg) => {
            const div = document.getElementById('statusLog');
            div.innerHTML += `<br>>>> ${msg}`;
            div.scrollTop = div.scrollHeight;
        };

        const fileInput = document.getElementById('fileInput');
        const submitBtn = document.getElementById('submitBtn');
        const intelBoard = document.getElementById('intelBoard');

        fileInput.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            log(`載荷識別成功: ${file.name}`);
            submitBtn.disabled = true;
            submitBtn.innerText = "正在執行情報試算...";
            intelBoard.style.display = 'block';

            const audio = new Audio();
            const objectUrl = URL.createObjectURL(file);
            audio.src = objectUrl;

            audio.onloadedmetadata = () => {
                const durationSec = audio.duration;
                const origMB = file.size / 1024 / 1024;
                
                // 體積預判 (48kbps Mono)
                const predMB = (durationSec * 48000) / 8 / 1024 / 1024;
                const savePercent = ((1 - (predMB / origMB)) * 100).toFixed(1);

                // 時間預判 (Gemini 3.1 Flash 估算公式)
                // 15s 基礎網路 + 每 10 分鐘約 45s 解析時間
                const estWaitSec = Math.round((durationSec * 0.075) + 15);
                const waitString = estWaitSec > 60 
                    ? `${Math.floor(estWaitSec / 60)}分${estWaitSec % 60}秒` 
                    : `${estWaitSec} 秒`;

                document.getElementById('origSize').innerText = `${origMB.toFixed(2)} MB`;
                document.getElementById('duration').innerText = `${Math.floor(durationSec / 60)}分${Math.round(durationSec % 60)}秒`;
                document.getElementById('predSize').innerText = `${predMB.toFixed(2)} MB`;
                document.getElementById('saveRate').innerText = `${savePercent}%`;
                document.getElementById('estWaitTime').innerText = `~ ${waitString}`;

                if (predMB > 20) log("⚠️ 警告：壓縮後體積依然龐大，請主公做好長線作戰準備。");
                
                submitBtn.disabled = false;
                submitBtn.innerText = "啟動單聲道降維並發射";
                URL.revokeObjectURL(objectUrl);
            };
        };

        async function compressToMonoMP3(file) {
            log("啟動物理降維協議...");
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const arrayBuffer = await file.arrayBuffer();
            const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

            const mp3encoder = new lamejs.Mp3Encoder(1, audioBuffer.sampleRate, 48); 
            const samplesL = audioBuffer.getChannelData(0);
            let mixedSamples = samplesL;
            
            if (audioBuffer.numberOfChannels > 1) {
                const samplesR = audioBuffer.getChannelData(1);
                mixedSamples = new Float32Array(samplesL.length);
                for (let i = 0; i < samplesL.length; i++) {
                    mixedSamples[i] = (samplesL[i] + samplesR[i]) / 2;
                }
            }

            const int16Samples = new Int16Array(mixedSamples.length);
            for (let i = 0; i < mixedSamples.length; i++) {
                int16Samples[i] = Math.max(-1, Math.min(1, mixedSamples[i])) * 0x7FFF;
            }

            const bufferSize = 1152;
            const mp3Data = [];
            for (let i = 0; i < int16Samples.length; i += bufferSize) {
                const chunk = int16Samples.subarray(i, i + bufferSize);
                const mp3buf = mp3encoder.encodeBuffer(chunk);
                if (mp3buf.length > 0) mp3Data.push(mp3buf);
                
                if (i % (bufferSize * 500) === 0) {
                    const percent = Math.round((i / int16Samples.length) * 100);
                    document.getElementById('progressBar').style.width = percent + '%';
                    document.getElementById('progressText').innerText = `降維處理: ${percent}%`;
                }
            }
            
            const endBuf = mp3encoder.flush();
            if (endBuf.length > 0) mp3Data.push(endBuf);
            return new File([new Blob(mp3Data, { type: 'audio/mp3' })], "payload.mp3", { type: 'audio/mp3' });
        }

        submitBtn.onclick = async () => {
            const file = fileInput.files[0];
            submitBtn.style.display = 'none';
            document.getElementById('progressContainer').style.display = 'block';

            try {
                const monoFile = await compressToMonoMP3(file);
                const formData = new FormData();
                formData.append('file', monoFile);

                const xhr = new XMLHttpRequest();
                xhr.upload.onprogress = (e) => {
                    if (e.lengthComputable) {
                        const percent = Math.round((e.loaded / e.total) * 100);
                        document.getElementById('progressBar').style.width = percent + '%';
                        document.getElementById('progressText').innerText = `傳輸中: ${percent}%`;
                    }
                };

                xhr.onload = () => {
                    const data = JSON.parse(xhr.responseText);
                    if (xhr.status === 200 && data.status === 'success') {
                        document.getElementById('result-content').innerHTML = marked.parse(data.report);
                        document.getElementById('report-container').style.display = 'block';
                        log("戰略解析達成，情報已歸檔。");
                    } else {
                        log("❌ 戰敗回報: " + JSON.stringify(data.error));
                        submitBtn.style.display = 'block';
                    }
                };

                xhr.open('POST', '/upload-and-run', true);
                xhr.send(formData);
            } catch (err) {
                log("❌ 引擎致命錯誤: " + err);
                submitBtn.style.display = 'block';
            }
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT

@app.post("/upload-and-run")
async def upload_and_run(file: UploadFile = File(...)):
    if not API_KEY:
        return {"status": "failed", "error": "API_KEY Missing"}
    try:
        # 1. 發射至 Dify
        upload_url = f"{BASE_URL}/files/upload"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        file_content = await file.read()
        files = {"file": (file.filename, file_content, file.content_type)}
        upload_response = requests.post(upload_url, headers=headers, files=files)
        upload_response.raise_for_status()
        file_id = upload_response.json().get("id")

        # 2. 觸發 工作流
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
        
        outputs = workflow_response.json().get("data", {}).get("outputs", {})
        report = outputs.get("戰報") or outputs.get("戰略審計報告") or outputs.get("text") or str(outputs)
        
        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
