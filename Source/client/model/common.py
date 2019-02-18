# -*- coding: utf-8 -*-

from core import user


class Common:
    def __init__(self):
        self._user_clicked = None

    @property
    def user_clicked(self):
        return self._user_clicked

    @user_clicked.setter
    def user_clicked(self, user):
        self._user_clicked = user
