from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Union
from router import handle_request
from fastapi.responses import StreamingResponse

app = FastAPI()

# Cấu trúc input đầu vào
class Message(BaseModel):
    role: str
    content: str

class RequestPayload(BaseModel):
    #model: str
    messages: List[Message] = Field(
        example=[
            {"role": "system", "content": "Bạn là trợ lý AI."},
            {"role": "user", "content": "Hãy giới thiệu bản thân"}
        ]
    )
    stream: Union[bool, None] = False

# API endpoint nhận request
@app.post("/chat")
def chat(payload: RequestPayload):
    try:
        messages = [msg.dict() for msg in payload.messages]
        response = handle_request(
            #model=payload.model,
            model="gemini-2.0-flash",
            messages=messages,
            stream=payload.stream
        )

        # Nếu là stream (generator), wrap vào StreamingResponse
        if hasattr(response, '__iter__') and not isinstance(response, str):
            return StreamingResponse(response, media_type="text/plain")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
