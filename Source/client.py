# -*- coding: utf-8 -*-

from client import *
from core import *
from db import *

#import xmlrpc.client

#s = xmlrpc.client.ServerProxy('http://localhost:8000', use_builtin_types=True)

#collection = ClientCollection(s)

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
