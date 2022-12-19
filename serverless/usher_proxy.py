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

@app.route('/api/channel/hls/<streamer>.m3u8', methods=['POST'])
def post_usher(streamer):
    # our proxy server is https://usher-proxy.twitch-auto-recorder.workers.dev
    params = flask.request.args

    url = "https://usher-proxy.twitch-auto-recorder.workers.dev/api/channel/hls/{streamer}.m3u8".format(streamer=streamer)
    url += '?' + '&'.join(['%s=%s' % (key, value) for (key, value) in params.items()])
    req = requests.post(url, data=flask.request.data)

    return req.text

# anything else url will be passthrough to original twitch usher server

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)