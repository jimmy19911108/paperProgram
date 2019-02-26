'''
access the information of turn loading
'''

import sqlite3


class TurnDB():
    
    def __init__(self):
        
        self.turn_conn = sqlite3.connect('turn.db')
        self.turn_curs = self.turn_conn.cursor()
        self.turn_curs.execute('''CREATE TABLE IF NOT EXISTS turn
        (turn_addr VARCHAR(15) PRIMARY KEY,
         loading REAL,
         history REAL,
         time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')

    def get_turn_info(self, addr):
        '''
        get the info of the turn server
        '''

        self.turn_curs.execute(
            '''SELECT * from turn where turn_addr = ?''', (addr,))

        # return None if doesn't exist
        return self.turn_curs.fetchone()
    
    def get_min_loading_turn_addr(self):
        '''
        get the info of the turn server which has the minimum loading
        '''

        self.turn_curs.execute(
            '''SELECT turn_addr, history, loading FROM turn WHERE loading = 
            (SELECT min(loading) FROM turn)''')
        
        turn_info = self.turn_curs.fetchone()
        print(turn_info)

        if turn_info[2] > 80:
            return None
        else:
            return turn_info[0]

    def update_turn_info(self, addr, loading, history):
        '''
        update data of the turn server
        '''

        self.delete_turn_info(addr)
        self.add_turn_info(addr, loading, history)

    def add_turn_info(self, addr, loading, history = 0.0):
        '''
        add the turn server into the database
        '''

        ins = 'INSERT INTO turn\
         (turn_addr, loading, history) VALUES(?, ?, ?)'

        self.turn_curs.execute(ins, (addr, loading, history))
        self.turn_conn.commit()

    def delete_turn_info_disconnect(self):
        '''
        delete the turn server if it doesn't send data over 6 time windows(30 mins)
        '''

        pass

    def delete_turn_info(self, addr):
        '''
        delete turn server
        '''

        self.turn_curs.execute(
            '''DELETE FROM turn where turn_addr = ?''', (addr,))
        self.turn_conn.commit()
