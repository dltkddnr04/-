from datetime import datetime
import function.function as function
import streamlink
import subprocess
import platform
import requests
import json
import random


GQL_URL = "https://gql.twitch.tv/gql#origin=twilight"
INTEGRITY_URL = "https://gql.twitch.tv/integrity"
HEADERS = {
    # "Client-ID": "jzkbprff40iqj646a697cyrvl0zt2m6"
    "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
}

def basic_file_info(user_login, extension):
    date = datetime.today().strftime('%Y-%m-%dT%H-%M-%S')
    path = './' + user_login + '/' + date + '.' + extension
    return path

def get_integrity():
    req = requests.post(INTEGRITY_URL, headers=HEADERS)
    return json.loads(req.text)["token"]

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
    try:
        for i in range(0, 4):
            serverless_m3u8 = get_stream_m3u8_serverless(user_login)
            pwnsh_m3u8 = get_stream_m3u8_pwnsh(user_login)
            # if serverless_m3u8 have 1080p60 or 1080p30 key then use serverless_m3u8
            if "1080p60" in serverless_m3u8.keys():
                stream_m3u8 = serverless_m3u8["1080p60"]
                message = "use serverless download 1080p60"
                break
            elif "1080p30" in serverless_m3u8.keys():
                stream_m3u8 = serverless_m3u8["1080p30"]
                message = "use serverless download 1080p30"
                break
            elif "1080p60" in pwnsh_m3u8.keys():
                stream_m3u8 = pwnsh_m3u8["1080p60"]
                message = "use pwnsh download 1080p60"
            elif "1080p30" in pwnsh_m3u8.keys():
                stream_m3u8 = pwnsh_m3u8["1080p30"]
                message = "use pwnsh download 1080p30"
            else:
                stream_m3u8 = get_stream_m3u8_streamlink(user_login)["best"]
                message = "can't use 1080p, instead 720p using streamlink"

    except:
        stream_m3u8 = get_stream_m3u8_streamlink(user_login)["best"]
        message = "can't use 1080p, instead 720p using streamlink"

    function.console_print(message)    

    if platform.system() == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(["streamlink", stream_m3u8, "best", "-o", path], creationflags=CREATE_NO_WINDOW)
    else:
        subprocess.run(["streamlink", stream_m3u8, "best", "-o", path])
    return

def download_stream_direct(user_login, extension):
    path = basic_file_info(user_login, extension)
    try:
        token, sig = get_stream_access_token(user_login)
        stream_m3u8_list = get_stream_m3u8_direct(user_login, sig, token)

        m3u8_quality_list = list(stream_m3u8_list.keys())

        # remove audio_only if exist
        if "audio_only" in m3u8_quality_list:
            m3u8_quality_list.remove("audio_only")

        # get best quality
        best_quality = None
        for quality in m3u8_quality_list:
            if quality.endswith('(original)'):
                best_quality = quality
                break

            if best_quality is None:
                best_quality = quality
            elif int(quality.split('p')[0]) >= int(best_quality.split('p')[0]):
                if int(quality.split('p')[1]) >= int(best_quality.split('p')[1]):
                    best_quality = quality

        stream_m3u8 = stream_m3u8_list[best_quality]
        message = "use direct download {quality}".format(quality=best_quality)

    except:
        stream_m3u8 = get_stream_m3u8_streamlink(user_login)["best"]
        message = "can't use direct, instead using streamlink"

    function.console_print(message)
    function.console_print("download dir: {path}".format(path=path))

    if platform.system() == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(["streamlink", stream_m3u8, "best", "-o", path], creationflags=CREATE_NO_WINDOW)
    else:
        # subprocess.run(["streamlink", stream_m3u8, "best", "-o", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-i", stream_m3u8, "-c", "copy", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return

def get_stream_access_token(user_login):
    url = "https://gql.twitch.tv/gql#origin=twilight"
    header = HEADERS.copy()
    header["Client-Integrity"] = get_integrity()
    data = {
        "operationName": "PlaybackAccessToken",
        "variables": {
            "isLive": True,
            "login": user_login,
            "isVod": False,
            "vodID": "",
            "playerType": "frontpage"
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "3093517e37e4f4cb48906155bcd894150aef92617939236d2508f3375ab732ce"
            }
        }
    }

    req = requests.post(url, headers=header, json=data)
    result = req.text

    sig = json.loads(result)['data']['streamPlaybackAccessToken']['signature']
    token = json.loads(result)['data']['streamPlaybackAccessToken']['value']

    return token, sig

def get_stream_access_token_serverless(user_login):
    url = "https://get-stream-accesstoken.twitch-auto-recorder.workers.dev/?channel={channel}".format(channel=user_login)
    req = requests.get(url)
    data = json.loads(req.text)

    sig = data['sig']
    token = data['token']

    return token, sig

def get_stream_m3u8_direct(streamer, sig, token):
    params = {
        "acmb": "e30=",
        "allow_source": True,
        "browser_family": "firefox",
        "browser_version": "120.0.1",
        "cdm": "fp",
        "fast_bread": True,
        "os_name": "Linux",
        "os_version": "22.04.3",
        "p": int(random.random() * 999999),
        "platform": "web",
        "play_session_id": "64dfd083536872a81c1136807d55f976",
        "player_backend": "mediaplayer",
        "player_version": "1.23.0",
        "playlist_include_framerate": True,
        "reassignments_supported": True,
        "sig": sig,
        "supported_codecs": "h265,h264",
        "token": token,
        "transcode_mode": "cbr_v1",
    }

    url = "https://usher.ttvnw.net/api/channel/hls/{streamer}.m3u8".format(streamer=streamer)
    url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])

    req = requests.get(url)
    data = req.text.splitlines()

    list = {}
    for i in range(3, len(data), 3):
        try:
            quality1 = data[i].split(",")[1].split("=")[1].split("x")[0]
            quality2 = data[i].split(",")[1].split("=")[1].split("x")[1]
            quality = quality1 if int(quality1) < int(quality2) else quality2
            frame = data[i].split(",")[5].split("=")[1].split(".")[0]
            video_nick = data[i].split(",")[4].split("\"")[1]
            url = data[i+1]

            if video_nick == "chunked":
                list["{}p{}(original)".format(quality, frame)] = url
            else:
                list["{}p{}".format(quality, frame)] = url

        except:
            url = data[i+1]
            list["audio_only"] = url

    return list

def get_stream_m3u8_streamlink(user_login):
    stream_url = "https://www.twitch.tv/" + user_login
    streams = streamlink.streams(stream_url)
    
    list = {}
    for key, value in streams.items():
        list[key] = value.url

    return list

def get_stream_m3u8_serverless(user_login):
    url = "https://get-m3u8.twitch-auto-recorder.workers.dev?channel={channel}".format(channel=user_login)
    req = requests.get(url)
    data = req.text.splitlines()

    list = {}
    for i in range(3, len(data), 3):
        try:
            quality1 = data[i].split(",")[1].split("=")[1].split("x")[0]
            quality2 = data[i].split(",")[1].split("=")[1].split("x")[1]
            quality = quality1 if int(quality1) < int(quality2) else quality2
            frame = data[i].split(",")[5].split("=")[1].split(".")[0]
            url = data[i+1]
            list["{}p{}".format(quality, frame)] = url
        except:
            url = data[i+1]
            list["audio_only"] = url

    return list

def get_stream_m3u8_pwnsh(user_login):
    url = "https://pwn.sh/tools/streamapi.py?url=twitch.tv/{channel}".format(channel=user_login)
    req = requests.get(url)
    data = json.loads(req.text)
    data = data["urls"]

    return data

def get_stream_m3u8_tokyo_fix(user_login):
    url = "https://api.twitch.tyo.kwabang.net/hls-raw/{channel}.m3u8".format(channel=user_login)
    token, sig = get_stream_access_token_serverless(user_login)
    url = url + "?token={token}&sig={sig}".format(token=token, sig=sig)
    req = requests.get(url)
    data = req.text.splitlines()

    list = {}
    for i in range(3, len(data), 3):
        try:
            quality1 = data[i].split(",")[1].split("=")[1].split("x")[0]
            quality2 = data[i].split(",")[1].split("=")[1].split("x")[1]
            quality = quality1 if int(quality1) < int(quality2) else quality2
            frame = data[i].split(",")[5].split("=")[1].split(".")[0]
            url = data[i+1]
            list["{}p{}".format(quality, frame)] = url
        except:
            url = data[i+1]
            list["audio_only"] = url

    return list

def get_stream_m3u8_gql(user_login):
    url = "https://usher.ttvnw.net/api/channel/hls/{streamer}.m3u8".format(streamer=user_login)
    token, sig = get_stream_access_token_serverless(user_login)
    params = {
        'sig': sig,
        'token': token,
        'allow_source': 'true',
        'allow_audio_only': 'true',
        'p': int(random.random() * 999999),
    }
    url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])
    req = requests.get(url)

    return req.text.splitlines()