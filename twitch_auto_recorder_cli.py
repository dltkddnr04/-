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
    stream_data = twitch_api.get_stream_data(user_id)
    if stream_data is not False:
        console_print("Stream started")
        recorder.download_stream_m3u8_legacy(user_login, 'ts')
        console_print("Stream ended")
        repeat_check = True
    else:
        if repeat_check:
            console_print("Waiting for {} to start streaming".format(user_login))
            repeat_check = False
        time.sleep(5)
