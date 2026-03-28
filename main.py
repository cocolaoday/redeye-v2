from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import google.generativeai as genai
import os

app = FastAPI()

# 🛡️ 資安協議：從環境變數讀取 API KEY
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# ---------------------------------------------------------
# ⚔️ 核心戰略提示詞（主公意志封裝，前端不可見）
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 🏗️ APP 前端大門（含進度條與火力切換）
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>AS-CORE-STRATEGIST v2.0</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background:#0a1015; color:#ff4d4d; font-family:monospace; text-align:center; padding:30px 10px; }
                .container { max-width:800px; margin:auto; border:2px solid #ff4d4d; padding:30px; border-radius:15px; background:#111; box-shadow: 0 0 40px rgba(255,77,77,0.2); }
                .panel { background:#000; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:20px; text-align:left; }
                select, input[type="file"] { background:#222; color:#00ff00; border:1px solid #444; padding:10px; width:100%; font-family:monospace; margin-top:5px; }
                #progressWrap { display:none; margin-top:20px; }
                .bar-bg { width:100%; background:#222; height:10px; border-radius:5px; overflow:hidden; }
                .bar-fill { width:0%; background:#ff4d4d; height:100%; transition: width 0.2s; }
                button { background:#ff4d4d; color:#000; border:none; padding:18px; font-weight:bold; cursor:pointer; border-radius:5px; font-size:18px; width:100%; letter-spacing:2px; transition:0.3s; }
                button:disabled { background:#444; color:#888; cursor:not-allowed; }
                #report { margin-top:30px; background:#000; color:#33ff33; padding:20px; text-align:left; border-left:5px solid #33ff33; min-height:200px; white-space:pre-wrap; font-size:14px; line-height:1.6; border-radius:5px; overflow-x:auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="margin:0; letter-spacing:3px;">⚡ [AS-CORE-STRATEGIST]</h1>
                <p style="color:#888; margin-bottom:30px;">數位外骨骼策略官 v2.0</p>
                
                <div class="panel">
                    <label style="color:#666; font-size:12px;">[ 1. 火力切換 ]</label>
                    <select id="modelSelect">
                        <option value="gemini-1.5-flash-latest">⚡ Gemini 1.5 Flash (快速審計)</option>
                        <option value="gemini-1.5-pro-latest">🔥 Gemini 1.5 Pro (重裝深度解析)</option>
                    </select>
                </div>

                <div class="panel">
                    <label style="color:#666; font-size:12px;">[ 2. 裝填音軌 ]</label>
                    <input type="file" id="mp3" accept="audio/*">
                </div>

                <div id="progressWrap">
                    <div class="bar-bg"><div id="bar" class="bar-fill"></div></div>
                    <p id="status" style="color:#33ff33; font-size:12px; margin-top:8px;">準備緒...</p>
                </div>

                <button onclick="fire()" id="btn">⚡ 執 行 審 計 ⚡</button>
                
                <div id="report">[ 系統待命 ]</div>
            </div>

            <script>
                function fire(){
                    const fileInput = document.getElementById('mp3');
                    const btn = document.getElementById('btn');
                    const report = document.getElementById('report');
                    const model = document.getElementById('modelSelect').value;
                    const wrap = document.getElementById('progressWrap');
                    const bar = document.getElementById('bar');
                    const status = document.getElementById('status');

                    if(fileInput.files.length === 0){ alert('⚠️ 尚未裝填音檔！'); return; }
                    
                    btn.disabled = true;
                    wrap.style.display = 'block';
                    bar.style.width = '0%';
                    report.innerText = '[ 任務開始 ]';
                    status.innerText = '📡 傳輸中... (上傳進度)';

                    const fd = new FormData();
                    fd.append('file', fileInput.files[0]);
                    fd.append('model_type', model);

                    const xhr = new XMLHttpRequest();
                    xhr.upload.onprogress = (e) => {
                        if (e.lengthComputable) {
                            const p = Math.round((e.loaded / e.total) * 100);
                            bar.style.width = p + '%';
                            if(p === 100) status.innerText = '🧠 傳輸完成！Gemini 核心演算中 (預計 5-20 秒)...';
                        }
                    };

                    xhr.onload = function() {
                        try {
                            const data = JSON.parse(xhr.responseText);
                            if (xhr.status === 200 && data.status === 'success') {
                                report.innerText = data.analysis;
                                status.innerText = '✅ 審計報告解析完成。';
                            } else {
                                report.innerText = '❌ 運算中斷：' + (data.analysis || '未知錯誤');
                                status.innerText = '⚠️ 執行失敗。';
                            }
                        } catch(err) {
                            report.innerText = '❌ 系統錯誤：解析回傳數據失敗。';
                        }
                        btn.disabled = false;
                    };

                    xhr.open('POST', '/analyze');
                    xhr.send(fd);
                }
            </script>
        </body>
    </html>
    """

# ---------------------------------------------------------
# 🚀 APP 核心引擎（火力動態分流）
# ---------------------------------------------------------
@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...), model_type: str = Form(...)):
    try:
        audio_content = await file.read()
        
        # 🛡️ 根據前端選擇切換 Flash 或 Pro
        model = genai.GenerativeModel(model_type)
        
        # 發動審計
        response = model.generate_content([
            CORE_PROMPT, 
            {"mime_type": "audio/mpeg", "data": audio_content}
        ])
        
        if not response.text:
            return {"analysis": "核心未回傳數據，請確認音軌品質。", "status": "error"}

        return {"analysis": response.text, "status": "success"}
        
    except Exception as e:
        return {"analysis": str(e), "status": "error"}
