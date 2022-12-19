import requests
import json
import datetime
import random
import flask

gql_url = "https://gql.twitch.tv/gql#origin=twilight"
gql_header = {
    "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
}

def get_stream_m3u8(user_login):
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
                "sha256Hash": "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"
            }
        }
    }

    req = requests.post(gql_url, headers=gql_header, json=data)
    result = req.text

    sig = json.loads(result)['data']['streamPlaybackAccessToken']['signature']
    token = json.loads(result)['data']['streamPlaybackAccessToken']['value']

    params = {
        'sig': sig,
        'token': token,
        'allow_source': 'true',
        'allow_audio_only': 'true',
        'p': int(random.random() * 999999),
    }

    url = "https://usher.ttvnw.net/api/channel/hls/{streamer}.m3u8".format(streamer=user_login)
    url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])
    req = requests.get(url)

    return req.text

app = flask.Flask(__name__)

@app.route('/<user_login>')
def get_m3u8(user_login):
    return get_stream_m3u8(user_login)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)