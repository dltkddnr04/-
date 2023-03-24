import requests
import streamlink
import time
import datetime
import os

streamer = "jujuplease"
url = "https://www.twitch.tv/{}".format(streamer)
url_list = streamlink.streams(url)
m3u8_url = url_list['best'].url

segment_list = []
count = 1
dir = "dt/{}".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

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

                if not os.path.exists(dir):
                    os.makedirs(dir)

                req = requests.get(line, stream=True)
                with open("{}/{}.ts".format(dir, line.split("/")[-1]), 'wb') as f:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                # get file's sha256 hash
                # with open("{}/{}.ts".format(dir, line.split("/")[-1]), 'rb') as f:
                #     sha256 = hashlib.sha256(f.read()).hexdigest()
                #     print(sha256)

                count += 1
    time.sleep(1)