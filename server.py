from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, Field
from typing import List, Dict, Union
from router import handle_request
from fastapi.responses import StreamingResponse
import shutil
import json
import os


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
            model="gemini-2.5-flash",
            messages=messages,
            stream=payload.stream
        )

        # Nếu là stream (generator), wrap vào StreamingResponse
        if hasattr(response, '__iter__') and not isinstance(response, str):
            return StreamingResponse(response, media_type="text/plain")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# API endpoint nhận request
@app.post("/face-emotion")
async def chat(
    image: UploadFile = File(
        ...,
        description="Support eight emotions: Happy, Sad, Angry, Surprised, Scared, Disgusted, Confused, and Neutral."
    ),
):
    try:
        messages = [
            {"role":"system", "content":"Respond with ONE of the following eight emotions: Happy, Sad, Angry, Surprised, Scared, Disgusted, Confused, or Neutral."},
            {"role":"user","content":"Identify the emotion of the person in the attached image."}
        ]
        stream = False

        img_bytes = await image.read() if image is not None else None
        response = handle_request(
            model="gemini-2.5-flash",
            messages=messages,
            image_bytes=img_bytes,
            stream=stream
        )

        if hasattr(response, '__iter__') and not isinstance(response, str):
            return StreamingResponse(response, media_type="text/plain")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#UPLOAD_FOLDER = "uploaded_images"
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#@app.post("/upload")
#async def upload_image(file: UploadFile = File(...)):
#    file_path = f"{UPLOAD_FOLDER}/{file.filename}"
#    with open(file_path, "wb") as buffer:
#        shutil.copyfileobj(file.file, buffer)
#    return {"filename": file.filename, "path": file_path}
