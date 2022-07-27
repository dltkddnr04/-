import requests
import json

def get_access_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token?client_id=' + client_id + '&client_secret=' + client_secret + '&grant_type=client_credentials'
    req = requests.post(url)
    access_token = req.json()['access_token']
    return access_token

def get_header(client_id, access_token):
    global headers
    headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + access_token}
    return headers

def check_user_exists(user_iden):
    if user_iden.isdigit() and len(user_iden) == 9:
        url = 'https://api.twitch.tv/helix/users?id='
    else:
        url = 'https://api.twitch.tv/helix/users?login='

    req = requests.get(url + user_iden, headers=headers)
    json_data = json.loads(req.text)
    if json_data["data"]:
        return True
    else:
        return False

def get_id_from_login(user_login):
    url = 'https://api.twitch.tv/helix/users?login=' + user_login
    req = requests.get(url, headers=headers)
    user_id = req.json()['data'][0]['id']
    return user_id

def get_login_from_id(user_id):
    url = 'https://api.twitch.tv/helix/users?id=' + user_id
    req = requests.get(url, headers=headers)
    user_login = req.json()['data'][0]['login']
    return user_login

def get_stream_data(user_id):
    url = 'https://api.twitch.tv/helix/streams?user_id=' + user_id
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    stream_data = json_data["data"][0]
    if not stream_data:
        return False
    else:
        return stream_data

def get_clip_data(clip_id):
    url = 'https://api.twitch.tv/helix/clips?id=' + clip_id
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    clip_data = json_data["data"][0]
    return clip_data

def using_pagination(url):
    list = []
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    list.extend(json_data["data"])
    while json_data["pagination"]:
        next_url = url + '&after=' + json_data["pagination"]["cursor"]
        req = requests.get(next_url, headers=headers)
        json_data = json.loads(req.text)
        list.extend(json_data["data"])
    return list

def get_follow_data(user_id):
    url = 'https://api.twitch.tv/helix/users/follows?from_id=' + user_id + '&first=100'
    follow_data = using_pagination(url)
    return follow_data

def get_follower_data(user_id):
    url = 'https://api.twitch.tv/helix/users/follows?to_id=' + user_id + '&first=100'
    follower_data = using_pagination(url)
    return follower_data

def get_clip_list(user_id, start_time, end_time):
    url = 'https://api.twitch.tv/helix/clips?broadcaster_id=' + user_id + '&first=100&started_at=' + start_time + '&ended_at=' + end_time
    clip_list = using_pagination(url)
    return clip_list