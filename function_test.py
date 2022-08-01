from function import (file_handle, function, recorder, socket_api, twitch_api, update, upnp_api)

client_id = '5ayor8kn22hxinl6way2j1ejzi41g2'
client_secret = '8tp18ssnpzbrzyyf0he83q3lsfayyx'
access_token = twitch_api.get_access_token(client_id, client_secret)
twitch_api.get_header(client_id, access_token)

user_login = ['moonlightinthenightsky_', 'zomul_e']
user_login = user_login[1]
user_id = twitch_api.get_id_from_login(user_login)

# follow_list = twitch_api.get_follow_data(user_id)
# list = []
# for streamer in follow_list:
#     list.append(streamer['to_name'])
# print(list)
# print(len(list))

list = twitch_api.get_vod_data(user_id, 'month')
print(list)