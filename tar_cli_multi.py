from function import (function, twitch_api, recorder)
from datetime import datetime
import time
import sys
import os
import threading

function.console_print("Program started")

def stream_download_solo(user_login):
    repeat_check = True

    if not os.path.exists("{}".format(user_login)):
        os.makedirs("{}".format(user_login))

    while True:
        stream_data = {}
        while stream_data == {}:
            if repeat_check:
                function.console_print("[{user_login}] Waiting to start streaming".format(user_login=user_login))
                repeat_check = False

            try:
                token, sig = recorder.get_stream_access_token(user_login)
                stream_data = recorder.get_stream_m3u8_direct(user_login, sig, token)
            except:
                continue
            
            time.sleep(1)

        if stream_data != {}:
            function.console_print("[{user_login}] Stream started".format(user_login=user_login))
            try:
                recorder.download_stream_direct(user_login, 'ts')
            except Exception as e:
                # print("Error: {}".format(e))
                continue

            function.console_print("[{user_login}] Stream ended".format(user_login=user_login))
            repeat_check = True

try:
    user_login_list = sys.argv[1:]
except:
    print("streamer nickname is not exist")
    exit()

if len(user_login_list) == 0:
    print("streamer nickname is not exist")
    exit()

for user_login in user_login_list:
    thread = threading.Thread(target=stream_download_solo, args=(user_login,))
    thread.start()

while True:
    time.sleep(60)