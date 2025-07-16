from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uuid
import json
from .services.chat_service import ChatService
from .services.auth_service import AuthService
from .models.schemas import ChatMessage, User

app = FastAPI(title="FAANG AI Chatbot", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
chat_service = ChatService()
auth_service = AuthService()

@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    """Process chat message and return AI response"""
    try:
        response = await chat_service.process_message(message)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            response = await chat_service.process_message(message)
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass