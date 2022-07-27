from function import (twitch_api, recorder, update)

client_id = '5ayor8kn22hxinl6way2j1ejzi41g2'
client_secret = '8tp18ssnpzbrzyyf0he83q3lsfayyx'
access_token = twitch_api.get_access_token(client_id, client_secret)
twitch_api.get_header(client_id, access_token)

# user_login = 'moonlightinthenightsky_'
user_login = 'zomul_e'
# user_login = 'yoshi_bl'
user_id = twitch_api.get_id_from_login(user_login)

#clip_list = twitch_api.get_clip_list(user_id, '2022-07-25T00:00:00Z', '2022-07-26T23:59:59Z')

#list = []
#for clip in clip_list:
#    if clip['creator_name'] == '우물쬬물하는너굴짱':
#        list.append(clip['url'])

#for data in list:
#    print(data)

chat_list = twitch_api.get_chat_from_vod('1535357097')
for chat in chat_list:
    print(chat['_id'])
print(chat_list)