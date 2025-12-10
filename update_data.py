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
    
    # 봇이 아니라 일반 사용자인 척 위장하는 헤더 (User-Agent)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://m.afreecatv.com/'
    }
    
    print(f"--- 📡 모바일 데이터망 접속 시작 ({len(bj_ids)}명) ---")
    
    for bj_id in bj_ids:
        try:
            # [핵심] 아프리카TV 모바일 웹페이지가 데이터를 받아오는 실제 주소
            target_url = f"https://hp.afreecatv.com/api/main/station/{bj_id}"
            
            response = requests.get(target_url, headers=headers, timeout=5)
            data = response.json()
            
            is_live = False
            title = ""
            
            # 데이터 구조 분석: data > station > broad 정보가 있으면 방송 중
            if "data" in data and "station" in data["data"]:
                station_data = data["data"]["station"]
                
                # 'broad' 항목이 존재하고 비어있지 않으면 방송 중
                if "broad" in station_data and station_data["broad"]:
                    is_live = True
                    title = station_data["broad"].get("broad_title", "방송 중")
                    print(f"🔥 LIVE 확인: {bj_id} - {title}")
                else:
                    print(f"💤 OFF: {bj_id}")
            else:
                print(f"❓ 데이터 확인 불가: {bj_id}")

            live_data[bj_id] = {
                "is_live": is_live,
                "title": title
            }
            
            # 서버 차단 방지를 위해 약간의 딜레이 (0.1초~0.3초)
            time.sleep(random.uniform(0.1, 0.3))
            
        except Exception as e:
            print(f"❌ 에러 {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "" }

    return live_data

if __name__ == "__main__":
    data = get_live_status()
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
