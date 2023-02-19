from function import (function, twitch_api, recorder)
from datetime import datetime
import time
import sys
import os
import threading

twitch_api.get_header_online()
function.console_print("Program started")

def stream_download_solo(user_login):
    user_id = twitch_api.get_id_from_login(user_login)
    repeat_check = True

    if not os.path.exists("{}".format(user_login)):
        os.makedirs("{}".format(user_login))

    while True:
        stream_data = twitch_api.get_stream_data(user_id)
        if stream_data is not False:
            function.console_print("[{user_login}] Stream started".format(user_login=user_login))
            try:
                recorder.download_stream_direct(user_login, 'ts')
                function.console_print("[{user_login}] Stream ended".format(user_login=user_login))
                repeat_check = True
            except Exception as e:
                function.console_print("[{user_login}] Stream ended".format(user_login=user_login))
                # print("Error: {}".format(e))
                repeat_check = True
                continue
        else:
            if repeat_check:
                function.console_print("[{user_login}] Waiting to start streaming".format(user_login=user_login))
                repeat_check = False
            time.sleep(5)

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
    time.sleep(10)