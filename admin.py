# coding:utf-8

import os

from base import Base
from common.error import NotUserError, UserActiveError, RoleError


class Admin(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)
        if current_user == None:
            raise NotUserError('not users %s' % self.username)

        if current_user.get('active') == False:
            raise UserActiveError('the user %s had not use' % self.username)

        if current_user.get('role') != 'admin':
            raise RoleError('permission by admin')

        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')

    def add_user(self, username, role):
        self.__check('permission')

        self._Base__write_user(username=username, role=role)

    def update_user_active(self, username):
        self.__check('permission')
        self._Base__change_active(username=username)

    def update_user_role(self, username, role):
        self.__check('permission')
        self._Base__change_role(username=username, role=role)

    def add_gift(self, first_level, second_level, gift_name, gift_count):
        self.__check('permission')
        self._Base__write_gift(first_level=first_level, second_level=second_level, gift_name=gift_name,
                               gift_count=gift_count)

    def delete_gift(self, first_level, second_level, gift_name):
        self.__check('permission')
        self._Base__delete_gift(first_level=first_level, second_level=second_level, gift_name=gift_name)
        return True

    def update_gift(self, first_level, second_level, gift_name, gift_count):
        self.__check('permission')
        self._Base__gift_update(first_level=first_level, second_level=second_level, gift_name=gift_name,
                                gift_count=gift_count, is_admin=True)

    def __check(self, message):
        self.get_user()
        if self.role != 'admin':
            raise Exception(message)


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    admin = Admin('lihua', user_path, gift_path)
    # admin.update_user_active(username='xiaozhang')
    # admin.add_gift(first_level='level1',second_level='level1',gift_name='糖豆',gift_count=12)
    admin.update_gift(first_level='level1', second_level='level1', gift_name='糖豆', gift_count=1000)
