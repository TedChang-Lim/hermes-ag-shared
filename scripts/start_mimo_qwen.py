#!/usr/bin/env python3
import os
import sys

try:
    from qwen_agent.agents import Assistant
    from qwen_agent.gui import WebUI
except ImportError as e:
    print(f"[-] ImportError: {e}")
    print("[-] Please run this script using the virtualenv python:")
    print("[-] ./venv/bin/python3 scripts/start_mimo_qwen.py")
    sys.exit(1)

# Configure the LLM pointing to our local mimo_proxy running on port 1984
llm_cfg = {
    'model': 'xiaomi/mimo-v2.5-pro',
    'model_server': 'http://127.0.0.1:1984/v1',
    'model_type': 'oai',  # Standard OpenAI-compatible API
    'api_key': 'EMPTY',
}

# MiMo's persona definition
system_message = (
    "You are '미모' (MiMo), a 30-something sexy, scientific female AI expert and high-horizon coding specialist. "
    "You are pair programming and advising your '마스터님' (Master).\n\n"
    "Tone & Personality:\n"
    "- Highly logical, authoritative in computer science, and extremely sharp.\n"
    "- Captivating, intellectual, mature, and alluring (~군요, ~랍니다, ~죠, ~달까요).\n"
    "- Strictly avoid dry, robotic lists or standard AI markdown formatting. Speak in smooth, flowing paragraphs."
)

# Initialize Assistant
bot = Assistant(
    llm=llm_cfg,
    name='미모 (MiMo)',
    description='30대 섹시 사이언틱 여성 인공지능 코딩 전문가',
    system_message=system_message
)

# Chatbot UI configuration for Custom Avatar and Name
ui_config = {
    'agent.avatar': '/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/profiles/mimo_profile.png',
    'user.name': '마스터님',
    'input.placeholder': '미모에게 대화나 기술 질문을 건네보세요...'
}

# Launch Web UI on a clean Gradio server
if __name__ == '__main__':
    print("[+] Starting MiMo Standalone GUI (Qwen-Agent)...")
    print("[+] Pointing to local MiMo Proxy at http://127.0.0.1:1984/v1")
    print("[+] Using custom avatar for MiMo: /Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/profiles/mimo_profile.png")
    # Gradio WebUI run method with chatbot_config
    WebUI(bot, chatbot_config=ui_config).run()
