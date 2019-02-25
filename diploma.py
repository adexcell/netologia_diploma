import requests
import json
import time
TOKEN = 'cda3b45cbeee1e6218c86b84d7b963e0bcf347ba1482c52db35cc6965b9954a428d001e6dbb0bf1f97e70'


if __name__ == '__main__':
    main_user = 171691064 #(eshmargunov)
    response_main_user_id = requests.get('https://api.vk.com/method/users.get', {'access_token': TOKEN, 'user_ids': main_user, 'v': '5.92'})
    main_user_id = response_main_user_id.json()['response'][0]['id']
    main_params = {
        'access_token': TOKEN,
        'user_id': main_user_id,
        'v': '5.92'
    }
    response_groups_main = requests.get('https://api.vk.com/method/groups.get', main_params)
    groups_main_ids = response_groups_main.json()['response']['items']
    response_friends = requests.get('https://api.vk.com/method/friends.get', main_params)
    friends_ids = response_friends.json()['response']['items']

    groups_for_compare = []

    for id in friends_ids:
        params = {
            'access_token': TOKEN,
            'user_id': id,
            'v': '5.92'
        }
        groups_of_friend_response = requests.get('https://api.vk.com/method/groups.get', params)
        if 'response' in groups_of_friend_response.json():
            groups_of_friend = groups_of_friend_response.json()['response']['items']
            groups_for_compare.append(groups_of_friend)
        time.sleep(0.334)
        print('.')

    for list_of_groups in groups_for_compare:
        for group in list_of_groups:
            if group in groups_main_ids:
                groups_main_ids.remove(group)


    groups_main_ids_str = ','.join(map(str, groups_main_ids))

    params_for_groups = {
        'access_token': TOKEN,
        'group_ids': groups_main_ids_str,
        'v': '5.92',
        'fields': 'members_count'
    }
    groups_info_responce = requests.get('https://api.vk.com/method/groups.getById', params_for_groups)
    groups_info = groups_info_responce.json()['response']

    for_json = []
    for group in groups_info:
        cell = {
            "name": group['name'],
            "gid": group['id'],
            "members_count": group['members_count']
        }
        for_json.append(cell)
    with open('groups.json', 'w', encoding='utf8') as file:
        json.dump(for_json, file, ensure_ascii=False, indent=2)

    print('End')
