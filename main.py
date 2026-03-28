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
- [NO-SELL-LOGIC]: 「非推銷式進場」與「非額外支出」視覺心理權威。

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
            <title>AS-CORE v3.2 | Final Stability</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background:#0a1015; color:#ff4d4d; font-family:monospace; text-align:center; padding:20px; }
                .container { max-width:850px; margin:auto; border:2px solid #ff4d4d; padding:25px; border-radius:15px; background:#111; box-shadow: 0 0 50px rgba(255,77,77,0.3); }
                .panel { background:#000; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:15px;
