from function import (twitch_api, recorder, update)

client_id = '5ayor8kn22hxinl6way2j1ejzi41g2'
client_secret = '8tp18ssnpzbrzyyf0he83q3lsfayyx'
access_token = twitch_api.get_access_token(client_id, client_secret)
twitch_api.get_header(client_id, access_token)

# user_login = 'moonlightinthenightsky_'
user_login = 'zomul_e'
# user_login = 'yoshi_bl'
user_id = twitch_api.get_id_from_login(user_login)