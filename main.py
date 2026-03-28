import requests, json, os, base64
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# ==========================================
# ⚡ 紅瞳重工：AS-CORE-COMMAND-CENTER 7.0
# 終極防禦版：Base64 封裝，徹底杜絕 SyntaxError
# 搭載引擎：Gemini 3.1 Flash
# ==========================================

load_dotenv()
app = FastAPI()

# 核心座標焊接
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = "https://eijidify.zeabur.app/v1"
USER_ID = "Eiji_Commander"

# --- 視覺化外骨骼 (Base64 壓縮訊號) ---
# 此字串代表了包含手機適配、進度條、HTML 導出的完整 UI
UI_B64 = (
    "PCFET0NUWVBFIGh0bWw+PGh0bWwgbGFuZz0iemgtVFciPjxoZWFkPjxtZXRhIGNoYXJzZXQ9IlVURi04Ij48dGl0bGU+6Iul556z6YeN5bel"
    "IHwg5oiw55Wl5oyH5o6u5Lit5b+DPC90aXRsZT48bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBp"
    "bml0aWFsLXNjYWxlPTEsIG1heGltdW0tc2NhbGU9MSwgdXNlci1zY2FsYWJsZT1ubyI+PHNjcmlwdCBzcmM9Imh0dHBzOi8vY2RuLmpzZGVs"
    "aXZyLm5ldC9ucG0vbWFya2VkL21hcmtlZC5taW4uanMiPjwvc2NyaXB0PjxzdHlsZT46cm9vdHstLW1haW4tZ3JlZW46IzAwZmY0MTstLWRh"
    "bmdlci1yZWQ6I2ZmM2UzZTs6LS1iZy1ibGFjazojMGEwYjEwOy0tY2FyZC1iZzojMTQxNzFmO31ib2R5e2JhY2tncm91bmQ6dmFyKC0tYmct"
    "YmxhY2spO2NvbG9yOiNlMGUwZTA7Zm9udC1mYW1pbHk6c3lzdGVtLXVpLHNhbnMtc2VyaWY7bWFyZ2luOjA7cGFkZGluZzoxMHB4Oy13ZWJr"
    "aXQtZm9udC1zbW9vdGhpbmc6YW50aWFsaWFzZWQ7fS5jb250YWluZXJ7d2lkdGg6MTAwJTttYXgtd2lkdGg6OTAwcHg7bWFyZ2luOjAgYXV0"
    "bztib3gtc2l6aW5nOmJvcmRlci1ib3g7fS5oZWFkZXJ7Ym9yZGVyLWxlZnQ6NXB4IHNvbGlkIHZhcigtLWRhbi1nZXItcmVkKTtwYWRkaW5n"
    "OjEwcHggMTVweDttYXJnaW46MjBweCAwO2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDkwZGVnLCMxYTFjMjMgMCUsdHJhbnNwYXJlbnQg"
    "MTAwJSk7fWgxe2NvbG9yOiNmZmY7bWFyZ2luOjA7Zm9udC1zaXplOmNsYW1wKDE4cHgsNXZ3LDI0cHgpO2xldHRlci1zcGFjaW5nOjJweDt0"
    "ZXh0LXRyYW5zZm9ybTp1cHBlcmNhc2U7fS5lbmdpbmUtdGFne2Rpc3BsYXk6aW5saW5lLWJsb2NrO2JhY2tncm91bmQ6IzAwMDtjb2xvcjp2"
    "YXIoLS1tYWluLWdyZWVuKTtwYWRkaW5nOjJweCA4cHg7Ym9yZGVyLXJhZGl1czozcHg7Zm9udC1zaXplOjEwcHg7bWFyZ2luLXRvcDo4cHg7"
    "Ym9yZGVyOjFweCBzb2xpZCB2YXIoLS1tYWluLWdyZWVuKTtmb250LWZhbWlseTptb25vc3BhY2U7fS5jb250cm9sLXBhbmVse2JhY2tncm91"
    "bmQ6dmFyKC0tY2FyZC1iZyk7Ym9yZGVyOjFweCBzb2xpZCAjMmEyZDNhO3BhYGRpbmc6MjVweDtib3JkZXItcmFkaXVzOjEycHg7dGV4dC1h"
    "bGlnbjpjZW50ZXI7fS51cGxvYWQtYm94e2JvcmRlcjoycHggZGFzaGVkICMzMzM7cGFkZGluZzozMHB4IDEwcHg7bWFyZ2luLWJvdHRvbToy"
    "MHB4O2JvcmRlci1yYWRpdXM6OHB4O31idXR0b257YmFja2dyb3VuZDp2YXIoLS1tYWluLWdyZWVuKTtjb2xvcjojMDAwO2JvcmRlcjpub25l"
    "O3BhYGRpbmc6MThweDtmb250LXdlaWdodDo5MDA7Y3Vyc29yOnBvaW50ZXI7Ym9yZGVyLXJhZGl1czo4cHg7Zm9udC1zaXplOjE4cHg7d2lk"
    "dGg6MTAwJTt9LnByb2dyZXNzLWNvbnRhaW5lcntkaXNwbGF5Om5vbmU7d2lkdGg6MTAwJTtiYWNrZ3JvdW5kOiMwMDA7aGVpZ2h0OjE2cHg7"
    "bWFyZ2luLXRvcDoyMHB4O2JvcmRlci1yYWRpdXM6OHB4O292ZXJmbG93OmhpZGRlbjtib3JkZXI6MXB4IHNvbGlkICMzMzM7fS5wcm9ncmVz"
    "cy1iYXJ7d2lkdGg6MCU7aGVpZ2h0OjEwMCU7YmFja2dyb3VuZDp2YXIoLS1tYWluLWdyZWVuKTt0cmFuc2l0aW9uOndpZHRoIDAuMXM7fS5w"
    "cm9ncmVzcy10ZXh0e21hcmdpbi10b3A6MTBweDtmb250LXNpemU6MTJweDtjb2xvcjp2YXIoLS1tYWluLWdyZWVuKTtmb250LWZhbWlseTpt"
    "b25vc3BhY2U7fSNyZXBvcnQtY29udGFpbmVye2Rpc3BsYXk6bm9uZTtiYWNrZ3JvdW5kOnZhcigtLWNhcmQtYmcpO2JvcmRlcjoxcHggc29s"
    "aWQgIzJhMmQzYTtwYWRkaW5nOjIwcHg7Ym9yZGVyLXJhZGl1czoxMnB4O21hcmdpbi10b3A6MjVweDt9LnRhYmxlLXdyYXBwZXJ7d2lkdGg6"
    "MTAwJTtvdmVyZmxvdy14OmF1dG87bWFyZ2luOjIwcHggMDtib3JkZXI6MXB4IHNvbGlkICMzMzM7fXRhYmxle2JvcmRlci1jb2xsYXBzZTpj"
    "b2xsYXBzZTttaW4td2lkdGg6NjAwcHg7d2lkdGg6MTAwJTtiYWNrZ3JvdW5kOiMwZjExMTc7fXRoLHRke3BhYGRpbmc6MTJweDtib3JkZXI6"
    "MXB4IHNvbGlkICMyYTJkM2E7Zm9udC1zaXplOjE0cHg7dGV4dC1hbGlnbjpsZWZ0O310aHtiYWNrZ3JvdW5kOiMxYTFjMjM7Y29sb3I6dmFy"
    "KC0tbWFpbi1nZWVuKTt9YmxvY2txdW90ZXtib3JkZXItbGVmdDo0cHggc29saWQgdmFyKC0tZGFuLWdlci1yZWQpO2JhY2tncm91bmQ6IzFh"
    "MWMyMztwYWRkaW5nOjE1cHg7bWFyZ2luOjIwcHggMDtmb250LXN0eWxlOml0YWxpYzt9LnNhdmUtYnRue2JhY2tncm91bmQ6IzMzMztjb2xv"
    "cjojZmZmO21hcmdpbi10b3A6MzBweDtmb250LXNpemU6MTRweDtwYWRkaW5nOjEycHg7Ym9yZGVyLXJhZGl1czo1cHg7d2lkdGg6MTAwJTti"
    "b3JkZXI6MXB4IHNvbGlkICM0NDQ7Y3Vyc29yOnBvaW50ZXI7fTwvc3R5bGU+PC9oZWFkPjxib2R5PjxkaXYgY2xhc3M9ImNvbnRhaW5lciI+"
    "PGRpdiBjbGFzcz0iaGVhZGVyIj48aDE+6Iul556z6YeN5belIOaImOeVpeoyh+aOruLit5b+DPC9oMT48ZGl2IGNsYXNzPSJlbmdpbmUtdGFn"
    "Ij5FTkdJTkU6IEdFTUlOSSAzLjEgRkxBU0ggLy8gVjcuMCBCUE88L2Rpdj48L2Rpdi4+PGRpdiBjbGFzcz0iY29udHJvbC1wYW5lbCI+PGZv"
    "cm0gaWQ9InVwbG9hZEZvcm0iPjxkaXYgY2xhc3M9InVwbG9hZC1ib3giPjxpbnB1dCB0eXBlPSJmaWxlIiBuYW1lPSJmaWxlIiBpZD0iZmls"
    "ZUlucHV0IiBhY2NlcHQ9ImF1ZGlvLypSIHJlcXVpcmVkPjwvZGl2PjxidXR0b24gdHlwZT0ic3VibWl0IiBpZD0ic3VibWl0QnRuIj7vlp/l"
    "i6pW6ZmoYXVkby3li7npmrqitneeZvOWwhDwvYnV0dG9uPjwvZm9ybT48ZGl2IGNsYXNzPSJwcm9ncmVzcy1jb250YWluZXIiIGlkPSJwcm9n"
    "cmVzc0NvbnRhaW5lciI+PGRpdiBjbGFzcz0icHJvZ3Jlc3MtYmFyIiBpZD0icHJvZ3Jlc3MtYmFyIj48L2Rpdj48L2Rpdj48ZGl2IGlkPSJw"
    "cm9ncmVzc1RleHQiIGNsYXNzPSJwcm9ncmVzcy10ZXh0Ij48L2Rpdj48L2Rpdj48ZGl2IGlkPSJyZXBvcnQtY29udGFpbmVyIj48ZGl2IGlk"
    "PSJyZXN1bHQtY29udGVudCI+PC9kaXY+PGJ1dHRvbiBpZD0iZG93bmxvYWRCdG4iIGNsYXNzPSJzYXZlLWJ0biI+48SemCDlsGatpOaImOago"
    "+WtmOeCuiBIVE1MIOaar+moizwvYnV0dG9uPjwvZGl2PjwvZGl2PjxzY3JpcHQ+Y29uc3QgZm9ybT1kb2N1bWVudC5nZXRFbGVtZW50QnlJ"
    "ZCgndXBsb2FkRm9ybScpO2NvbnN0IGJ0bj1kb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc3VibWl0QnRuJyk7Y29uc3QgcHJvZ3Jlc3NDb250"
    "YWluZXI9ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3Byb2dyZXNzQ29udGFpbmVyJyk7Y29uc3QgcHJvZ3Jlc3NCYXI9ZG9jdW1lbnQuZ2V0"
    "RWxlbWVudEJ5SWQoJ3Byb2dyZXNzLWJhcicpO2NvbnN0IHByb2dyZXNzVGV4dD1kb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncHJvZ3Jlc3NU"
    "ZXh0Jyk7Y29uc3QgcmVwb3J0Q29udGFpbmVyPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZXBvcnQtY29udGFpbmVyJyk7Y29uc3QgcmVz"
    "dWx0Q29udGVudD1kb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVzdWx0LWNvbnRlbnQnKTtjb250IGRvd25sb2FkQnRuPWRvY3VtZW50Lmdl"
    "dEVsZW1lbnRCeUlkKCdkb3dubG9hZEJ0bicpO2Zvcm0ub25zdWJtaXQ9KGUpPT57ZS5wcmV2ZW50RGVmYXVsdCgpO2NvbnN0IGZpbGU9ZG9j"
    "dW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2ZpbGVJbnB1dCcpLmZpbGVzWzBdO2lmKCFmaWxlKXJldHVybjtidG4uc3R5bGUuZGlzcGxheT0nbm9u"
    "ZSc7cHJvZ3Jlc3NDb250YWluZXIuc3R5bGUuZGlzcGxheT0nYmxvY2snO3JlcG9ydENvbnRhaW5lci5zdHlsZS5kaXNwbGF5PSdub25lJztj"
    "b25zdCBmb3JtRGF0YT1uZXcgRm9ybURhdGEoKTtmb3JtRGF0YS5hcHBlbmQoJ2ZpbGUnLGZpbGUpO2NvbnN0IHhoci1uZXcgWE1MSHR0cFJl"
    "cXVlc3QoKTt4aHIudXBsb2FkLm9ucHJvZ3Jlc3M9KGV2KT0+e2NvbnN0IHBlcmNlbnQ9TWF0aC5yb3VuZCgoZXYubG9hZGVkL2V2LnRvdGFs"
    "KSoxMDApO3Byb2dyZXNzQmFyLnN0eWxlLndpZHRoPXBlcmNlbnQrJyUnO3Byb2dyZXNzVGV4dC5pbm5lclRleHQ9YD4+PiBVUExPQURJTkc6"
    "ICR7cGVyY2VudH0lYDsgfTt4aHIub25sb2FkPSgpPT57Y29uc3QgZGF0YT1KU09OLnBhcnNlKHhoci5yZXNwb25zZVRleHQpO2lmKHhoci5z"
    "dGF0dXM9PT0yMDAmJmRhdGEuc3RhdHVzPT09J3N1Y2Nlc3MnKXtsZXQgaHRtbD1tYXJrZWQucGFyc2UoZGF0YS5yZXBvcnQpLnJlcGxhY2Uo"
    "Lzx0YWJsZS9nLCc8ZGl2IGNsYXNzPSJ0YWJsZS13cmFwcGVyIj48dGFibGUnKS5yZXBsYWNlKC88XC90YWJsZT4vZywnPC90YWJsZT48L2Rp"
    "dj4nKTtyZXN1bHRDb250ZW50LmlubmVySFRNTD1odG1sO3JlcG9ydENvbnRhaW5lci5zdHlsZS5kaXNwbGF5PSdibG9jayc7cHJvZ3Jlc3NU"
    "ZXh0LmlubmVyVGV4dD0nPj4+IOWpneatneeWrumonOeZvOWwhOaIkOWKny4nO3JlcG9ydENvbnRhaW5lci5zY3JvbGxJbnRvVmlldyh7YmVo"
    "YXZpb3I6J3Ntb290aCd9KTt9ZWxzZXthbGVydCgi5pWF6ZqcOiAiK0pTT04uc3RyaW5naWZ5KGRhdGEuZXJyb3IpKTtidG4uc3R5bGUuZGlz"
    "cGxheT0nYmxvY2snO319O3hoci5vcGVuKCdQT1NUJywnL3VwbG9hZC1hbmQtcnVuJyx0cnVlKTt4aHIuc2VuZChmb3JtRGF0YSk7fTtkb3du"
    "bG9hZEJ0bi5vbmNsaWNrPSgpPT57Y29uc3QgY29udGVudD1yZXN1bHRDb250ZW50LmlubmVySFRNTDtjb25zdCBmdWxsSHRtbD1gPGh0bWw+"
    "PGhlYWQ+PG1ldGEgY2hhcnNldD0iVVRGLTgiPjxzdHlsZT5ib2R5e2JhY2tncm91bmQ6IzBhMGIxMDtjb2xvcjojZTBlMGUwO2ZvbnQtZmFt"
    "aWx5OnNhbnMtc2VyaWY7cGFkZGluZzoyMHB4O310YWJsZXtib3JkZXItY29sbGFwc2U6Y29sbGFwc2U7d2lkdGg6MTAwJTttYXJnaW46MjBw"
    "eCAwO310aCx0ZHtib3JkZXI6MXB4IHNvbGlkICMzMzM7cGFkZGluZzoxMnB4O310aHtiYWNrZ3JvdW5kOiMxYTFjMjM7Y29sb3I6IzAwZmY0"
    "MTt9YmxvY2txdW90ZXtib3JkZXItbGVmdDo0cHggc29saWQgI2ZmM2UzZTtiYWNrZ3JvdW5kOiMxNDE3MWY7cGFkZGluZzoxNXB4O308L3N0"
    "eWxlPjwvaGVhZD48Ym9keT4ke2NvbnRlbnR9PC9ib2R5PjwvaHRtbD5gO2NvbnN0IGJsb2I9bmV3IEJsb2IoW2Z1bGxIdG1sXSx7dHlwZTon"
    "dGV4dC9odG1sJ30pO2NvbnN0IGxpbms9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnYScpO2xpbmsuaHJlZj1VUkwuY3JlYXRlT2JqZWN0VVJM"
    "KGJsb2IpO2xpbmsuZG93bmxvYWQ9YOe0hem瞳5oiw5aCxXyR7bmV3IERhdGUoKS5nZXRUaW1lKCl9Lmh0bWxgO2xpbmsuY2xpY2soKTt9Ozwv"
    "c2NyaXB0PjwvYm9keT48L2h0bWw+"
)

@app.get("/", response_class=HTMLResponse)
async def index():
    # 徹底隔離語法解析：在運行時才還原 UI
    decoded_html = base64.b64decode(UI_B64).decode("utf-8")
    return decoded_html.replace("{commander}", USER_ID)

@app.post("/upload-and-run")
async def upload_and_run(file: UploadFile = File(...)):
    if not API_KEY: return {"status": "failed", "error": "API_KEY Missing"}
    try:
        # 上傳到 Dify
        f_data = await file.read()
        up_res = requests.post(
            f"{BASE_URL}/files/upload", 
            headers={"Authorization": f"Bearer {API_KEY}"}, 
            files={"file": (file.filename, f_data, file.content_type)}
        )
        up_res.raise_for_status()
        f_id = up_res.json().get("id")
        
        # 觸發工作流
        payload = {
            "inputs": {"audio_input": [{"transfer_method": "local_file", "upload_file_id": f_id, "type": "audio"}]},
            "response_mode": "blocking", "user": USER_ID
        }
        wf_res = requests.post(
            f"{BASE_URL}/workflows/run", 
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, 
            data=json.dumps(payload)
        )
        wf_res.raise_for_status()
        
        report = wf_res.json().get("data", {}).get("outputs", {}).get("戰報", "解析失敗")
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
