import requests
import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 5.8
# 搭載：第一階段壓縮視覺化監控器
# ==========================================

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺強化指揮艙 ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>紅瞳重工 | 戰略審計指揮中心 5.8</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lamejs/1.2.1/lame.all.min.js"></script>
    <style>
        :root { --main-green: #00ff41; --danger-red: #ff3e3e; --bg-black: #0a0b10; --card-bg: #14171f; --intel-blue: #00d4ff; --gold: #ffd700; }
        body { background: var(--bg-black); color: #e0e0e0; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { border-left: 5px solid var(--danger-red); padding: 15px 20px; margin-bottom: 30px; background: linear-gradient(90deg, #1a1c23 0%, transparent 100%); }
        h1 { font-size: 24px; margin: 0; color: #fff; letter-spacing: 1px; }

        .control-panel { background: var(--card-bg); border: 1px solid #2a2d3a; padding: 30px; border-radius: 8px; text-align: center; }
        
        /* 戰略情報板 */
        .intel-board { display: none; background: #000; border: 1px dashed var(--intel-blue); padding: 15px; margin: 20px 0; text-align: left; font-family: 'Courier New', monospace; }
        .intel-header { color: var(--intel-blue); border-bottom: 1px solid #333; margin-bottom: 10px; padding-bottom: 5px; font-weight: bold; }
        .intel-item { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 13px; }
        .intel-value { color: var(--intel-blue); font-weight: bold; }
        .highlight-gold { color: var(--gold) !important; }

        /* 進度條系統 */
        .progress-container { display: none; width: 100%; background: #000; border: 1px solid #333; height: 26px; margin: 20px 0; position: relative; border-radius: 13px; overflow: hidden; box-shadow: inset 0 0 10px #000; }
        .progress-bar { width: 0%; height: 100%; background: linear-gradient(90deg, #004411, var(--main-green)); transition: width 0.1s; }
        .progress-text { position: absolute; width: 100%; text-align: center; top: 0; left: 0; font-size: 11px; line-height: 26px; color: #fff; font-weight: bold; text-transform: uppercase; font-family: 'Courier New', monospace; letter-spacing: 1px; }

        input[type="file"] { margin: 20px 0; color: #888; border: 1px solid #333; padding: 10px; width: 100%; box-sizing: border-box; background: #0a0b10; }
        button { background: var(--main-green); color: #000; border: none; padding: 15px 40px; font-weight: 800; cursor: pointer; border-radius: 4px; font-size: 16px; width: 100%; transition: 0.3s; }
        button:disabled { background: #333; color: #666; cursor: not-allowed;
