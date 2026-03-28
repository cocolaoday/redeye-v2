import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 6.5
# 全平台適配 | 物理進度條 | HTML 戰報導出
# 搭載引擎：Gemini 3.1 Flash
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標焊接
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# 使用 r""" 原始字串防止 Python 3.13 轉義字元報錯
HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略指揮中心</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 10px; -webkit-font-smoothing: antialiased; }
        .container { width: 100%; max-width: 900px; margin: 0 auto; box-sizing: border-box; }
        
        /* 標題與位階標籤 */
        .header { border-left: 5px solid var(--danger-red); padding: 10px 15px; margin: 20px 0; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { color: #fff; margin: 0; font-size: clamp(18px, 5vw, 24px); text-transform: uppercase; letter-spacing: 2px; }
        .engine-tag { display: inline-block; background: #000; color: var(--main-green); padding: 2px 8px; border-radius: 3px; font-size: 10px; margin-top: 8px; border: 1px solid var(--main-green); font-family: monospace; }

        /* 控制艙 */
        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .upload-box { border: 2px dashed #333; padding: 40px 10px; margin-bottom: 20px; border-radius: 8px; transition: 0.3s; }
        input[type="file"] { width: 100%; color: #888; font-size: 14px; }
        button { background: var(--main-green); color: #000; border: none; padding: 18px; font-weight: 900; cursor: pointer; border-radius: 8px; font-size: 18px; width: 100%; transition: 0.2s; box-shadow: 0 4px 0 #008822; }
        button:active { transform: translateY(2px); box-shadow: none; background: #fff; }

        /* 物理進度感應器 */
        .progress-container { display: none; width: 100%; background: #000; height: 16px; margin-top: 20px; border-radius: 8px; overflow: hidden; border: 1px solid #333; }
        .progress-bar { width: 0%; height: 100%; background: linear-gradient(90deg, #004411, var(--main-green)); transition: width 0.1s; }
        .progress-text { margin-top: 10px; font-size: 12px; color: var(--main-green); font-family: 'Courier New', monospace; font-weight: bold; }

        /* 戰報輸出與美化 */
        #report-container { display: none; background: var(--card-bg); border: 1px solid #2a2d3a; padding: 20px; border-radius: 12px; margin-top: 25px; position: relative; }
        .table-wrapper { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 20px 0; border: 1px solid #333; }
        table { border-collapse: collapse; min-width: 600px; width: 100%; background: #0f1117; }
        th, td { padding: 12px; border: 1px solid #2a2d3a; font-size: 14px; text-align: left; }
        th { background: #1a1c23; color: var(--main-green); text-transform: uppercase; }
        blockquote { border-left: 4px solid var(--danger-red); background: #1a1c23; padding: 15px 20px; margin: 20px 0; font-style: italic; color: #fff; }
        h2, h3 { color: var(--main-green); border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 30px; }

        /* 資產導出按鈕 */
        .save-btn { background: #333; color: #fff; margin-top: 30px; font-size: 14px; padding: 12px; border: 1px solid #444; width: auto; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>紅瞳重工 戰略指揮中心</h1>
            <div class="engine-tag">ENGINE: GEMINI 3.1 FLASH // PROTOCOL: AS-CORE-6.5</div>
        </div>

        <div class="control-panel">
            <form id="uploadForm">
                <div class="upload-box">
                    <input type="file" name="file" id="fileInput" accept="audio/*" required>
                </div>
                <button type="submit" id="submitBtn">啟動多模態審計發射</button>
            </form>

            <div class="progress-container" id="progressContainer"><div class="progress-bar" id="progressBar"></div></div>
            <div id="progressText" class="progress-text"></div>
        </div>

        <div id="report-container">
            <div id
