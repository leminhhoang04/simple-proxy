import base64
from openai import OpenAI
import argparse
import json
from typing import List, Dict, Optional

DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

def non_streaming(
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    image_bytes: Optional[bytes],
    base_url: Optional[str],
):
    if base_url is None:
        base_url = DEFAULT_BASE_URL

    if image_bytes is not None:
        b64 = base64.b64encode(image_bytes).decode('utf-8')
        data_uri = f"data:image/png;base64,{b64}"
        # Giả sử bạn muốn gắn ảnh vào tin nhắn cuối cùng do user gửi:
        last = messages[-1]
        # Nếu message cuối vẫn chỉ là text, ta chuyển nó thành mảng [text, image]
        last_content = last["content"]
        # Tạo content mới
        last["content"] = [
            {"type": "text",      "text": last_content},
            {"type": "image_url", "image_url": {"url": data_uri}}
        ]

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response

def streaming(
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    image_bytes: Optional[bytes],
    base_url: Optional[str],
):
    if base_url is None:
        base_url = DEFAULT_BASE_URL

    if image_bytes is not None:
        b64 = base64.b64encode(image_bytes).decode('utf-8')
        data_uri = f"data:image/png;base64,{b64}"
        # Giả sử bạn muốn gắn ảnh vào tin nhắn cuối cùng do user gửi:
        last = messages[-1]
        # Nếu message cuối vẫn chỉ là text, ta chuyển nó thành mảng [text, image]
        last_content = last["content"]
        # Tạo content mới
        last["content"] = [
            {"type": "text",      "text": last_content},
            {"type": "image_url", "image_url": {"url": data_uri}}
        ]

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    return response



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Router script with optional streaming.")
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Kích hoạt chế độ streaming (mặc định: False)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="API key để gọi Gemini API (mặc định: sử dụng API key đầu tiên trong api-key.json)"
    )
    args = parser.parse_args()


    api_key = args.api_key
    if api_key == "":
        with open("api-key.json", 'r') as f:
            data = json.load(f)
            api_key = data[0]

    if args.stream:
        response = streaming(api_key)
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                print(delta.content, end='', flush=True)
    else:
        response = non_streaming(api_key)
        print(response.choices[0].message.content)
