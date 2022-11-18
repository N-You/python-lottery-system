# coding:utf-8
import json
import os
import time

from common.utils import check_file, timestamp_to_string
from common.error import UserExistsError, RoleError, LevelError
from common.consts import ROLES, FIRSTLEVELS, SECONDLEVELS


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self.__check_user_json()
        self.__check_gift_json()

        self.__init_gifts()

    def __check_user_json(self):
        check_file(self.user_json)

    def __check_gift_json(self):
        check_file(self.gift_json)

    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r') as f:
            data = json.loads(f.read())

        if time_to_str:
            for username, k, v in data.items():
                v['create_time'] = timestamp_to_string(v['create_time'])
                v['update_time'] = timestamp_to_string(v['update_time'])
                data[username] = v

        return data

    def __write_user(self, **user):
        if 'username' not in user:
            raise ValueError('missing username')
        if 'role' not in user:
            raise ValueError('missing role')

        user['active'] = True
        user['create_time'] = time.time()
        user['update_time'] = time.time()
        user['gifts'] = []

        users = self.__read_users()

        if user['username'] in users:
            raise UserExistsError('username %s had exists' % user['username'])

        users.update({user['username']: user})

        json_users = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_users)
        return True

    def __change_role(self, username, role):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        if role not in ROLES:
            raise RoleError('not use role %s' % role)

        user['role'] = role
        user['update_time'] = time.time()
        users[username] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True

    def __change_active(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        user['active'] = not user['active']
        user['update_time'] = time.time()
        users[username] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True

    def __delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        delete_user = users.pop(username)

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)

        return delete_user

    def __read_gifts(self):
        with open(self.gift_json, 'r') as f:
            data = json.loads(f.read())
        return data

    def __init_gifts(self):
        data = {
            'level1': {'level1': {},
                       'level2': {},
                       'level3': {}},
            'level2': {'level1': {},
                       'level2': {},
                       'level3': {}},
            'level3': {'level1': {},
                       'level2': {},
                       'level3': {}}
        }
        gifts = self.__read_gifts()
        if len(gifts) != 0:
            return
        json_data = json.dumps(data)
        with open(self.gift_json,'w') as f:
            f.write(json_data)
        return True

    def __write_gift(self,first_level, second_level, gift_name, gift_count):

        if first_level not in FIRSTLEVELS:
            raise LevelError('firstlevel not exists')
        if second_level not in SECONDLEVELS:
            raise LevelError('secondlevel not exists')

        gifts = self.__read_gifts()

        current_gift_pool = gifts[first_level]
        current_second_gift_pool = current_gift_pool[second_level]

        if gift_count <= 0:
            gift_count = 1

        if gift_name in current_second_gift_pool:
            current_second_gift_pool[gift_name]['count'] = current_second_gift_pool[gift_name]['count'] + gift_count
        else:
            current_second_gift_pool[gift_name] = {
                'name': gift_name,
                'count': gift_count
            }

        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        json_data = json.dumps(gifts)
        with open(self.gift_json,'w') as f:
            f.write(json_data)
        return True


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    print(gift_path)
    print(user_path)
    base = Base(user_json=user_path, gift_json=gift_path)
    # base.write_user(username='lihua',role='admin')
    # base.write_gift(first_level='level1',second_level='level4',gift_name='iphone10',gift_count=10)
