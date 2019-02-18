# -*- coding: utf-8 -*-

from core import user


class Common:
    def __init__(self, user_clicked):
        self.user_clicked = user_clicked

    def set_user_clicked(self, user_clicked):
        # Passer par un setter pour pouvoir notifier les changements
        self.user_clicked = user_clicked


        print(self.user_clicked.first_name)
