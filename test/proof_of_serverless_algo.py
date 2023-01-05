import requests
import random
import json

streamer = "haumpah"

header = {
    'Client-ID': 'jzkbprff40iqj646a697cyrvl0zt2m6',
}

url = "https://api.twitch.tv/api/channels/{streamer}/access_token?".format(streamer=streamer)

req = requests.get(url, headers=header)

sig = req.json()['sig']
token = req.json()['token']

params = {
    'sig': sig,
    'token': token,
    'allow_source': 'true',
    'allow_audio_only': 'true',
    'allow_spectre': 'false',
    'type': 'any',
    'p': int(random.random() * 999999),
}
url = "https://usher.ttvnw.net/api/channel/hls/{streamer}.m3u8".format(streamer=streamer)
# make url with params
url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])
req = requests.get(url)

print(req.text)