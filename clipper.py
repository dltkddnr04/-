from function import (function, recorder, twitch_api)
from datetime import (datetime, timedelta)
import requests
import json
import threading
import time
import os
import hashlib

def clip_download_threading(clip_data):
    clip_link = clip_data["thumbnail_url"].split("-preview-")[0] + ".mp4"

    clip_count_in_thread = clip_count - len(clip_list)
    clip_list.remove(clip_data)

    file_name = clip_data["hash_id"] + ".mp4"
    file_dir = "clips/{}/{}".format(user_login, file_name)
    try:
        req = requests.get(clip_link, stream=True)
        with open(file_dir, "wb") as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        function.console_print("Download Complete: {} ({}/{})".format(file_name, clip_count_in_thread, clip_count))
    except:
        clip_list.append(clip_data)

twitch_api.get_header_online()

function.console_print("Clipper Start")

# 스트리머 정보를 가져옴
user_login = 'ryung971219'
user_id = twitch_api.get_id_from_login(user_login)

if not os.path.exists("clips/{}".format(user_login)):
    os.makedirs("clips/{}".format(user_login))

function.console_print("Streamer: {}".format(user_login))

# 스트리머의 클립 정보를 가져옴
# start and end time as RFC3339 format
start_time = datetime(2000, 1, 1, 0, 0, 0).isoformat() + 'Z'
# end time is tomorrow
end_time = datetime.now() + timedelta(days=1)
end_time = end_time.isoformat() + 'Z'
clip_list = twitch_api.get_clip_list(user_id, start_time, end_time)

clip_count = len(clip_list)

function.console_print("Clip Count: {}".format(clip_count))

for clip_data in clip_list:
    hash_raw = clip_data["broadcaster_name"] + clip_data["created_at"]
    # hash to sha256
    hash_id = hashlib.sha256(hash_raw.encode()).hexdigest()
    clip_data["hash_id"] = hash_id

# 클립 정보를 json 파일로 저장
# clip_list = json.loads(clip_list)
with open("clips/{}_clip_list.json".format(user_login), "w") as f:
    f.write(json.dumps(clip_list, indent=4))

function.console_print("Clip List Save Complete: clips/{}_clip_list.json".format(user_login))

# 파일 다운로드
while len(clip_list) > 0:
    while threading.active_count() > 10:
        time.sleep(0.1)
    threading.Thread(target=clip_download_threading, args=(clip_list[0],)).start()

# check file number and compare with clip count
file_list = os.listdir("clips/{}".format(user_login))
if len(file_list) != clip_count:
    function.console_print("some files are not downloaded. program will be retry to download.")
    while len(clip_list) > 0:
        # manual download
        for clip_link in clip_list:
            clip_download_threading(clip_link)
        
function.console_print("{} clips are successfully downloaded".format(len(file_list)))