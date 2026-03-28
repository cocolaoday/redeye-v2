import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 5.0
# 全平台響應式適配版 | 搭載 Gemini 3.1 Flash
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
    <title>紅瞳重工 | 戰略指揮中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; }
        
        body { 
            background: var(--bg-black); 
            color: #e0e0e0; 
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
            margin: 0; 
            padding: 10px; /* 手機端邊距縮小 */
            -webkit-font-smoothing: antialiased;
        }

        .container { 
            width: 100%; 
            max-width: 900px; 
            margin: 0 auto; 
            box-sizing: border-box;
        }
        
        /* 標題區塊 - 響應式字體 */
        .header { 
            border-left: 4px solid var(--danger-red); 
            padding: 10px 15px; 
            margin: 20px 0; 
            background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); 
        }
        h1 { 
            color: #fff; 
            margin: 0; 
            letter-spacing: 1px; 
            font-size: clamp(18px, 5vw, 26px); /* 根據螢幕自動調整大小 */
            text-transform: uppercase;
        }
        .engine-tag { 
            display: inline-block; 
            background: #000; 
            color: var(--main-green); 
            padding: 2px 8px; 
            border-radius: 3px; 
            font-size: 10px; 
            margin-top: 8px; 
            border: 1px solid var(--main-green);
            font-family: monospace;
        }

        /* 控制面板 */
        .control-panel { 
            background: var(--card-bg); 
            border: 1px solid #2a2d3a; 
            padding: 20px; 
            border-radius: 12px; 
            text-align: center;
        }
        
        .upload-box {
            border: 2px dashed #333;
            padding: 30px 10px;
            margin-bottom: 20px;
            border-radius: 8px;
            transition: 0.3s;
        }
        .upload-box:active { border-color: var(--main-green); background: #1a1c23; }

        input[type="file"] { 
            width: 100%;
            font-size: 14px;
            color: #888;
        }

        button { 
            background: var(--main-green); 
            color: #000; 
            border: none; 
            padding: 18px; 
            font-weight: 800; 
            cursor: pointer; 
            border-radius: 8px; 
            font-size: 16px; 
            width: 100%; 
            transition: 0.2s;
            -webkit-tap-highlight-color: transparent;
        }
        button:active { transform: scale(0.98); background: #fff; }

        /* 進度條 */
        .progress-container { 
            display: none; 
            width: 100%; 
            background: #000; 
            height: 24px; 
            margin-top: 20px; 
            border-radius: 12px; 
            overflow: hidden; 
            border: 1px solid #333;
        }
        .progress-bar { width: 0%; height: 100%; background: var(--main-green); transition: width 0.1s; }
        .progress-text { margin-top: 8px; font-size: 12px; color: var(--main-green); font-family: monospace; }

        /* 戰報輸出區 */
        #report-container { 
            display: none; 
            background: var(--card-bg); 
            border: 1px solid #2a2d3a; 
            padding: 20px; 
            border-radius: 12px; 
            margin-top: 25px; 
            box-sizing: border-box;
        }

        /* 關鍵：解決手機版表格爆開問題 */
        .table-wrapper {
            width: 100%;
            overflow-x: auto; /* 橫向滑動 */
            -webkit-overflow-scrolling: touch;
            margin: 20px 0;
            border: 1px solid #333;
        }
        #result-content table { border-collapse: collapse; min-width: 500px; width: 100%; }
        #result-content th, #result-content td { padding: 12px; border: 1px solid #2a2d3a; font-size: 14px; text-align: left; }
        #result-content th { background: #1a1c23; color: var(--main-green); }
        
        #result-content h2, #result-content h3 { color: var(--main-green); font-size: 1.2em; border-left: 3px solid var(--main-green); padding-left: 10px; }
        #result-content blockquote { border-left: 4px solid var(--danger-red); background: #1a1c23; padding: 15px; margin: 20px 0; font-size: 14px; }

        @media (max-width: 600px) {
            body { padding: 5px; }
            .control-panel { padding: 15px; }
            #report-container { padding: 15px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略指揮中心</h1>
            <div class="engine-tag">CORE: GEMINI 3.1 FLASH // MOBILE-READY</div>
        </div>

        <div class="control-panel">
            <form id="uploadForm">
                <div class="upload-box">
                    <input type="file" name="file" id="fileInput" accept="audio/*" required>
                </div>
                <button type="submit" id="submitBtn">啟動多模態審計發射</button>
            </form>

            <div class="progress-container" id="progressContainer">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            <div class="progress-text" id="progressText"></div>
        </div>

        <div id="report-container">
            <div id="result-content"></div>
        </div>
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
                    progressText.innerText = `>>> 上傳中: ${percent}% [${(event.loaded / 1024 / 1024).toFixed(1)}MB]`;
                    if (percent === 100) {
                        progressText.innerText = '>>> 檔案已投抵 Zeabur，正在喚醒 Gemini 3.1 Flash...';
                    }
                }
            };

            xhr.onload = () => {
                const data = JSON.parse(xhr.responseText);
                if (xhr.status === 200 && data.status === 'success') {
                    // 將 Markdown 渲染，並自動為 table 加上包裹器
                    let rawHtml = marked.parse(data.report);
                    // 暴力修正：為所有 table 標籤包上一層滑動 div
                    let shieldedHtml = rawHtml.replace(/<table/g, '<div class="table-wrapper"><table').replace(/<\\/table>/g, '</table></div>');
                    
                    resultContent.innerHTML = shieldedHtml;
                    reportContainer.style.display = 'block';
                    progressText.innerText = '>>> 審計戰報噴發成功。';
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
