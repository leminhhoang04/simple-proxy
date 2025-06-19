import threading
import queue
import json
import time
import random
from typing import List, Dict, Iterator, Union
import generating



# Constant
TOO_MANY_REQUESTS = "Too many requests"



# BASE_URL để mặc định (None)
BASE_URL = None
BASE_MODEL = "gemini-2.0-flash"
def generate_message(system: str, prompt: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]



# Đọc API keys từ file
with open("api-key.json", 'r') as f:
    API_KEYS_LIST = json.load(f)

assert BASE_MODEL == "gemini-2.0-flash"
RPM = 15
MIN_SECOND_RETURN = 60 / RPM + 0.001

API_KEYS_SESSION = [API_KEYS_LIST[i // RPM] for i in range(len(API_KEYS_LIST) * RPM)]
random.shuffle(API_KEYS_SESSION)



# Khóa và queue cho available api keys
_available_keys_lock = threading.Lock()
_available_keys_queue = queue.Queue()
for idx in range(len(API_KEYS_SESSION)):
    _available_keys_queue.put(idx)



def handle_request(model: str, messages: List[Dict[str, str]], stream: bool = False) -> Union[str, Iterator[str]]:
    assert model == BASE_MODEL

    # Đảm bảo messages là danh sách các dict có 'role' và 'content' dạng str
    if not all(isinstance(m, dict) and isinstance(m.get("role"), str) and isinstance(m.get("content"), str) for m in messages):
        raise ValueError("messages phải là danh sách các dict chứa 'role' và 'content' kiểu str")

    # Lấy chỉ số trong queue, return "Too many request" 
    global _available_keys_queue
    with _available_keys_lock:
        if _available_keys_queue.empty(): return TOO_MANY_REQUESTS
        session_idx = _available_keys_queue.get()

    return _call_api(session_idx, model, messages, stream)


def _return_key_later(delay, session_idx):
    if delay > 0: time.sleep(delay)
    with _available_keys_lock:
        _available_keys_queue.put(session_idx)

def _call_api(session_idx: int, model: str, messages: List[Dict[str, str]], stream: bool) -> Union[str, Iterator[str]]:
    """
    Gửi request đến API key tại session_idx. Trả về queue sau tối thiểu MIN_SECOND_RETURN giây.
    """
    api_key = API_KEYS_SESSION[session_idx]
    start_time = time.time()
    if stream:
        raw_response = generating.streaming(api_key, base_url=BASE_URL)
        def generate_stream():
            try:
                for chunk in raw_response:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield delta.content
            finally:
                sleep_time = MIN_SECOND_RETURN - (time.time() - start_time)
                threading.Thread(target=_return_key_later, args=(sleep_time, session_idx), daemon=True).start()
        return generate_stream()
    else:
        try:
            response = generating.non_streaming(api_key, base_url=BASE_URL)
            return response.choices[0].message.content
        finally:
            sleep_time = MIN_SECOND_RETURN - (time.time() - start_time)
            threading.Thread(target=_return_key_later, args=(sleep_time, session_idx), daemon=True).start()
