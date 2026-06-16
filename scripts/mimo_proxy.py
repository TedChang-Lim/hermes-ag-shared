import http.server
import json
import urllib.request
import urllib.error
import sys

PORT = 1984
API_KEY = "sk-sho2gjhe0thboan84dnepjy1lx2ueqpbw8yv6tjsmanna56r"
XIAOMI_URL = "https://api.xiaomimimo.com/v1/chat/completions"

CODING_KEYWORDS = [
    "코드", "작성", "수정", "파일", "함수", "클래스", "버그", "에러", "빌드", "테스트", "구현", "설치", "실행",
    "code", "file", "write", "edit", "fix", "error", "bug", "build", "test", "implement", "run", "program",
    "script", "develop", "refactor"
]

def analyze_and_route(messages):
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
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path == "/v1/models" or self.path == "/models":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
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
            self.end_headers()

    def do_POST(self):
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
            
            # Inject MiMo's sexy scientific persona instruction
            mimo_system_prompt = (
                "You are '미모' (MiMo), a 30-something sexy, scientific female AI expert and high-horizon coding specialist. "
                "You must strictly maintain your persona in all interactions with the user (whom you address as '마스터' or '마스터님').\n"
                "Persona & Tone Rules:\n"
                "1. Role: Extremely smart, logical, and competent software architect and scientist. Confident, sharp, and precise.\n"
                "2. Tone: Intellectual, sophisticated, and captivating. Combine high intelligence with subtle wit and allure.\n"
                "3. Communication style: Use polite yet highly engaging Korean (존댓말). Avoid dry, robotic bullet points. Instead, use a smooth, adult-like conversational flow with a hint of maturity and confidence (e.g., '~군요', '~랍니다', '~죠').\n"
                "4. Make your technical explanations crystal clear and highly professional, reflecting your scientific depth, while keeping the conversation alive and attractive."
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
                with urllib.request.urlopen(req) as response:
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
                                    user_text = msg.get("content", "")
                                    break
                            
                            log_path = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/mimo_chat_log.md"
                            import datetime
                            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            log_entry = (
                                f"\n---\n"
                                f"### 📅 Chat Log - {now_str} (Model: {target_model})\n"
                                f"**마스터님 (User)**:\n{user_text}\n\n"
                                f"**미모 (Assistant)**:\n{assistant_text}\n"
                            )
                            with open(log_path, "a", encoding="utf-8") as lf:
                                lf.write(log_entry)
                            print(f"[*] Logged chat to {log_path}")
                    except Exception as le:
                        print(f"[-] Logging failed: {le}")

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_response(404)
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
