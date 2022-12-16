from function import (file_handle, function, recorder, socket_api, twitch_api, update)
import datetime
import json

twitch_api.get_header_online()

def console_print(text):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'{time} {text}')

user_login = ['moonlightinthenightsky_', 'zomul_e', 'momilsoba', 'foxb_', 'wmmmjs', 'dookongc_manager', 'mokonekomiyu', 'haumpah', 'dookongc', 'ryung971219', 'liyel', 'stickybomb_official']
user_login = user_login[1]

user_login = 'youna1113'
user_id = twitch_api.get_id_from_login(user_login)

follow_list = twitch_api.get_follow_data(user_id)

for i in follow_list:
    print("{} {}".format(i['followed_at'], i['to_name']))