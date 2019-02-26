'''
handle imformation of turn servers
'''

import turn_db_manipulation as tdbm


class TurnManipulation():
    
    def __init__(self):
        self.data_base = tdbm.TurnDB()

    def turn_loading(self):
        pass