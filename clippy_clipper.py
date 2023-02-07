from function import (function, twitch_api)
from datetime import (datetime, timedelta)
import requests
import json
import threading
import time
import os
import hashlib

def clip_download_thread(clip_data):
    clip_link = clip_data["downloadLink"]
    clip_file_name = clip_data["hash_id"] + ".mp4"
    temp_file_name = clip_data["hash_id"] + ".temp"
    file_dir = "clips/{}/{}".format(user_login, temp_file_name)

    # if file already exsist then skip
    if os.path.isfile(file_dir.replace(".temp", ".mp4")):
        # function.console_print("Already Downloaded: {}".format(clip_file_name))
        return

    try:
        req = requests.get(clip_link, stream=True)
        with open(file_dir, "wb") as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        # change file extension to mp4
        os.rename(file_dir, file_dir.replace(".temp", ".mp4"))

        clip_count_in_thread = get_current_file_number("clips/{}".format(user_login), "mp4")
        function.console_print("Download Complete: {} ({}/{})".format(clip_file_name, clip_count_in_thread, clip_count))
        return
    except:
        function.console_print("Download Failed: {}".format(clip_file_name))
        return

def get_current_file_number(directory, extension):
    file_list = os.listdir(directory)
    extension_filtered = filter(lambda x: x.endswith('.' + extension), file_list)
    num_extension_filtered = len(list(extension_filtered))

    return num_extension_filtered

twitch_api.get_header_online()
function.console_print("Clipper Start")

user_login = "ryung971219"
user_id = twitch_api.get_id_from_login(user_login)

if not os.path.exists("clips/{}".format(user_login)):
    os.makedirs("clips/{}".format(user_login))

function.console_print("Streamer: {}".format(user_login))

url = url = "https://api.clippy.kr/clip/user/{}".format(user_id)
req = requests.get(url)
clip_list_raw = req.json()
clip_list_raw = clip_list_raw["data"]
clip_list = []
download_queue = []

for clip_data in clip_list_raw:
    if clip_data not in clip_list:
        clip_list.append(clip_data)

clip_count = len(clip_list)
function.console_print("Clip Count: {}".format(clip_count))

for clip_data in clip_list:
    hash_raw = clip_data["userInfo"]["display_name"] + clip_data["created_at"] + clip_data["key"]
    hash_id = hashlib.sha256(hash_raw.encode()).hexdigest()
    clip_data["hash_id"] = hash_id

with open("clips/{}.json".format(user_login), "w") as f:
    f.write(json.dumps(clip_list, indent=4, ensure_ascii=False))

function.console_print("Clip List Save Complete: clips/{}.json".format(user_login))

while len(clip_list) != get_current_file_number("clips/{}".format(user_login), "mp4"):
    # get current file list and compare with clip_list and update download_queue
    current_file_list = os.listdir("clips/{}".format(user_login))
    for clip_data in clip_list:
        if clip_data["hash_id"] + ".mp4" not in current_file_list:
            download_queue.append(clip_data)

    if get_current_file_number("clips/{}".format(user_login), "mp4") == 0:
        function.console_print("Download Start")
    elif len(download_queue) != 0:
        function.console_print("{} clips are not downloaded".format(len(download_queue)))

    # download logic
    while len(download_queue) > 0:
        while threading.active_count() < 10:
            if len(download_queue) == 0:
                break
            else:
                current_file = download_queue.pop()
                threading.Thread(target=clip_download_thread, args=(current_file,)).start()
        time.sleep(0.5)

    while threading.active_count() != 1:
        time.sleep(1)

file_num = get_current_file_number("clips/{}".format(user_login), "mp4")
# print("Final Check ({}/{})".format(file_num, clip_count))
if len(clip_list) == file_num:
    function.console_print("{} clips are successfully downloaded".format(file_num))