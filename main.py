from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"msg": "主公，新戰場通車成功！"}
