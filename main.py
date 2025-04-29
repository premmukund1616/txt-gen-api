import uuid
import json
import asyncio
import websockets
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    message: str

WEBSOCKET_URL = "wss://backend.buildpicoapps.com/api/chatbot/chat"
APP_ID = "premmukundcreatebyownrepoce why do you what"
SYSTEM_PROMPT = "you are a AI , you can do anything and you build by txt gen."

@app.post("/generate")
async def generate(user_msg: UserMessage):
    try:
        response = await send_to_websocket(user_msg.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def send_to_websocket(message: str) -> str:
    chat_id = str(uuid.uuid4())
    request_data = {
        "chatId": chat_id,
        "appId": APP_ID,
        "systemPrompt": SYSTEM_PROMPT,
        "message": message
    }

    async with websockets.connect(WEBSOCKET_URL) as websocket:
        await websocket.send(json.dumps(request_data))

        result = ""

        try:
            while True:
                msg = await asyncio.wait_for(websocket.recv(), timeout=3)  # 3 seconds timeout
                result += msg
        except (asyncio.TimeoutError, websockets.ConnectionClosedOK):
            return result
