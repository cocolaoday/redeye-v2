import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 6.7
# 緊急修補版：防禦 Python 3.13 字串解析潰縮
# 搭載引擎：Gemini 3.1 Flash
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標焊接
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺強化控制艙 (HTML UI) ---
# 這裡使用最穩定的字串拼接法，徹底爆破 SyntaxError
HTML_HEAD = r"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略指揮中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 10px; }
        .container { width: 100%; max-width: 900px; margin: 0 auto; box-sizing: border-box; }
        .header { border-left: 5px solid var(--danger-red); padding: 10px 15px; margin: 20px 0; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { color: #fff; margin: 0; font-size: clamp(18px, 5vw, 24px); text-transform: uppercase; letter-spacing: 2px; }
        .engine-tag { display: inline-block; background: #000; color: var(--main-green); padding: 2px 8px; border-radius: 3px; font-size: 10px; margin-top: 8px; border: 1px solid var(--main-green); font-family: monospace; }
        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 25px; border-radius: 12px; text-align: center; }
        .upload-box { border: 2px dashed #333; padding: 40px 10px; margin-bottom: 20px; border-radius: 8px; }
        button { background: var(--main-green); color: #000; border: none; padding: 18px; font-weight: 900; cursor: pointer; border-radius: 8px; font-size: 18px; width: 100%; }
        .progress-container { display: none; width: 100%; background: #000; height: 12px; margin-top: 20px; border-radius: 6px; overflow: hidden; border: 1px solid #333; }
        .progress-bar { width: 0%; height: 100%; background: var(--main-green); }
        .progress-text { margin-top: 10px; font-size: 12px; color: var(--main-green); font-family: monospace; }
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 20px; border-radius: 12px; margin-top: 25px; }
        .table-wrapper { width: 100%; overflow-x: auto; margin: 20px 0; border: 1px solid #333; }
        table { border-collapse: collapse; min-width: 600px; width: 100%; }
        th, td { padding: 12px; border: 1px solid #2a2d3a; font-size: 14px; text-align: left; }
        th { background: #1a1c23; color: var(--main-green); }
        blockquote { border-left: 4px solid var(--danger-red); background: #1a1c23; padding: 15px; margin: 20px 0; font-style: italic; }
        .save-btn { background: #333; color: #fff; margin-top: 30px; font-size: 14px; padding: 12px; border-radius: 5px; width: 100%; border: 1px solid #444; cursor: pointer; }
    </style>
</head>
"""

HTML_BODY = r"""
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略指揮中心</h1>
            <div class="engine-tag">ENGINE: GEMINI 3.1 FLASH // V6.7 PATCH</div>
        </div>
        <div class="control-panel">
            <form id="uploadForm">
                <div class="upload-box"><input type="file" name="file" id="fileInput" accept="audio/*" required></div>
                <button type="submit" id="submitBtn">啟動多模態審計發射</button>
            </form>
            <div class="progress-container" id="progressContainer"><div class="progress-bar" id="progressBar"></div></div>
            <div id="progressText" class="progress-text"></div>
        </div>
        <div id="report-container">
            <div id="result-content"></div>
            <button id="downloadBtn" class="save-btn">📥 將此戰略審計存為 HTML 檔案</button>
        </div>
    </div>
    <script>
        const form = document.getElementById('uploadForm');
        const btn = document.getElementById('submitBtn');
        const progressBar = document.getElementById('progressBar');
        const progressContainer = document.getElementById('progressContainer');
        const progressText = document.getElementById('progressText');
        const reportContainer = document.getElementById('report-container');
        const resultContent = document.getElementById('result-content');
        const downloadBtn = document.getElementById('downloadBtn');

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
            xhr.upload.onprogress = (ev) => {
                const percent = Math.round((ev.loaded / ev.total) * 100);
                progressBar.style.width = percent + '%';
                progressText.innerText = `>>> UPLOADING: ${percent}%`;
            };
            xhr.onload = () => {
                const data = JSON.parse(xhr.responseText);
                if (xhr.status === 200 && data.status === 'success') {
                    let html = marked.parse(data.report).replace(/<table/g, '<div class="table-wrapper"><table').replace(/<\/table>/g, '</table></div>');
                    resultContent.innerHTML = html;
                    reportContainer.style.display = 'block';
                    progressText.innerText = '>>> 戰略解析完成。';
                    reportContainer.scrollIntoView({ behavior: 'smooth'
