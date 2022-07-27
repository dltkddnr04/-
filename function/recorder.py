import datetime
import streamlink
import ffmpeg
import subprocess
import platform

def basic_file_info(user_login):
    date = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    path = './' + user_login + '/' + date + '.ts'
    return path


def download_stream_legacy(user_login):
    path = basic_file_info(user_login)
    stream_url = 'twitch.tv/' + user_login

    if platform.system() == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(["streamlink", stream_url, "best", "-o", path], creationflags=CREATE_NO_WINDOW)
    else:
        subprocess.run(["streamlink", stream_url, "best", "-o", path])
    return

def get_stream_m3u8(user_login):
    stream_url = "https://www.twitch.tv/" + user_login
    stream_m3u8 = streamlink.streams(stream_url)["best"].url
    return stream_m3u8

def download_stream_ffmpeg(user_login):
    path = basic_file_info(user_login)
    stream_m3u8 = get_stream_m3u8(user_login)
    ffmpeg.input(stream_m3u8).output(path).run()
    return
