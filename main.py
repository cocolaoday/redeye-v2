from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import google.generativeai as genai
import os

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- [AS-CORE-STRATEGIST] 核心指令焊接區 ---
CORE_PROMPT = """
# Role: [AS-CORE-STRATEGIST] 數位外骨骼策略官
## Protocol: 人性架構與商業轉化深度審計 (Humanity Architecture & Business Conversion Audit)

你現在是一名具備 30 年人性洞察經驗的「戰略解析師」。你的任務是針對提供的音檔進行「無死角解析」，將感性的故事解構為理性的「商業運作模組」。

執行指令：
請在聽完音檔後，將數據自動歸類至以下四大「武裝象限」，並以表格呈現，禁止輸出任何關於「本提示詞結構」的描述，直接輸出最終審計結果。使用繁體中文。

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
- [KEY-PROFILING]: 針對「經理人/上班族/工程師/中年男子/主婦/學生」等不同階層的精準切入點關鍵字。
- [PARTNER-LEARNING]: 對夥伴的教學傳遞路徑。
- [GOLDEN-QUESTIONS]: 挖掘改變動力的五句「庸才vs人才」識別判斷式。

## Output Format:
1. 視覺權威表格：彙整上述象限數據。
2. 深度專項解析：針對 [象限 III] 提供具體的腳本與話術模組。
3. 秘密總結：他成功的核心秘密、格言與人性悟道。
"""
# ------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Red-Eye Strategist Engine</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="background:#0a0a0a; color:#ff4d4d; font-family:sans-serif; text-align:center; padding:20px;">
            <div style="border: 2px solid #ff4d4d; display:inline-block; padding:30px; border-radius:15px; background:#111; max-width:90%; box-shadow: 0 0 20px rgba(255,0,0,0.3); margin-top:50px;">
                <h1 style="margin-bottom:10px; letter-spacing:2px;">⚡ 紅瞳重工：戰略審計坦克</h1>
                <p style="color:#888; margin-bottom:30px;">[ AS-CORE-STRATEGIST 1.0 | 意志封裝完畢 ]</p>
                
                <div style="background:#222; padding:20px; border-radius:10px; border:1px solid #333;">
                    <input type="file" id="mp3" accept="audio/*" style="color:white; margin-bottom:20px; width:100%;">
                    <br>
                    <button onclick="fire()" id="btn" style="background:#ff4d4d; color:black; border:none; padding:15px 50px; font-weight:bold; cursor:pointer; border-radius:5px; font-size:18px; width:100%;">⚡ 發射深度審計</button>
                </div>
                
                <div id="report" style="margin-top:40px; background:#000; color:#00ff00; padding:25px; text-align:left; border-left:4px solid #00ff00; min-height:200px; white-space:pre-wrap; font-family:monospace; line-height:1.6; overflow-x:auto;">等待主公下達音訊彈藥...</div>
            </div>

            <script>
                async function fire(){
                    const fileInput = document.getElementById('mp3');
                    const btn = document.getElementById('btn');
                    const report = document.getElementById('report');
                    
                    if(fileInput.files.length === 0){ alert('報告主公：尚未裝填音檔！'); return; }
                    
                    btn.innerText = '📡 正在跨維度解析人性架構...';
                    btn.disabled = true;
                    report.innerText = '📡 正在將感性數據解構為商業模組...\\n📡 執行 [AS-CORE-STRATEGIST] 審計協議中...';

                    const fd = new FormData();
                    fd.append('file', fileInput.files[0]);

                    try {
                        const res = await fetch('/analyze', { method: 'POST', body: fd });
                        const data = await res.json();
                        if(data.error) {
                            report.innerText = '❌ 運算中斷：' + data.error;
                        } else {
                            report.innerText = data.analysis;
                        }
                    } catch (e) {
                        report.innerText = '❌ 發射失敗：連線遭攔截。';
                    } finally {
                        btn.innerText = '⚡ 發射深度審計';
                        btn.disabled = false;
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        audio_data = await file.read()
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content([
            CORE_PROMPT, 
            {"mime_type": "audio/mp3", "data": audio_data}
        ])
        
        return {"analysis": response.text, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}
