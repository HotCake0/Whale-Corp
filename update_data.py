import requests
import json
import time
import random

# BJ ID 목록
bj_ids = [
    "bach023", "gyeonjahee", "melodingding", "nunknown314", 
    "soyoung6056", "akdma9692", "nlov555jij", "xpdpfv2", 
    "gatgdf", "kimmaren77", "doki0818", "dmng50", 
    "ducke77", "joaras2"
]

def get_live_status():
    live_data = {}
    
    # [중요] SOOP(숲) 홈페이지에서 접속한 것처럼 위장하는 헤더
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.sooplive.co.kr/'
    }
    
    print(f"--- 📡 SOOP 데이터망(BJAPI) 접속 시작 ({len(bj_ids)}명) ---")
    
    for bj_id in bj_ids:
        try:
            # [핵심] 현재 SOOP 홈페이지가 실제로 사용하는 방송 정보 주소 (bjapi)
            target_url = f"https://bjapi.afreecatv.com/api/{bj_id}/station"
            
            response = requests.get(target_url, headers=headers, timeout=5)
            data = response.json()
            
            is_live = False
            title = ""
            
            # 데이터 구조 분석 (station > broad 안에 정보가 있으면 방송중)
            if "station" in data and "broad" in data["station"]:
                broad_data = data["station"]["broad"]
                
                # 방송 정보가 비어있지 않으면(None이 아니면) 방송 중!
                if broad_data:
                    is_live = True
                    title = broad_data.get("broad_title", "방송 중")
                    print(f"🔥 LIVE 확인: {bj_id} - {title}")
                else:
                    print(f"💤 OFF: {bj_id}")
            else:
                print(f"💤 OFF: {bj_id} (데이터 없음)")

            live_data[bj_id] = {
                "is_live": is_live,
                "title": title
            }
            
            # 서버 부하 방지를 위해 0.1~0.3초 대기
            time.sleep(random.uniform(0.1, 0.3))
            
        except Exception as e:
            print(f"❌ 에러 {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "" }

    return live_data

if __name__ == "__main__":
    data = get_live_status()
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
