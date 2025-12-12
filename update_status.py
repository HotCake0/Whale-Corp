import json
import requests
import os

# 고래상사 & 종겜크루 멤버 리스트
CREW_MEMBERS = {
    "bach023": "울산큰고래",
    "doki0818" : "감자가비",
    "xpdpfv2" : "이지수",
    "ducke77" : "밀크티냠",
    "joaras2" : "조아라",
    "gyeonjahee" : "견자희",
    "melodingding" : "멜로딩딩",
    "soyoung6056" : "빡쏘",
    "akdma9692" : "온자두",
    "nlov555jij" : "삐요코",
    "gatgdf" : "쏭이",
    "kimmaren77": "김마렌",
    "dmng50": "빵땅콩",
    "nunknown314": "미현영"
}

def check_member_live(bj_id, bj_name):
    url = f"https://bjapi.afreecatv.com/api/{bj_id}/station"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        broad_data = data.get("broad")
        
        if broad_data:
            broad_no = broad_data.get("broad_no")
            # 썸네일 주소
            thumb_url = f"https://liveimg.afreecatv.com/m/{broad_no}"
            
            # [추가됨] 생방송 플레이어 직행 주소 생성
            # PC 플레이어 기준 주소입니다. 모바일에서도 잘 연결됩니다.
            live_url = f"https://play.sooplive.co.kr/{bj_id}/{broad_no}"
            
            return {
                "id": bj_id,
                "is_live": True,
                "title": broad_data.get('broad_title', ''),
                "viewers": broad_data.get('current_sum_viewer', 0),
                "thumbnail": thumb_url,
                "live_url": live_url  # 이 주소를 웹으로 보냅니다
            }
        else:
            return {"id": bj_id, "is_live": False}
    except Exception as e:
        print(f"Error {bj_name}: {e}")
        return {"id": bj_id, "is_live": False}

if __name__ == '__main__':
    results = []
    print("방송 상태 확인 중...")
    for bj_id, bj_name in CREW_MEMBERS.items():
        info = check_member_live(bj_id, bj_name)
        results.append(info)
    
    # 결과를 status.json 파일로 저장
    with open('status.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("status.json 업데이트 완료!")
