from core import *
from datetime import date

user = User("Toto", "Dupont", "toto@mail.com", "0656565656")
print(user)

slot = Slot(date.today(), 15, 1.5)
print(slot)

presence = Presence(slot, [user])
print(presence)
