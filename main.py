import uvicorn
from fastapi import FastAPI, WebSocket, Request
from starlette.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    mes_counter = 1
    while True:
        try:
            data = await websocket.receive_json()
            message = {'message': {'id': mes_counter, 'message': data['message']}}
            print(message)
            mes_counter += 1
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(e)
            await websocket.close()
            break


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
