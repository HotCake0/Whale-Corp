import requests
import json
import os

# GitHub Secrets에서 가져오기
CLIENT_ID = os.environ.get('SOOP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SOOP_CLIENT_SECRET')

bj_ids = [
    "bach023", "gyeonjahee", "melodingding", "nunknown314", 
    "soyoung6056", "akdma9692", "nlov555jij", "xpdpfv2", 
    "gatgdf", "kimmaren77", "doki0818", "dmng50", 
    "ducke77", "joaras2"
]

def get_live_status():
    if not CLIENT_ID:
        print("❌ 오류: SOOP_CLIENT_ID가 없습니다. Secrets 설정을 확인하세요.")
        return {}

    url = "https://openapi.afreecatv.com/broad/list"
    
    # [수정됨] 헤더 이름을 'Brief-Key'에서 'ClientId'로 변경
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "ClientId": CLIENT_ID 
    }
    
    live_data = {}
    print(f"--- 방송 정보 조회 시작 (대상: {len(bj_ids)}명) ---")
    
    for bj_id in bj_ids:
        try:
            params = {
                "client_id": CLIENT_ID,
                "select_key": "bj_id",
                "select_value": bj_id
            }
            
            # 타임아웃 5초 설정 (무한 대기 방지)
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            is_live = False
            title = ""
            
            if response.status_code == 200:
                data = response.json()
                
                # 방송 중인지 체크
                if "broad" in data and data["broad"]:
                    is_live = True
                    title = data["broad"][0].get("broad_title", "")
                    print(f"✅ {bj_id}: 방송 중! ({title})")
                else:
                    # 방송 중이 아님
                    print(f"💤 {bj_id}: OFF")
            else:
                # [중요] 에러가 나면 왜 났는지 로그에 출력
                print(f"⚠️ {bj_id}: 호출 실패 (Code: {response.status_code})")
                print(f"👉 서버 메시지: {response.text}") 

            live_data[bj_id] = {
                "is_live": is_live,
                "title": title
            }
            
        except Exception as e:
            print(f"❌ 에러 발생 {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "" }

    return live_data

if __name__ == "__main__":
    data = get_live_status()
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
