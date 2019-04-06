# -*- coding: utf-8 -*-

from client.view import *
from client.model import *
from core import *

collection = ClientCollection()
common = Common(collection)

## TEMP
account = collection.load_account("root", "root")
common.account = account
common.user_clicked = list(common.account.users)[0]
common.agenda_displayed = common.user_clicked.agenda
common.event_clicked = None
common.day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
## TEMP

win = Window(common)
win.main()

collection.close()
