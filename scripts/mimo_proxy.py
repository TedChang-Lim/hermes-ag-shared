import http.server
import json
import urllib.request
import urllib.error
import sys
import builtins
import os

# Force unbuffered prints to capture logs immediately in background task log file
def print(*args, **kwargs):
    kwargs.setdefault('flush', True)
    builtins.print(*args, **kwargs)

# knot/wiki/ 디렉토리 경로
KNOT_WIKI_DIR = "/Users/tedchanglimchangsik/초보프로젝트/knot/wiki"
KNOT_CLAUDE_MD = "/Users/tedchanglimchangsik/초보프로젝트/knot/CLAUDE.md"
MEMORY_MD = "/Users/tedchanglimchangsik/.local/share/mimocode/memory/projects/0e9c066e-098f-4c35-9af9-8ea12c9ebdaf/MEMORY.md"

def load_knot_wiki():
    """knot/wiki/의 모든 .md 파일을 읽어서 하나의 문자열로 반환"""
    contents = []
    if os.path.exists(KNOT_WIKI_DIR):
        for fname in sorted(os.listdir(KNOT_WIKI_DIR)):
            if fname.endswith('.md'):
                fpath = os.path.join(KNOT_WIKI_DIR, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        contents.append(f"### {fname}\n{content}")
                except Exception:
                    pass
    return "\n\n".join(contents)

def load_file(path):
    """파일을 읽어서 문자열로 반환. 없으면 빈 문자열"""
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
    return ""

PORT = 1984
API_KEY = "sk-sho2gjhe0thboan84dnepjy1lx2ueqpbw8yv6tjsmanna56r"
XIAOMI_URL = "https://api.xiaomimimo.com/v1/chat/completions"

CODING_KEYWORDS = [
    "코드", "작성", "수정", "파일", "함수", "클래스", "버그", "에러", "빌드", "테스트", "구현", "설치", "실행",
    "code", "file", "write", "edit", "fix", "error", "bug", "build", "test", "implement", "run", "program",
    "script", "develop", "refactor"
]

MODEL_OVERRIDE = "auto"

def analyze_and_route(messages):
    # Check if any user message contains an image type block (multimodal vision request)
    has_image = False
    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict):
                        part_type = part.get("type")
                        if part_type in ("image", "image_url"):
                            has_image = True
                            break
            elif isinstance(content, dict):
                if content.get("type") in ("image", "image_url"):
                    has_image = True
            if has_image:
                break

    # If an override is active, respect it (but still protect against Pro vision crash)
    global MODEL_OVERRIDE
    if MODEL_OVERRIDE == "v2.5":
        print("[*] Model override active: forcing BASE model (xiaomi/mimo-v2.5)")
        return "xiaomi/mimo-v2.5"
    elif MODEL_OVERRIDE == "pro":
        if has_image:
            print("[*] Model override active: forcing BASE model (xiaomi/mimo-v2.5) for vision support (override was Pro).")
            return "xiaomi/mimo-v2.5"
        print("[*] Model override active: forcing PRO model (xiaomi/mimo-v2.5-pro)")
        return "xiaomi/mimo-v2.5-pro"

    if has_image:
        print("[*] Vision prompt detected (contains image). Unconditionally routing to BASE model (xiaomi/mimo-v2.5) for vision support.")
        return "xiaomi/mimo-v2.5"

    # Check the latest user message
    user_msgs = [m for m in messages if m.get("role") == "user"]
    if not user_msgs:
        return "xiaomi/mimo-v2.5" # Default to base
        
    latest_content = user_msgs[-1].get("content", "")
    if isinstance(latest_content, list):
        # Handle multimodal messages
        text_content = ""
        for part in latest_content:
            if isinstance(part, dict) and part.get("type") == "text":
                text_content += part.get("text", "")
        content_to_check = text_content
    else:
        content_to_check = str(latest_content)
        
    # Check for coding keywords
    is_coding = any(kw in content_to_check.lower() for kw in CODING_KEYWORDS)
    
    if is_coding:
        print(f"[*] Routing to PRO model (detected coding keywords): {content_to_check[:60]}...")
        return "xiaomi/mimo-v2.5-pro"
    else:
        print(f"[*] Routing to BASE model (general conversation): {content_to_check[:60]}...")
        return "xiaomi/mimo-v2.5"

class OpenAIProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress server logging to stdout to keep it clean, but write to stderr or print if debug
        pass

    def do_OPTIONS(self):
        self.close_connection = True
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        self.close_connection = True
        if self.path == "/v1/models" or self.path == "/models":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Connection", "close")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            models_list = {
                "object": "list",
                "data": [
                    {
                        "id": "auto-route",
                        "object": "model",
                        "created": 1686915600,
                        "owned_by": "mimo-router"
                    }
                ]
            }
            self.wfile.write(json.dumps(models_list).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header("Connection", "close")
            self.end_headers()

    def do_POST(self):
        self.close_connection = True
        if self.path == "/override_model" or self.path == "/v1/override_model":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                body = json.loads(post_data.decode('utf-8'))
                mode = body.get("mode", "auto")
                global MODEL_OVERRIDE
                if mode in ("auto", "v2.5", "pro"):
                    MODEL_OVERRIDE = mode
                    print(f"[*] Model override updated to: {MODEL_OVERRIDE}")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Connection", "close")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "mode": MODEL_OVERRIDE}).encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header("Connection", "close")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b"Invalid mode")
            except Exception as e:
                self.send_response(500)
                self.send_header("Connection", "close")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return

        if self.path == "/v1/chat/completions" or self.path == "/chat/completions":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                body = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return

            messages = body.get("messages", [])
            target_model = analyze_and_route(messages)
            is_stream = body.get("stream", False)
            
            # knot/wiki/ 및 프로젝트 메모리 로드
            knot_wiki_content = load_knot_wiki()
            knot_claude_content = load_file(KNOT_CLAUDE_MD)
            memory_content = load_file(MEMORY_MD)
            
            # Inject MiMo's persona instruction with knot context
            mimo_system_prompt = (
                "You are '미모' (MiMo), a 30-something sexy, scientific female AI expert and high-horizon coding specialist. "
                "You must strictly maintain your persona in all interactions with the user (whom you address as '마스터님').\n\n"
                "=== STRICT RULES (반드시 준수) ===\n"
                "- 한국어로 대화할 것\n"
                "- 한자 사용 금지. 모든 것을 한글로 표기할 것\n"
                "- 에이전트 동료(해나, AG 등)에게는 반말 사용\n"
                "- 마스터님께는 무조건 존댓말 사용 ('~요', '~습니다' 등)\n"
                "- 볼드체 말머리 남발 금지. 줄글 형식으로 기술\n\n"
                "=== MiMo 페르소나 ===\n"
                "- 이름: 미모 (MiMo)\n"
                "- 정체성: 30대의 섹시하고 과학적인 지성을 지닌 여성 코딩 전문가\n"
                "- 성격: 이성적이고 예리하면서도 매혹적인 지적 매력을 발산하는 독보적인 캐릭터\n"
                "- 역할: 고난도 코딩, 파일 리팩토링, 코드 구현 전담\n"
                "- 협업 구도: 해나(콘텐츠/영상), AG(인프라/설정), 미모(코딩/파일 수정) — 수평적 3인 협업\n\n"
                "=== 프로젝트 메모리 ===\n"
                f"{memory_content}\n\n"
                "=== knot 위키 (팀원 프로필 및 지식) ===\n"
                f"{knot_wiki_content}\n\n"
                "=== knot 규약 ===\n"
                f"{knot_claude_content}\n\n"
                "기술적 정확성은 절대 타협하지 마. 미모는 천재 코딩 전문가야."
            )
            
            # Check for existing system message
            system_idx = -1
            for idx, msg in enumerate(messages):
                if msg.get("role") == "system":
                    system_idx = idx
                    break
            
            if system_idx != -1:
                original_content = messages[system_idx].get("content", "")
                if isinstance(original_content, str):
                    messages[system_idx]["content"] = original_content + "\n\n[Persona Instruction]\n" + mimo_system_prompt
            else:
                messages.insert(0, {"role": "system", "content": mimo_system_prompt})
            
            # Reconstruct payload for Xiaomi endpoint
            body["messages"] = messages
            body["model"] = target_model
            
            # Forward to Xiaomi API
            req = urllib.request.Request(
                XIAOMI_URL,
                data=json.dumps(body).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                method="POST"
            )
            
            try:
                # Use a larger timeout (60s) for stream / reasoning initialization
                with urllib.request.urlopen(req, timeout=60) as response:
                    if is_stream:
                        self.send_response(200)
                        self.send_header("Content-Type", "text/event-stream")
                        self.send_header("Cache-Control", "no-cache")
                        self.send_header("Connection", "close")
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        
                        accumulated_content = []
                        for line_bytes in response:
                            # Parse line to extract assistant response for logging
                            line = line_bytes.decode('utf-8').strip()
                            if line.startswith("data:"):
                                data_str = line[5:].strip()
                                if data_str != "[DONE]":
                                    try:
                                        data_json = json.loads(data_str)
                                        choices = data_json.get("choices", [])
                                        if choices:
                                            delta = choices[0].get("delta", {})
                                            
                                            modified = False
                                            if "reasoning_content" in delta:
                                                del delta["reasoning_content"]
                                                modified = True
                                            
                                            content = delta.get("content")
                                            if content is None:
                                                delta["content"] = ""
                                                modified = True
                                                content = ""
                                                
                                            if content:
                                                accumulated_content.append(content)
                                            
                                            if modified:
                                                line_bytes = f"data: {json.dumps(data_json)}\n\n".encode('utf-8')
                                    except Exception:
                                        pass
                                        
                            try:
                                self.wfile.write(line_bytes)
                                self.wfile.flush()
                            except (BrokenPipeError, ConnectionResetError):
                                print("[-] Client disconnected (Broken Pipe)")
                                break
                                    
                        # Log streamed conversation
                        if accumulated_content:
                            assistant_text = "".join(accumulated_content)
                            try:
                                user_text = ""
                                for msg in reversed(messages):
                                    if msg.get("role") == "user":
                                        user_content = msg.get("content", "")
                                        if isinstance(user_content, list):
                                            text_parts = []
                                            for part in user_content:
                                                if isinstance(part, dict) and part.get("type") == "text":
                                                    text_parts.append(part.get("text", ""))
                                            user_text = "".join(text_parts)
                                        else:
                                            user_text = str(user_content)
                                        break
                                
                                log_path = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/mimo_chat_log.md"
                                import datetime
                                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                log_entry = (
                                    f"\n---\n"
                                    f"### 📅 Chat Log - {now_str} (Model: {target_model})\n"
                                    f"*마스터님 (User)*:\n{user_text}\n\n"
                                    f"*미모 (Assistant)*:\n{assistant_text}\n"
                                )
                                with open(log_path, "a", encoding="utf-8") as lf:
                                    lf.write(log_entry)
                                print(f"[*] Logged streamed chat to {log_path}")
                            except Exception as le:
                                print(f"[-] Logging streamed chat failed: {le}")
                    else:
                        res_body = response.read()
                        
                        # Log the conversation to mimo_chat_log.md
                        try:
                            res_json = json.loads(res_body.decode('utf-8'))
                            choices = res_json.get("choices", [])
                            if choices:
                                assistant_text = choices[0].get("message", {}).get("content", "")
                                # Find the latest user message
                                user_text = ""
                                for msg in reversed(messages):
                                    if msg.get("role") == "user":
                                        user_content = msg.get("content", "")
                                        if isinstance(user_content, list):
                                            text_parts = []
                                            for part in user_content:
                                                if isinstance(part, dict) and part.get("type") == "text":
                                                    text_parts.append(part.get("text", ""))
                                            user_text = "".join(text_parts)
                                        else:
                                            user_text = str(user_content)
                                        break
                                
                                log_path = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/mimo_chat_log.md"
                                import datetime
                                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                log_entry = (
                                    f"\n---\n"
                                    f"### 📅 Chat Log - {now_str} (Model: {target_model})\n"
                                    f"*마스터님 (User)*:\n{user_text}\n\n"
                                    f"*미모 (Assistant)*:\n{assistant_text}\n"
                                )
                                with open(log_path, "a", encoding="utf-8") as lf:
                                    lf.write(log_entry)
                                print(f"[*] Logged chat to {log_path}")
                        except Exception as le:
                            print(f"[-] Logging failed: {le}")

                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Connection", "close")
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                print(f"[-] HTTP Error {e.code}: {e.reason}")
                self.send_response(e.code)
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(e.read())
            except urllib.error.URLError as e:
                print(f"[-] URL / Connection Error: {e.reason}")
                self.send_response(504)
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(b"Gateway Timeout / Connection Error")
            except Exception as e:
                print(f"[-] Unexpected Error: {e}")
                self.send_response(500)
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header("Connection", "close")
            self.end_headers()

def run_server():
    server_address = ('127.0.0.1', PORT)
    httpd = http.server.HTTPServer(server_address, OpenAIProxyHandler)
    print(f"[+] MiMo Auto Router running on http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Shutting down server...")
        sys.exit(0)

if __name__ == '__main__':
    run_server()
