from openai import OpenAI
import argparse
import json
from typing import List, Dict, Optional

DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_MESSAGE = [
    {"role": "system", "content": "Bạn là một trợ lý hữu ích."},
    {"role": "user", "content": "Hãy giới thiệu bản thân"}
]

def non_streaming(
    api_key: str,
    model: str = DEFAULT_MODEL,
    messages: List[Dict[str, str]] = DEFAULT_MESSAGE,
    base_url: Optional[str] = None,
):
    if base_url is None:
        base_url = DEFAULT_BASE_URL

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response

def streaming(
    api_key: str,
    model: str = DEFAULT_MODEL,
    messages: List[Dict[str, str]] = DEFAULT_MESSAGE,
    base_url: Optional[str] = None,
):
    if base_url is None:
        base_url = DEFAULT_BASE_URL

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
