import requests
import json

sid = "272211337"

url = "https://tgd.kr/clips/lists/{page_number}?date_range=overall&sortby=new&streamer_id={sid}"

page_number = 1
status = "success"

while status == "success":
    req = requests.get(url.format(page_number=page_number, sid=sid))
    data = req.text.split("</ul>\n</div>\n\n")[-1]
    if data.startswith("\n<div class=\"r\">"):
        clip_list_raw = data.split("<div class=\"clips\" ")

        for i in clip_list_raw:
            if i.startswith("data-id"):
                clip_url = i.split("<img class=\"clips-thumbnail\" src=\"")[1].split("-preview")[0] + ".mp4"
                file_name = clip_url.split("/")[-1]

                # download clip using requests
                req = requests.get(clip_url, stream=True)
                with open(file_name, "wb") as f:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

    else:
        status = "fail"

    page_number += 1