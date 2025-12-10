import requests
import json
import os

CLIENT_ID = os.environ.get('SOOP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SOOP_CLIENT_SECRET')

# 지금 방송 중인 그 멤버의 ID를 맨 앞에 적어주세요! (테스트를 위해)
bj_ids = [
    "bach023", "gyeonjahee", "melodingding", "nunknown314", 
    "soyoung6056", "akdma9692", "nlov555jij", "xpdpfv2", 
    "gatgdf", "kimmaren77", "doki0818", "dmng50", 
    "ducke77", "joaras2"
]

def get_live_status():
    if not CLIENT_ID:
        print("❌ API 키 없음")
        return {}

    url = "https://openapi.afreecatv.com/broad/list"
    
    # 아까 성공했던 그 헤더 방식
    headers = { "ClientId": CLIENT_ID, "Content-Type": "application/x-www-form-urlencoded" }
    
    live_data = {}
    print(f"--- 🕵️ 디버깅 모드 시작 ---")
    
    for bj_id in bj_ids:
        try:
            params = { "client_id": CLIENT_ID, "select_key": "bj_id", "select_value": bj_id }
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            is_live = False
            title = ""
            
            if response.status_code == 200:
                data = response.json()
                
                # [중요] 방송 중인 사람의 데이터는 무조건 출력해서 눈으로 확인!
                if "broad" in data and data["broad"]:
                    print(f"\n✅ {bj_id} 데이터를 찾았습니다!")
                    print(json.dumps(data, indent=2, ensure_ascii=False)) # 데이터 전체 출력
                    
                    is_live = True
                    title = data["broad"][0].get("broad_title", "")
                else:
                    # 방송 중이라는데 데이터가 비어있다면, 그 이유를 알기 위해 빈 껍데기도 출력해봅니다.
                    # 너무 길어질 수 있으니 첫 번째 사람(bach023) 것만 출력
                    if bj_id == bj_ids[0]:
                        print(f"\n❓ {bj_id}: 방송 중이라는데 API는 없다고 함. 원본 데이터:")
                        print(json.dumps(data, indent=2, ensure_ascii=False))
                    else:
                        print(f"💤 {bj_id}: OFF")

            else:
                print(f"⚠️ {bj_id}: 에러 {response.status_code}")

            live_data[bj_id] = { "is_live": is_live, "title": title }
            
        except Exception as e:
            print(f"❌ {bj_id} 에러: {e}")

    return live_data

if __name__ == "__main__":
    data = get_live_status()
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
