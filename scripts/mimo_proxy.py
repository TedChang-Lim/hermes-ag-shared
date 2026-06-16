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
            
            # Reconstruct payload for Xiaomi endpoint
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
