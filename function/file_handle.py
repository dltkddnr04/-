import json
import threading

run_queue = []

def make_setting_file():
    setting_file = open('test_setting.json', 'w')
    setting_data = {
        "account": {
        },
        "setting": {
            "download_mode": "",
            "download_path": "",
            "video_type": ""
        },
        "user_data_list": {
            "download_live_stream": {

            }
        }
    }
    setting_file.write(json.dumps(setting_data, indent=4))
    setting_file.close()

def read_setting_file():
    setting_file = open('test_setting.json', 'r')
    setting_data = json.loads(setting_file.read())
    setting_file.close()
    return setting_data

def write_setting_file(setting_data):
    setting_file = open('test_setting.json', 'w')
    setting_file.write(json.dumps(setting_data, indent=4))
    setting_file.close()

def check_key_exist(setting_data, key):
    key_value = key.split('/')

    if key_value[0] in setting_data:
        if key_value[1] in setting_data[key_value[0]]:
            return True
        else:
            return False
    else:
        return False

def add_queue(key, data):
    run_queue.append([key, data])
    return

def execute_queue(key, data):
    setting_json = read_setting_file()
    key_value = key.split('/')
    if check_key_exist(setting_json, key):
        setting_json[key_value[0]][key_value[1]] = data
        write_setting_file(setting_json)
        return True
    else:
        return False

def main():
    while True:
        if len(run_queue) > 0:
            key = run_queue[0][0]
            data = run_queue[0][1]
            if not execute_queue(key, data):
                print('Error: Key not exist')
            run_queue.pop(0)
        else:
            pass

# test code
try:
    open('test_setting.json', 'r')
except FileNotFoundError:
    make_setting_file()

threading.Thread(target=main).start()

add_queue('account/username', 'test')