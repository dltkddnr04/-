from function import (function, twitch_api, recorder)
from datetime import datetime
import time
import sys

twitch_api.get_header_online()

repeat_check = True

# user_login = "zomul_e"
try:
    user_login = sys.argv[1]
except:
    print("streamer nickname is not exist")
    exit()
user_id = twitch_api.get_id_from_login(user_login)

function.console_print("Program started")

while True:
    stream_data = twitch_api.get_stream_data(user_id)
    if stream_data is not False:
        function.console_print("Stream started")
        recorder.download_stream_m3u8_legacy(user_login, 'ts')
        function.console_print("Stream ended")
        repeat_check = True
    else:
        if repeat_check:
            function.console_print("Waiting for {} to start streaming".format(user_login))
            repeat_check = False
        time.sleep(5)
