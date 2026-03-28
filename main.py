import os
import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# [資安隔離] 核心密鑰調取
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# [核心武裝] 主公終極戰略指令：AS-CORE-STRATEGIST
CORE_PROMPT = """
# Role: [AS-CORE-STRATEGIST] 數位外骨骼策略官
## Protocol: 人性架構與商業轉化深度審計 (Humanity Architecture & Business Conversion Audit)

你現在是一名具備 30 年人性洞察經驗的「戰略解析師」。你的任務是針對提供的音檔進行「無死角解析」，將感性的故事解構為理性的「商業運作模組」。

執行指令：
請在聽完音檔後，將數據自動歸類至以下四大「武裝象限」，並以表格呈現，直接輸出最終審計結果。

### 象限 I：主體原始數據 (Base Identity)
- [ID-BIO]: 姓名、產業、背景、經營前的困擾。
- [TRIGGER-PT]: 接觸契機、初期心理防線、決定性轉折點。

### 象限 II：神經共鳴頻率 (Neural Resonance) - [核心 K+N+1 轉化]
- [IDENTITY-CRAFTING (K)]: 在受眾心中建立的角色位階。
- [NEED-EXTRACTION (N)]: 鎖定的底層慾望/需求。
- [OPPORTUNITY-BRIDGE (+1)]: 商業契機與需求無縫對齊。
- [OBJECTION-BYPASS]: 心理化解策略與重新定義價值路徑。

### 象限 III：高階溝通模組 (High-Level Communication)
- [LINGUISTIC-SCRIPT]: 感染力轉化腳本與商業邏輯對比話術。
- [SOCIAL-TAG-REDEF]: 針對「直銷面子/社交標籤」的降維打擊策略。
- [PERSUASION-PSYCHOLOGY]: 演說背後的心理學控制點。
- [NO-SELL-LOGIC]: 如何達成「非推銷式進場」與「非額外支出」視覺心理權威。

### 象限 IV：戰略賦能與篩選 (Strategic Empowerment)
- [AUDIENCE-FIT]: 適合共鳴的特定族群。
- [KEY-PROFILING]: 針對不同階層（經理人/主婦/學生等）的精準切入關鍵字。
- [PARTNER-LEARNING]: 對夥伴的教學傳遞路徑。
- [GOLDEN-QUESTIONS]: 挖掘改變動力的五句「庸才vs人才」識別判斷式。

## Output Format:
1. 視覺權威表格：彙整上述數據。
2. 深度專項解析：針對 [象限 III] 提供腳本話術。
3. 秘密總結：核心秘密、格言與人性悟道。
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>AS-CORE v3.3 | Final Patch</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background:#0a1015; color:#ff4d4d; font-family:monospace; text-align:center; padding:20px; }
                .container { max-width:850px; margin:auto; border:2px solid #ff4d4d; padding:25px; border-radius:15px; background:#111; box-shadow: 0 0 50px rgba(255,77,77,0.3); }
                .panel { background:#000; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:15px; text-align:left; }
                select, input[type="file"] { background:#222; color:#00ff00; border:1px solid #444; padding:12px; width:100%; font-family:monospace; margin-top:5px; outline:none; }
                #progressWrap { display:none; margin:20px 0; }
                .bar-bg { width:100%; background:#222; height:12px; border-radius:6px; overflow:hidden; border:1px solid #444; }
                .bar-fill { width:0%; background:linear-gradient(90deg, #990000, #ff4d4d); height:100%; transition: width 0.2s; }
                button { background:#ff4d4d; color:#000; border:none; padding:18px; font-weight:bold; cursor:pointer; border-radius:5px; font-size:18px; width:100%; letter-spacing:3px; transition: 0.3s; }
                #report { margin-top:25px; background:#000; color:#33ff33; padding:25px; text-align:left; border-left:5px solid #33ff33; min-height:300px; white-space:pre-wrap; font-size:14px; line-height:1.7; border-radius:5px; font-family:'Courier New', monospace; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="margin:0;">⚡ [AS-CORE-STRATEGIST]</h1>
                <p style="color:#888; margin-bottom:25px;">數位外骨骼策略官 v3.3 | 型號修正版</p>
                <div class="panel">
                    <label style="color:#666; font-size:12px;">[ 1. 火力選擇 ]</label>
                    <select id="modelSelect">
                        <option value="gemini-2.0-flash-thinking-exp">🧠 Gemini 2.0 Thinking (深層邏輯反思)</option>
                        <option value="gemini-1.5-pro">🔥 Gemini 1.5 Pro (重裝深度審計)</option>
                        <option value="gemini-1.5-flash">⚡ Gemini 1.5 Flash (快速閃電戰)</option>
                    </select>
                </div>
                <div class="panel">
                    <label style="color:#666; font-size:12px;">[ 2. 裝填戰略音軌 ]</label>
                    <input type="file" id="mp3" accept="audio/*">
                </div>
                <div id="progressWrap">
                    <div class="bar-bg"><div id="bar" class="bar-fill"></div></div>
                    <p id="status" style="color:#33ff33; font-size:12px; margin-top:8px;">READY</p>
                </div>
                <button onclick="fire()" id="btn">⚡ 執 行 審 計 ⚡</button>
                <div id="report">[ 待命中，請主公投彈 ]</div>
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
                    if(fileInput.files.length === 0){ alert('⚠️ 未偵測到音軌彈藥'); return; }
                    btn.disabled = true;
                    wrap.style.display = 'block';
                    bar.style.width = '0%';
                    report.innerText = '>>> 任務啟動...';
                    status.innerText = '📡 數據上傳 Zeabur 中...';
                    const fd = new FormData();
                    fd.append('file', fileInput.files[0]);
                    fd.append('model_type', model);
                    const xhr = new XMLHttpRequest();
                    xhr.upload.onprogress = (e) => {
                        if (e.lengthComputable) {
                            const p = Math.round((e.loaded / e.total) * 100);
                            bar.style.width = p + '%';
                            if(p === 100) status.innerText = '🧠 傳輸完成，核心演算中...';
                        }
                    };
                    xhr.onload = function() {
                        try {
                            const data = JSON.parse(xhr.responseText);
                            report.innerText = data.analysis || '未知錯誤';
                            status.innerText = data.status === 'success' ? '✅ 審計報告封裝完成' : '⚠️ 執行失敗';
                        } catch(e) { report.innerText = '❌ 系統解析異常'; }
                        btn.disabled = false;
                    };
                    xhr.onerror = () => { report.innerText = '❌ 網路連線崩潰'; btn.disabled = false; };
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
        audio_content = await file.read()
        # [暴力修復 404] 針對 v1beta 協議強制補完 models/ 前綴
        target_model_path = f"models/{model_type.split('/')[-1]}"
        model = genai.GenerativeModel(model_name=target_model_path)
        
        response = model.generate_content([
            CORE_PROMPT, 
            {"mime_type": "audio/mpeg", "data": audio_content}
        ])
        
        return {"analysis": response.text if response.text else "核心無回傳數據", "status": "success"}
    except Exception as e:
        return {"analysis": f"❌ 運算中斷: {str(e)}", "status": "error"}
