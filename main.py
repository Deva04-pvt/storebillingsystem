from tkfunctions import *
password = ObtainSqlPassword()
ExistingUsers = GetUsers()
if not ExistingUsers:
    CreateFirstWindow()
else:
    CreateLoginWindow()
CreateMainWindow()
CallUpdateActivity()
