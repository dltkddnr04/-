import json
import threading

run_queue = []

def read_file(file_path):
    file = open(file_path, 'r')
    data = file.read()
    file.close()
    return data

def write_file(file_path, data):
    file = open(file_path, 'w')
    file.write(data)
    file.close()
    return

def add_queue(file_path, key, data):
    run_queue.append({'path': file_path, 'key': key, 'data': data})
    return

def check_key_exist(dict, key):
    key_value = key.split('/')

    if key_value[0] in dict:
        if key_value[1] in dict[key_value[0]]:
            return True
        else:
            return False
    else:
        return False

def execute_queue(file_path, key, data):
    file_data = read_file(file_path)
    json_data = json.loads(file_data)
    
    if check_key_exist(json_data, key):
        key_value = key.split('/')
        json_data[key_value[0]][key_value[1]] = data

        write_file(file_path, json.dumps(json_data))
        return True
    else:
        return False

def loop_queue():
    while True:
        if len(run_queue) > 0:
            query = run_queue[0]
            execute_queue(query['path'], query['key'], query['data'])
            run_queue.remove(query)
        else:
            pass

# here is function test code
# threading.Thread(target=loop_queue).start()
# add_queue('setting_test.json', 'account/access_token', 'sexyguy')