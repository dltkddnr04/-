import requests
import json
import random

streamer = "nangodof"

url = "https://gql.twitch.tv/gql#origin=twilight"

header = {
    "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
}

data = {
    "operationName": "PlaybackAccessToken",
    "variables": {
        "isLive": True,
        "login": streamer,
        "isVod": False,
        "vodID": "",
        "playerType": "frontpage"
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"
        }
    }
}

req = requests.post(url, headers=header, json=data)
result = req.text

print(result)
exit()

sig = json.loads(result)['data']['streamPlaybackAccessToken']['signature']
token = json.loads(result)['data']['streamPlaybackAccessToken']['value']

params = {
    'sig': sig,
    'token': token,
    'allow_source': 'true',
    'allow_audio_only': 'true',
    'p': int(random.random() * 999999),
}

url = "https://usher.ttvnw.net/api/channel/hls/{streamer}.m3u8".format(streamer=streamer)
# make url with params
url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])
req = requests.get(url)

print(req.text)