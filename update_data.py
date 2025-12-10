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
    
    # Player API (로그인 불필요, 가장 빠름)
    url = "https://live.afreecatv.com/afreeca/player_live_api.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    print(f"--- 📡 데이터 수집 시작 ({len(bj_ids)}명) ---")
    
    for bj_id in bj_ids:
        try:
            data = { "bid": bj_id, "type": "live" }
            response = requests.post(url, headers=headers, data=data, timeout=5)
            res_json = response.json()
            
            is_live = False
            title = ""
            thumb = ""
            view_cnt = "0"
            
            if "CHANNEL" in res_json and res_json["CHANNEL"].get("RESULT") == 1:
                channel = res_json["CHANNEL"]
                is_live = True
                title = channel.get("BROAD_TITLE", "")
                view_cnt = channel.get("VIEW_CNT", "0")
                
                # 썸네일 URL 생성 (Player API 방식)
                broad_no = channel.get("BROAD_NO")
                if broad_no:
                    thumb = f"https://liveimg.afreecatv.com/m/{broad_no}.gif"
                
                print(f"🔥 LIVE: {bj_id} ({view_cnt}명)")
            else:
                print(f"💤 OFF : {bj_id}")

            live_data[bj_id] = {
                "is_live": is_live,
                "title": title,
                "thumb": thumb,
                "view_cnt": view_cnt
            }
            
            time.sleep(random.uniform(0.05, 0.1)) # 차단 방지 딜레이
            
        except Exception as e:
            print(f"❌ 에러 {bj_id}: {e}")
            live_data[bj_id] = { "is_live": False, "title": "", "thumb": "", "view_cnt": "0" }

    return live_data

if __name__ == "__main__":
    data = get_live_status()
    with open("streamer_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
