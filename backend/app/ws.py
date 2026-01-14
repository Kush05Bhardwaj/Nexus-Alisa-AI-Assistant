from fastapi import WebSocket, WebSocketDisconnect
from .llm_client import stream_llm_response
from .memory import MemoryBuffer
from .memory_long import save_memory, fetch_recent_memories
from .modes import set_mode, get_mode_prompt
from .emotion import extract_emotion
from .prompt import build_prompt
from typing import List

memory = MemoryBuffer()

# Store all connected WebSocket clients
connected_clients: List[WebSocket] = []

async def broadcast_message(message: str, exclude: WebSocket = None):
    """Send a message to all connected clients, optionally excluding one"""
    disconnected = []
    for client in connected_clients:
        if client != exclude:
            try:
                await client.send_text(message)
            except:
                disconnected.append(client)
    
    # Remove disconnected clients
    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)

async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"✅ Client connected. Total clients: {len(connected_clients)}")

    try:
        while True:
            user_input = await websocket.receive_text()

            if user_input.startswith("/mode"):
                set_mode(user_input.split()[-1])
                await websocket.send_text("[MODE CHANGED]")
                await websocket.send_text("[END]")
                continue


            memory.add("user", user_input)

            memories = fetch_recent_memories()
            system_prompt = build_prompt(get_mode_prompt(), memories)

            messages = [
                {"role": "system", "content": system_prompt},
                *memory.get()
            ]

            full_response = ""

            async for token in stream_llm_response(messages):
                full_response += token
                # Send to the requesting client
                await websocket.send_text(token)
                # Broadcast to other clients (like overlay)
                await broadcast_message(token, exclude=websocket)

            emotion, clean_text = extract_emotion(full_response)

            memory.add("assistant", clean_text)
            save_memory(emotion, clean_text)

            # Send emotion and end marker to all clients
            await websocket.send_text(f"[EMOTION]{emotion}")
            await broadcast_message(f"[EMOTION]{emotion}", exclude=websocket)
            
            await websocket.send_text("[END]")
            await broadcast_message("[END]", exclude=websocket)

    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(connected_clients)}")
