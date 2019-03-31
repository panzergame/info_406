# -*- coding: utf-8 -*-

from client.view import *
from client.model import *
from core import *

collection = ClientCollection()
common = Common(collection)

## TEMP
account = Account.load(collection, 1)
common.account = account
common.user_clicked = list(common.account.users)[0]
common.agenda_displayed = common.user_clicked.agenda
common.event_clicked = None
common.day = datetime(2019, 2, 18)
## TEMP

win = Window(common)
win.main()

collection.close()
