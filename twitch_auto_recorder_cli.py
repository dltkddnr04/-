import requests
import json
import subprocess
import time
from datetime import datetime
from function import (twitch_api, recorder)

twitch_api.get_header_online()

repeat_check = True

user_login = "zomul_e" # 자동 다운로드 하고싶은 스트리머의 영문 닉네임을 입력해준다.
user_id = twitch_api.get_id_from_login(user_login)

def console_print(message):
    print("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "] " + message)

console_print("Program started")

while True:
    if twitch_api.get_stream_data(user_id):
        console_print(user_login + " start streaming")
        recorder.download_stream_legacy(user_login)
        console_print(user_login + " finished streaming")
        repeat_check = True
    else:
        if repeat_check:
            console_print("Waiting for " + user_login + " to start streaming")
            repeat_check = False

    time.sleep(5) # 5초동안 쉬고 다시 체크