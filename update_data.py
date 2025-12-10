import requests
import json
import os

# 1. SOOP 개발자 센터에서 받은 키 (나중에 GitHub에 등록할 예정)
# 로컬에서 테스트할 때는 os.environ.get(...) 부분을 지우고 본인의 실제 키를 따옴표 안에 넣어서 테스트하세요.
CLIENT_ID = os.environ.get('SOOP_CLIENT_ID') 
CLIENT_SECRET = os.environ.get('SOOP_CLIENT_SECRET')

# 2. 고래상사 멤버들의 ID 목록 (HTML의 data-bj-id와 일치해야 함)
bj_ids = [
    "bach023", "gyeonjahee", "melodingding", "nunknown314", 
    "soyoung6056", "akdma9692", "nlov555jij", "xpdpfv2", 
    "gatgdf", "kimmaren77", "doki0818", "dmng50", 
    "ducke77", "joaras2"
]

def get_live_status():
    # SOOP API: 방송 리스트 조회 엔드포인트
    url = "https://openapi.afreecatv.com/broad/list"
    
    # 헤더 설정 (Brief-Key 방식이 일반적이나, API 문서에 따라 Client-ID 방식일 수 있음)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Brief-Key": CLIENT_ID 
    }
    
    live_data = {}
    
    print("--- 방송 정보 조회 시작 ---")
    
    for bj_id in bj_ids:
        try:
            # API 호출 파라미터 (특정 BJ ID로 검색)
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
                # 'broad' 키 안에 데이터가 있으면 방송 중인 것으로 판단
                if "broad" in data and len(data["broad"]) > 0:
                    is_live = True
                    title = data["broad"][0].get("broad_title", "")
                    print(f"✅ {bj_id}: 방송 중 ({title})")
                else:
                    print(f"💤 {bj_id}: 방송 종료")
            else:
                print(f"⚠️ {bj_id}: API 호출 실패 (Code: {response.status_code})")

            # 결과 저장
            live_data[bj_id] = {
                "is_live": is_live,
                "title": title
            }
            
        except Exception as e:
            print(f"Error fetching {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "" }

    return live_data

if __name__ == "__main__":
    # 데이터 가져오기
    data = get_live_status()
    
    # JSON 파일로 저장 (웹사이트가 이 파일을 읽음)
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("--- streamer_data.json 저장 완료 ---")