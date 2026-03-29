import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 6.0
# 搭載 三段式即時戰況反饋系統
# ==========================================

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略審計指揮中心 6.0</title>
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
        .intel-header { color: var(--intel-blue); border-bottom: 1px solid #333; margin-bottom: 10px; padding-bottom: 5px; font-weight: bold; }
        .intel-item { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 13px; }
        .intel-value { color: var(--intel-blue); font-weight: bold; }

        /* 三段式進度條 */
        .progress-section { margin: 20px 0; display: none; }
        .progress-label { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 5px; color: var(--main-green); font-family: 'Courier New'; }
        .progress-container { width: 100%; background: #000; border: 1px solid #333; height: 12px; position: relative; border-radius: 6px; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: var(--main-green); transition: width 0.3s; }
        #analysisBar { background: var(--gold); } /* 解析條用金色區分 */

        input[type="file"] { margin: 20px 0; color: #888; border: 1px solid #333; padding: 10px; width: 100%; box-sizing: border-box; background: #0a0b10; }
        button { background: var(--main-green); color: #000; border: none; padding: 15px 40px; font-weight: 800; cursor: pointer; border-radius: 4px; font-size: 16px; width: 100%; transition: 0.3s; }
        button:disabled { background: #333; color: #666; cursor: not-allowed; }
        
        .status-log { font-family: 'Courier New', monospace; font-size: 11px; color: var(--main-green); margin-top: 15px; text-align: left; height: 100px; overflow-y: auto; border: 1px solid #222; padding: 10px; background: #050505; }
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 40px; border-radius: 8px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略審計指揮中心 6.0</h1>
            <div style="color: var(--main-green); font-size: 12px;">SYSTEM STATUS: REAL-TIME FEEDBACK ENABLED</div>
        </div>

        <div class="control-panel">
            <input type="file" id="fileInput" accept="audio/*">
            
            <div class="intel-board" id="intelBoard">
                <div class="intel-header">[ 戰略情報預判報告 ]</div>
                <div class="intel-item"><span>任務時長:</span> <span class="intel-value" id="duration">-</span></div>
                <div class="intel-item"><span>預估解析耗時:</span> <span class="intel-value" id="estWaitTime" style="color:var(--gold)">-</span></div>
            </div>

            <button id="submitBtn" disabled>等待載荷裝填...</button>
            
            <div id="progressZone">
                <div class="progress-section" id="sectionCompress">
                    <div class="progress-label"><span>STAGE 1: 物理降維 (Local Compression)</span><span id="txtCompress">0%</span></div>
                    <div class="progress-container"><div class="progress-bar" id="barCompress"></div></div>
                </div>
                <div class="progress-section" id="sectionUpload">
                    <div class="progress-label"><span>STAGE 2: 投彈傳輸 (Network Upload)</span><span id="txtUpload">0%</span></div>
                    <div class="progress-container"><div class="progress-bar" id="barUpload"></div></div>
                </div>
                <div class="progress-section" id="sectionAnalysis">
                    <div class="progress-label"><span>STAGE 3: 戰略解析 (AI Analysis)</span><span id="txtAnalysis">等待中</span></div>
                    <div class="progress-container"><div class="progress-bar" id="barAnalysis"></div></div>
                </div>
            </div>

            <div class="status-log" id="statusLog">>>> 指揮中心就緒。</div>
        </div>

        <div id="report-container"><div id="result-content"></div></div>
    </div>

    <script>
        let estWaitSecGlobal = 0;
        const log = (msg) => {
            const div = document.getElementById('statusLog');
            div.innerHTML += `<br>>>> ${msg}`;
            div.scrollTop = div.scrollHeight;
        };

        const fileInput = document.getElementById('fileInput
