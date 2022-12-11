import requests
import json
import flask

app = flask.Flask(__name__)

@app.route('/api/channel/hls/<streamer>.m3u8', methods=['GET'])
def get_usher(streamer):
    # our proxy server is https://usher-proxy.twitch-auto-recorder.workers.dev
    params = flask.request.args

    url = "https://usher-proxy.twitch-auto-recorder.workers.dev/api/channel/hls/{streamer}.m3u8".format(streamer=streamer)
    url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])
    req = requests.get(url)

    return req.text

app.run(host='0.0.0.0', port=80)