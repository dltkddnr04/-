import requests
import json

def get_release_data():
    url = 'https://api.github.com/repos/dltkddnr04/Twitch-Auto-Recorder/releases/latest'
    req = requests.get(url)
    json_data = json.loads(req.text)
    return json_data

def get_latest_version():
    json_data = get_release_data()
    latest_version = json_data['name'].replace("v", "")
    return latest_version

def get_download_url():
    json_data = get_release_data()
    download_url = json_data["assets"][0]["browser_download_url"]
    return download_url

def get_patch_notes():
    json_data = get_release_data()
    patch_notes = json_data["body"]
    return patch_notes

def compare_version(current_version, latest_version):
    current_version = current_version.split(".")
    latest_version = latest_version.split(".")

    if int(current_version[0]) < int(latest_version[0]):
        return True
    elif int(current_version[0]) == int(latest_version[0]):
        if int(current_version[1]) < int(latest_version[1]):
            return True
        elif int(current_version[1]) == int(latest_version[1]):
            if int(current_version[2]) < int(latest_version[2]):
                return True
            else:
                return False
        else:
            return False