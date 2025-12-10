import requests
import json
import os

# [핵심] GitHub 금고(환경변수)에서 키를 꺼내옵니다.
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
        print("오류: API 키가 없습니다. GitHub Secrets 설정을 확인하세요.")
        return {}

    url = "https://openapi.afreecatv.com/broad/list"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Brief-Key": CLIENT_ID 
    }
    
    live_data = {}
    print("--- 방송 정보 조회 시작 ---")
    
    for bj_id in bj_ids:
        try:
            params = {
                "client_id": CLIENT_ID,
                "select_key": "bj_id",
                "select_value": bj_id
            }
            response = requests.get(url, headers=headers, params=params)
            
            is_live = False
            title = ""
            
            if response.status_code == 200:
                data = response.json()
                if "broad" in data and len(data["broad"]) > 0:
                    is_live = True
                    title = data["broad"][0].get("broad_title", "")
                    print(f"✅ {bj_id}: ON")
                else:
                    print(f"💤 {bj_id}: OFF")
            else:
                print(f"⚠️ {bj_id}: API 호출 실패 ({response.status_code})")

            live_data[bj_id] = {"is_live": is_live, "title": title}
            
        except Exception as e:
            print(f"에러 발생 {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "" }

    return live_data

if __name__ == "__main__":
    data = get_live_status()
    # 결과 저장
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
