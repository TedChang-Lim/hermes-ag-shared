import requests
import json
import base64
import os

API_KEY = "sk-sho2gjhe0thboan84dnepjy1lx2ueqpbw8yv6tjsmanna56r"
BASE_URL = "https://api.xiaomimimo.com/v1"
OUTPUT_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/tts_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_tts(text, voice_description, filename):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # assistant 역할만 사용하는 방식
    payload = {
        "model": "mimo-v2.5-tts",
        "messages": [
            {
                "role": "assistant",
                "content": f"[{voice_description}] {text}"
            }
        ]
    }
    
    print(f"[*] 생성 중: {filename}")
    print(f"    텍스트: {text[:50]}...")
    print(f"    목소리: {voice_description}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                audio_data = message.get("audio", {}).get("data")
                
                if audio_data:
                    audio_bytes = base64.b64decode(audio_data)
                    output_path = os.path.join(OUTPUT_DIR, f"{filename}.wav")
                    with open(output_path, "wb") as f:
                        f.write(audio_bytes)
                    print(f"    [OK] 저장 완료: {output_path}")
                    return True
                else:
                    content = message.get("content", "")
                    print(f"    [INFO] 응답: {json.dumps(result, ensure_ascii=False)[:300]}")
            else:
                print(f"    [ERROR] 응답 형식 오류")
        else:
            print(f"    [ERROR] HTTP {response.status_code}: {response.text[:300]}")
            
    except Exception as e:
        print(f"    [ERROR] 예외 발생: {e}")
    
    return False

# 테스트 1: 중년 남성
generate_tts(
    text="안녕하세요, 저는 이 프로젝트의 책임자입니다. 오늘 회의에서 중요한 결정을 내려야 합니다.",
    voice_description="중년 남성, 낮고 굵은 목소리, 차분하고 권위 있는 말투",
    filename="test_01_middleaged_man"
)

# 테스트 2: 20대 여성
generate_tts(
    text="안녕하세요! 오늘 날씨가 정말 좋네요. 함께 산책하면 좋을 것 같아요.",
    voice_description="20대 여성, 밝고 경쾌한 목소리, 활기찬 말투",
    filename="test_02_young_woman"
)

# 테스트 3: 과묵한 남자
generate_tts(
    text="그래. 알겠어. 하면 되는 거잖아.",
    voice_description="30대 남성, 굵고 낮은 목소리, 과묵하고 간결한 말투",
    filename="test_03_strong_silent"
)

print(f"\n[*] 완료. 결과: {OUTPUT_DIR}")
