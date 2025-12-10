import requests
import json
import os
import time

# 환경변수에서 키 가져오기
CLIENT_ID = os.environ.get('SOOP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SOOP_CLIENT_SECRET')

# BJ ID 목록
bj_ids = [
    "bach023", "gyeonjahee", "melodingding", "nunknown314", 
    "soyoung6056", "akdma9692", "nlov555jij", "xpdpfv2", 
    "gatgdf", "kimmaren77", "doki0818", "dmng50", 
    "ducke77", "joaras2"
]

def get_live_status():
    if not CLIENT_ID:
        print("❌ 오류: API 키가 없습니다. Settings > Secrets를 확인하세요.")
        return {}

    url = "https://openapi.afreecatv.com/broad/list"
    
    # 3가지 헤더 방식을 모두 준비
    header_candidates = [
        {"ClientId": CLIENT_ID},          # 1순위: 최신 방식
        {"Brief-Key": CLIENT_ID},         # 2순위: 기존 방식
        {"x-brief-key": CLIENT_ID}        # 3순위: 일부 레거시
    ]
    
    # 올바른 헤더 찾기 테스트 (첫 번째 BJ로 테스트)
    valid_headers = None
    test_bj = bj_ids[0]
    
    print(f"--- API 연결 테스트 시작 (대상: {test_bj}) ---")
    
    for headers in header_candidates:
        try:
            # 헤더별 Content-Type 추가
            current_headers = headers.copy()
            current_headers["Content-Type"] = "application/x-www-form-urlencoded"
            
            params = {"client_id": CLIENT_ID, "select_key": "bj_id", "select_value": test_bj}
            response = requests.get(url, headers=current_headers, params=params, timeout=3)
            
            if response.status_code == 200:
                print(f"✅ 연결 성공! 사용된 헤더 방식: {headers}")
                valid_headers = current_headers
                break
            elif response.status_code == 401:
                print(f"⚠️ 인증 실패 (401) - 헤더 {headers} 방식이 아님.")
        except Exception as e:
            print(f"에러: {e}")

    if not valid_headers:
        print("❌ [치명적 오류] 모든 헤더 방식이 실패했습니다. Client ID가 정확한지 확인하세요.")
        # 실패해도 빈 데이터라도 남기기 위해 기본 헤더 사용
        valid_headers = {"ClientId": CLIENT_ID, "Content-Type": "application/x-www-form-urlencoded"}

    # 실제 데이터 수집 시작
    live_data = {}
    print(f"\n--- 전체 BJ({len(bj_ids)}명) 조회 시작 ---")
    
    for bj_id in bj_ids:
        try:
            params = {
                "client_id": CLIENT_ID,
                "select_key": "bj_id",
                "select_value": bj_id
            }
            response = requests.get(url, headers=valid_headers, params=params, timeout=5)
            
            is_live = False
            title = ""
            
            if response.status_code == 200:
                data = response.json()
                if "broad" in data and data["broad"]:
                    is_live = True
                    title = data["broad"][0].get("broad_title", "")
                    print(f"🔴 LIVE: {bj_id} - {title}")
                else:
                    print(f"⚪ OFF : {bj_id}")
            else:
                print(f"⚠️ 호출 오류 {bj_id}: {response.status_code}")

            live_data[bj_id] = { "is_live": is_live, "title": title }
            
        except Exception as e:
            print(f"❌ 에러 {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "" }
            
    return live_data

if __name__ == "__main__":
    data = get_live_status()
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
