from ShazamAPI import Shazam
import json

audio = open('sample.wav', 'rb').read()
shazam = Shazam(audio)
recognize_generator = shazam.recognizeSong()

list = [
    {
        "timestamp": 0,
        "track": "None"
    }
]

try:
    while True:
        data = next(recognize_generator)
        timestamp = data[0]
        if "track" in data[1]:
            title = data[1]['track']['title']
            subtitle = data[1]['track']['subtitle']
            track_data = "{} - {}".format(title, subtitle)
        else:
            track_data = "None"
        print(timestamp, track_data)
        if list[-1]["track"] != track_data:
            list.append({
                "timestamp": timestamp,
                "track": track_data
            })
except StopIteration:
    pass

with open("music_data.json", 'w') as f:
    f.write(json.dumps(list, indent=4, ensure_ascii=False))