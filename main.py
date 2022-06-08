import requests
import json
import subprocess
import time
from datetime import datetime

client_id = "" # 트위치에서 발급한 클라이언트 아이디 키
client_secret = "" # 트위치에서 발급한 클라이언트 시크릿 키

req = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials")
json_data = json.loads(req.text)
access_token = json_data["access_token"]

repeat_check = True

date = datetime.today().strftime('%Y-%m-%d %H:%M')
path = "" # 파일이 저장될 경로를 지정해준다.
streamer = "" # 자동 다운로드 하고싶은 스트리머의 영문 닉네임을 입력해준다.

def console_print(message):
    print("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] " + message)

def stream_check(streamer):
    req = requests.get("https://api.twitch.tv/helix/users?login=" + streamer, headers={"Client-ID": client_id, "Authorization": "Bearer " + access_token})
    json_data = json.loads(req.text)
    user_id = json_data["data"][0]["id"]

    headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + access_token}
    req = requests.get("https://api.twitch.tv/helix/streams?user_id=" + user_id, headers=headers)
    
    json_data = json.loads(req.text)
    stream_status = json_data["data"]

    if not stream_status:
        return False
    else:
        return True

def stream_download(streamer):
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    subprocess.call(["streamlink", "twitch.tv/" + streamer, "best", "-o", path + "/" + date + ".ts"])

console_print("프로그램 시작됨")

while True:
    if stream_check(streamer):
        console_print("스트리밍 시작이 감지되었습니다")
        stream_download(streamer)
        console_print("스트리밍이 완료되었습니다")
        repeat_check = True
    else:
        if repeat_check:
            console_print("방송 시작 대기중")
            repeat_check = False

    time.sleep(5) # 5초동안 쉬고 다시 체크