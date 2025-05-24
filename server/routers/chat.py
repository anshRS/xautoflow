from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from server.controllers.chat import graph  

router = APIRouter()

@router.websocket("/ws/chat/{client_id}")
async def websocket_realtime_chat_endpoint(
        websocket: WebSocket,
        client_id: str,
):         
    await websocket.accept()
                
    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("query")  

            async for event in graph.astream({
                "messages": [("user", query)]
            }, config={
                "configurable": {"thread_id": client_id}
            }, stream_mode="messages"):  
                await websocket.send_json({
                    "data": event[0].content,
                    "isBot": True
                })
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected.")
    