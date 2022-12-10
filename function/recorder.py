from datetime import datetime
import streamlink
import subprocess
import platform
import ffmpeg
import requests

def basic_file_info(user_login, extension):
    date = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    path = './' + user_login + '/' + date + '.' + extension
    return path


def download_stream_legacy(user_login, extension):
    path = basic_file_info(user_login, extension)
    stream_url = 'twitch.tv/' + user_login

    if platform.system() == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(["streamlink", stream_url, "best", "-o", path], creationflags=CREATE_NO_WINDOW)
    else:
        subprocess.run(["streamlink", stream_url, "best", "-o", path])
    return

def download_stream_m3u8_legacy(user_login, extension):
    path = basic_file_info(user_login, extension)
    stream_m3u8 = get_stream_m3u8_proxy(user_login)
    stream_m3u8_list = []
    for key, value in stream_m3u8.items():
        stream_m3u8_list.append(value)
    
    try:
        stream_m3u8 = stream_m3u8_list[0]
    except:
        return

    if platform.system() == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(["streamlink", stream_m3u8, "best", "-o", path], creationflags=CREATE_NO_WINDOW)
    else:
        subprocess.run(["streamlink", stream_m3u8, "best", "-o", path])
    return

def get_stream_m3u8(user_login):
    stream_url = "https://www.twitch.tv/" + user_login
    stream_m3u8 = streamlink.streams(stream_url)["best"].url
    return stream_m3u8

def get_stream_m3u8_proxy(user_login):
    url = "https://get-m3u8.twitch-auto-recorder.workers.dev?channel={channel}".format(channel=user_login)
    req = requests.get(url)
    data = req.text.splitlines()

    list = {}
    for i in range(3, len(data), 3):
        try:
            quality = data[i].split(",")[1].split("=")[1].split("x")[1]
            frame = data[i].split(",")[5].split("=")[1].split(".")[0]
            url = data[i+1]
            list["{}p{}".format(quality, frame)] = url
        except:
            url = data[i+1]
            list["audio_only"] = url
    return list

'''
def download_stream_ffmpeg(user_login):
    path = basic_file_info(user_login)
    stream_m3u8 = get_stream_m3u8(user_login)
    ffmpeg.input(stream_m3u8).output(path).run()
    return
'''

def get_remote_file_data(url):
    req = requests.get(url)
    return req.content

def download_stream_direct(user_login):
    path = basic_file_info(user_login, "ts")
    stream_m3u8 = get_stream_m3u8(user_login)