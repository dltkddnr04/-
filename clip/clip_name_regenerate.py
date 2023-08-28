import os
import sys
import json

user_login = "ryung971219"

# open ryung971219_clippy.json to get the list of clips
with open('clips/{}_clippy.json'.format(user_login), 'r') as f:
    data = json.load(f)

for clip in data:
    title = clip['title']
    created_at = clip['created_at'].split('.')[0]

    privious_file_name = clip['hash_id']
    final_file_name = f'[{created_at}] {title}.mp4'

    # rename the file
    os.rename(f'clips/{user_login}/{privious_file_name}.mp4', f'clips/{user_login}/{final_file_name}')