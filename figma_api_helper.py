#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests

def get_figma_file(file_key, token, node_ids=None):
    """
    Figma REST API를 호출하여 파일 정보를 가져옵니다.
    node_ids가 지정된 경우, 특정 노드(프레임/컴포넌트) 정보만 상세하게 가져옵니다.
    """
    headers = {
        "X-Figma-Token": token
    }
    
    if node_ids:
        # 특정 노드만 가져올 때
        url = f"https://api.figma.com/v1/files/{file_key}/nodes"
        params = {"ids": ",".join(node_ids)}
        print(f"[*] Figma API 호출 중 (특정 노드 조회): {url} (nodes: {node_ids})")
        response = requests.get(url, headers=headers, params=params)
    else:
        # 전체 파일 가져올 때
        url = f"https://api.figma.com/v1/files/{file_key}"
        print(f"[*] Figma API 호출 중 (전체 파일 조회): {url}")
        response = requests.get(url, headers=headers)
        
    if response.status_code != 200:
        print(f"[-] API 호출 실패 (상태 코드: {response.status_code})")
        print(f"[-] 응답 메시지: {response.text}")
        sys.exit(1)
        
    return response.json()

def clean_node_data(node):
    """
    LLM(헤나)이 분석하기 쉽도록 불필요한 메타데이터를 제거하고 핵심 정보만 정제합니다.
    """
    if not isinstance(node, dict):
        return node
        
    # 핵심 필드만 추출
    cleaned = {
        "id": node.get("id"),
        "name": node.get("name"),
        "type": node.get("type"),
    }
    
    # 레이아웃 정보
    if "absoluteBoundingBox" in node:
        cleaned["bounds"] = node["absoluteBoundingBox"]
        
    # 텍스트 정보 (가장 중요)
    if node.get("type") == "TEXT":
        cleaned["text"] = node.get("characters", "")
        if "style" in node:
            cleaned["text_style"] = {
                "fontSize": node["style"].get("fontSize"),
                "fontWeight": node["style"].get("fontWeight"),
                "fontFamily": node["style"].get("fontFamily"),
                "textAlignHorizontal": node["style"].get("textAlignHorizontal"),
            }
            
    # 스타일 및 색상 정보 정제
    if "fills" in node and node["fills"]:
        fills = []
        for fill in node["fills"]:
            if fill.get("visible", True) and fill.get("type") == "SOLID":
                color = fill.get("color", {})
                # 0-1 범위를 0-255 범위로 변환
                r = int(color.get("r", 0) * 255)
                g = int(color.get("g", 0) * 255)
                b = int(color.get("b", 0) * 255)
                a = color.get("a", 1.0)
                fills.append(f"rgba({r}, {g}, {b}, {a:.2f})")
        if fills:
            cleaned["fills"] = fills
            
    # 자식 노드 순회하며 정제 (재귀)
    if "children" in node:
        cleaned["children"] = [clean_node_data(child) for child in node["children"] if child.get("visible", True)]
        
    return cleaned

def parse_args():
    parser = argparse.ArgumentParser(description="Figma REST API Helper for Hermes Agent")
    parser.add_argument("--token", help="Figma Personal Access Token (또는 FIGMA_ACCESS_TOKEN 환경변수 사용)")
    parser.add_argument("--file-key", required=True, help="Figma 파일 키 (URL에서 'file/' 뒤에 오는 고유값)")
    parser.add_argument("--nodes", help="조회할 Node ID 목록 (쉼표로 구분, 예: '0:1,12:34')")
    parser.add_argument("--output", default="figma_output.json", help="결과를 저장할 JSON 파일 경로")
    parser.add_argument("--raw", action="store_true", help="정제하지 않고 원본 API 응답 저장")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 토큰 로드 순서: Argument -> 환경 변수
    token = args.token or os.environ.get("FIGMA_ACCESS_TOKEN")
    if not token:
        print("[-] 에러: Figma Personal Access Token이 필요합니다.")
        print("    --token 옵션을 사용하거나 FIGMA_ACCESS_TOKEN 환경변수를 설정해주세요.")
        sys.exit(1)
        
    node_ids = [n.strip() for n in args.nodes.split(",")] if args.nodes else None
    
    # 1. API 호출
    try:
        data = get_figma_file(args.file_key, token, node_ids)
    except Exception as e:
        print(f"[-] 예외 발생: {e}")
        sys.exit(1)
        
    # 2. 데이터 정제 또는 원본 유지
    if args.raw:
        result = data
        print("[*] 원본 데이터를 저장합니다.")
    else:
        print("[*] LLM용 핵심 데이터 정제 진행 중...")
        if node_ids:
            # nodes API의 결과는 {"nodes": {"NODE_ID": {"document": ...}}} 구조임
            result = {}
            for nid, ncontent in data.get("nodes", {}).items():
                doc = ncontent.get("document", {})
                result[nid] = clean_node_data(doc)
        else:
            # file API의 결과는 {"document": ...} 구조임
            doc = data.get("document", {})
            result = clean_node_data(doc)
            
    # 3. 파일 저장
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"[+] 성공! 저장 완료: {os.path.abspath(args.output)}")
    print(f"[*] 저장된 노드 수: {len(result) if isinstance(result, dict) else '1 (전체 트리)'}")

if __name__ == "__main__":
    main()
