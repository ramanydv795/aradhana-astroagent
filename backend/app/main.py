from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from langchain_core.messages import HumanMessage
from graph import astro_graph
from state import BirthDetails
import json
import asyncio

app = FastAPI(title="Aradhana AstroAgent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    birth_details: Optional[BirthDetails] = None
    conversation_history: Optional[list] = []

class ChatResponse(BaseModel):
    response: str
    intent: Optional[str]
    tool_calls_made: Optional[list]

@app.get("/")
def root():
    return {"status": "ok", "message": "Aradhana AstroAgent is running ✨"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint."""
    try:
        from langchain_core.messages import HumanMessage, AIMessage

        # Build message history
        messages = []
        for msg in request.conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        messages.append(HumanMessage(content=request.message))

        # Run the graph
        result = await asyncio.to_thread(
            astro_graph.invoke,
            {
                "messages": messages,
                "birth_details": request.birth_details,
                "birth_chart": None,
                "daily_transits": None,
                "intent": None,
                "tool_outputs": None,
                "is_safe": True,
            }
        )

        # Get last AI message
        last_message = result["messages"][-1]
        response_text = last_message.content

        return ChatResponse(
            response=response_text,
            intent=result.get("intent"),
            tool_calls_made=[]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint — streams tokens as they're generated."""
    async def generate():
        try:
            from langchain_core.messages import HumanMessage, AIMessage

            messages = []
            for msg in request.conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

            messages.append(HumanMessage(content=request.message))

            # Stream from graph
            async for chunk in astro_graph.astream(
                {
                    "messages": messages,
                    "birth_details": request.birth_details,
                    "birth_chart": None,
                    "daily_transits": None,
                    "intent": None,
                    "tool_outputs": None,
                    "is_safe": True,
                },
                stream_mode="messages"
            ):
                if isinstance(chunk, tuple):
                    message_chunk, metadata = chunk
                    if hasattr(message_chunk, "content") and message_chunk.content:
                        data = json.dumps({
                            "type": "token",
                            "content": message_chunk.content
                        })
                        yield f"data: {data}\n\n"
                        await asyncio.sleep(0)

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )