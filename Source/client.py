# -*- coding: utf-8 -*-

from client.view import *
from client.model import *
from core import *

collection = ClientCollection()
common = Common()

## TEMP
account = Account.load(collection, 1)
common.account = account
common.event_clicked = Event.load(collection, 1) # HUMMM
common.day = datetime(2019, 2, 18)
## TEMP

win = Window(common)
win.main()

collection.close()
