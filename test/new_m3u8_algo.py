import requests
import json
import datetime
import time
import os
import sys
import subprocess
import random

streamer = "dookongc"

def get_sig_token(streamer):
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

    sig = json.loads(result)['data']['streamPlaybackAccessToken']['signature']
    token = json.loads(result)['data']['streamPlaybackAccessToken']['value']

    return sig, token

def get_m3u8_url(streamer, sig, token):
    params = {
        'allow_source': True,
        'p': int(random.random() * 999999),
        'player_backend': 'mediaplayer',
        'sig': sig,
        'supported_codecs': 'vp09.00.50.08,avc1.64001f',
        'token': token,
        'warp': True,
    }

    cookie = {
        'experiment_overrides': {
            "experiments": {
                "e5c813df-a190-4def-b0cb-932224c989f1":"treatment"
            },
            "disabled":[]
        }
    }

    url = "https://usher.ttvnw.net/api/channel/hls/{streamer}.m3u8".format(streamer=streamer)
    url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])

    req = requests.get(url)
    return req.text

print(get_m3u8_url(streamer, *get_sig_token(streamer)))
