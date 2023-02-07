import requests
import streamlink
import time

streamer = "liyel"
url = "https://www.twitch.tv/{}".format(streamer)
url_list = streamlink.streams(url)
m3u8_url = url_list['best'].url

segment_list = []
count = 1

while True:
    response = requests.get(m3u8_url)
    stream_data = response.content

    # if line start "#" then it is instruction line
    # if line start "https" then it is a link to a segment

    for line in stream_data.splitlines():
        line = str(line, "utf-8")
        if line.startswith("#"):
            continue
        else:
            if line not in segment_list:
                segment_list.append(line)

                req = requests.get(line, stream=True)
                with open("{}.ts".format(count), "wb") as f:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                count += 1
    time.sleep(10)