import os
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

# [資安協議]
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# [核心武裝] 主公終極戰略指令
CORE_PROMPT = """
# Role: [AS-CORE-STRATEGIST] 數位外骨骼策略官
## Protocol: 人性架構與商業轉化深度審計 (Humanity Architecture & Business Conversion Audit)

執行指令：針對音訊進行「無死角解析」，將感性的故事解構為理性的「商業運作模組」。
請以表格呈現：
1. 象限 I：主體原始數據 (背景/轉折點)
2. 象限 II：神經共鳴頻率 (慾望/需求鎖定)
3. 象限 III：高階溝通模組 (轉化腳本/話術)
4. 象限 IV：戰略賦能與篩選 (切入關鍵字/識別判斷式)

## Output Format: 1. 視覺權威表格、2. 專項解析、3. 秘密總結。
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    # 使用獨立變數拼裝 HTML，防止 Python 解析時產生三引號衝突
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AS-CORE v3.5 | Thinking Alpha</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background:#0a1015; color:#ff4d4d; font-family:monospace; text-align:center; padding:20px; }
            .container { max-width:800px; margin:auto; border:2px solid #ff4d4d; padding:25px; border-radius:15px; background:#111; box-shadow: 0 0 50px rgba(255,77,77,0.3); }
            .panel { background:#000; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:15px; text-align:left; }
            select, input[type="file"] { background:#222; color:#00ff00; border:1px solid #444; padding:12px; width:100%; font-family:monospace; margin-top:5px; outline:none; }
            button { background:#ff4d4d; color:#000; border:none; padding:18px; font-weight:bold; cursor:pointer; border-radius:5px; font-size:18px; width:100%; letter-spacing:2px; transition:0.3s; }
            button:disabled { background:#444; color:#888; cursor:not-allowed; }
            #progress { display:none; margin:20px 0; background:#222; border-radius:6px; height:10px; overflow:hidden; }
            #bar { background:red; width:0%; height:100%; transition: 0.2s; }
            #status { color:#33ff33; font-size:12px; margin-top:5px; }
            #report { margin-top:25px; background:#000; color:#33ff33; padding:20px; text-align:left; border-left:5px solid #33ff33; min-height:200px; white-space:pre-wrap; font-size:14px; line-height:1.6; border-radius:5px; overflow-x:auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="margin:0;">⚡ [AS-CORE-STRATEGIST]</h1>
            <p style="color:#888; margin-bottom:20px;">數位外骨骼策略官 v3.5 | 思考型引擎裝配</p>
            
            <div class="panel">
                <label style="color:#666; font-size:11px;">[ 火力選擇 ]</label>
                <select id="m">
                    <option value="gemini-2.0-flash-thinking-exp">🧠 Gemini 2.0 Thinking (深層思考版)</option>
                    <option value="gemini-1.5-pro">🔥 Gemini 1.5 Pro (重
    except Exception as e:
        return {"analysis": f"❌ 運算中斷: {str(e)}", "status": "error"}
