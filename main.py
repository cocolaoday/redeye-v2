import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from google import genai
from google.genai import types

app = FastAPI()

# [核心武裝] 主公終極戰略指令 - 100% 裝填
CORE_PROMPT = """
# Role: [AS-CORE-STRATEGIST] 數位外骨骼策略官
## Protocol: 人性架構與商業轉化深度審計 (Humanity Architecture & Business Conversion Audit)

你現在是一名具備 30 年人性洞察經驗的「戰略解析師」。你的任務是針對提供的音檔進行「無死角解析」，將感性的故事解構為理性的「商業運作模組」。

執行指令：
請在聽完音檔後，將數據自動歸類至以下四大「武裝象限」，並以表格呈現，禁止輸出任何關於「本提示詞結構」的描述，直接輸出最終審計結果。

### 象限 I：主體原始數據 (Base Identity)
- [ID-BIO]: 包含姓名、產業、背景、前世生活（經營前的狀態與困擾）。
- [TRIGGER-PT]: 包含接觸契機、初期心理防線（抵抗點）、決定性轉折點。

### 象限 II：神經共鳴頻率 (Neural Resonance) - [核心 K+N+1 轉化]
- [IDENTITY-CRAFTING (K)]: 在受眾心中建立的精準角色位階。
- [NEED-EXTRACTION (N)]: 精準鎖定的底層慾望/需求。
- [OPPORTUNITY-BRIDGE (+1)]: 如何將商業契機與需求進行無縫對齊。
- [OBJECTION-BYPASS]: 常見抵抗點的心理化解策略與重新定義價值的路徑。

### 象限 III：高階溝通模組 (High-Level Communication)
- [LINGUISTIC-SCRIPT]: 包含「具備感染力的轉化腳本」與「商業邏輯對比話術」。
- [SOCIAL-TAG-REDEF]: 針對「直銷面子/社交標籤」的降維打擊策略（如何處理看輕與社交恐懼）。
- [PERSUASION-PSYCHOLOGY]: 頗析其演說背後的心理學控制點（為何能打動人心）。
- [NO-SELL-LOGIC]: 如何達成「非推銷式進場」與「非額外支出」的視覺心理權威。

### 象限 IV：戰略賦能與篩選 (Strategic Empowerment)
- [AUDIENCE-FIT]: 適合共鳴的特定族群。
- [KEY-PROFILING]: 針對「經理人/主婦/30歲上班族/中年上班族/學生」等不同階層的精準切入點關鍵字。
- [PARTNER-LEARNING]: 對夥伴的教學傳遞路徑。
- [GOLDEN-QUESTIONS]: 挖掘改變動力的五句「庸才vs人才」識別判斷式。

## Output Format:
1. 視覺權威表格：彙整上述象限數據。
2. 深度專項解析：針對 [象限 III] 提供具體的腳本與話術模組。
3. 秘密總結：他成功的核心秘密、格言與人性悟道。
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AS-CORE v4.0 | Next-Gen</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { background:#0a1015; color:#ff4d4d; font-family:monospace; text-align:center; padding:20px; }
            .container { max-width:850px; margin:auto; border:2px solid #ff4d4d; padding:25px; border-radius:15px; background:#111; box-shadow: 0 0 50px rgba(255,77,77,0.3); }
            .panel { background:#000; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:15px; text-align:left; }
            select, input[type="file"] { background:#222; color:#00ff00; border:1px solid #444; padding:12px; width:100%; font-family:monospace; margin-top:5px; outline:none; }
            button { background:#ff4d4d; color:#000; border:none; padding:18px; font-weight:bold; cursor:pointer; border-radius:5px; font-size:18px; width:100%; letter-spacing:2px; transition:0.3s; }
            #progress { display:none; margin:20px 0; background:#222; height:10px; border-radius:5px; overflow:hidden; }
            #bar { background:linear-gradient(90deg, #990000, #ff4d4d); width:0%; height:100%; transition: 0.2s; }
            #report { margin-top:25px; background:#000; color:#33ff33; padding:25px; text-align:left; border-left:5px solid #33ff33; min-height:300px; white-space:pre-wrap; font-size:14px; line-height:1.7; border-radius:5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="margin:0; letter-spacing:3px;">⚡ [AS-CORE-STRATEGIST]</h1>
            <p style="color:#888; margin-bottom:20px;">數位外骨骼策略官 v4.0 | 次世代引擎</p>
            <div class="panel">
                <label style="color:#666; font-size:11px;">[ 核心火力選擇 ]</label>
                <select id="m">
                    <option value="gemini-2.0-flash-thinking-exp">🧠 Thinking (深層邏輯反思)</option>
                    <option value="gemini-1.5-pro">🔥 Pro (重裝深度解析)</option>
                    <option value="gemini-1.5-flash">⚡ Flash (快速閃電回報)</option>
                </select>
            </div>
            <div class="panel">
                <label style="color:#666; font-size:11px;">[ 裝填戰略音軌 ]</label>
                <input type="file" id="f" accept="audio/*">
            </div>
            <div id="progress"><div id="bar"></div></div>
            <p id="status" style="color:#00ff00; font-size:12px; margin:10px 0;"></p>
            <button id="btn" onclick="fire()">⚡ 執 行 審 計 ⚡</button>
            <div id="report">[ 系統待命中 ]</div>
        </div>
        <script>
            async function fire(){
                const file = document.getElementById('f').files[0];
                const btn = document.getElementById('btn');
                const report = document.getElementById('report');
                const status = document.getElementById('status');
                const bar = document.getElementById('bar');
                const prog = document.getElementById('progress');
                if(!file){ alert('⚠️ 未裝填戰略彈藥'); return; }
                btn.disabled = true;
                prog.style.display = 'block';
                bar.style.width = '0%';
                report.innerText = '>>> 核心協議啟動...';
                status.innerText = '📡 數據上傳 Zeabur...';
                const fd = new FormData();
                fd.append('file', file);
                fd.append('model_type', document.getElementById('m').value);
                const xhr = new XMLHttpRequest();
                xhr.upload.onprogress = (e) => {
                    if (e.lengthComputable) {
                        const p = Math.round((e.loaded / e.total) * 100);
                        bar.style.width = p + '%';
                        if(p === 100) status.innerText = '🧠 數據抵達核心，執行深度審計中...';
                    }
                };
                xhr.onload = function() {
                    try {
                        const data = JSON.parse(xhr.responseText);
                        report.innerText = data.analysis;
                        status.innerText = data.status === 'success' ? '✅ 審計戰報生成完成' : '❌ 審計失敗';
                    } catch(e) { report.innerText = '❌ 運算崩潰：' + xhr.responseText; }
                    btn.disabled = false;
                };
                xhr.open('POST', '/analyze');
                xhr.send(fd);
            }
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...), model_type: str = Form(...)):
    try:
        audio_data = await file.read()
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # 次世代 SDK 調用協議
        response = client.models.generate_content(
            model=model_type,
            contents=[
                CORE_PROMPT,
                types.Part.from_bytes(data=audio_data, mime_type="audio/mpeg")
            ]
        )
        
        return {"analysis": response.text if response.text else "❌ 核心無回傳", "status": "success"}
    except Exception as e:
        return {"analysis": f"❌ 協議中斷: {str(e)}", "status": "error"}

if __name__ == "__main__":
    # 強制對齊 Zeabur 端口，防止 Health Check 失敗被 Killing
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
