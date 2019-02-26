'''
access the information of turn loading
'''

import sqlite3
from datetime import datetime
from datetime import timedelta


class TurnDB():
    
    def __init__(self):
        
        self.turn_conn = sqlite3.connect('turn.db')
        self.turn_curs = self.turn_conn.cursor()
        self.turn_curs.execute('''CREATE TABLE IF NOT EXISTS turn
        (turn_addr VARCHAR(15) PRIMARY KEY,
         loading REAL,
         conn_state BOOLEAN,
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

        #self.turn_curs.execute(
        #    '''SELECT turn_addr, history, loading FROM turn WHERE loading = 
        #    (SELECT min(loading) FROM turn)''')

        self.turn_curs.execute(
            '''SELECT * FROM turn WHERE conn_state = 1 AND loading < 100 ORDER BY loading''')
        
        turn_info = self.turn_curs.fetchall()

        if turn_info:
            for i in range(0, len(turn_info)):
                data_time = datetime.strptime(turn_info[i][3], "%Y-%m-%d %H:%M:%S")
                if (data_time - data_time.now()) > timedelta(seconds = 185):
                    self.update_turn_info(turn_info[i][0], turn_info[i][1], 0)
                else:
                    return turn_info[i][0]

        return "0.0.0.0"

    def update_turn_info(self, addr, loading, conn_state = 1):
        '''
        update data of the turn server
        '''

        self.delete_turn_info(addr)
        self.add_turn_info(addr, loading, conn_state)

    def add_turn_info(self, addr, loading, conn_state = 1):
        '''
        add the turn server into the database
        '''

        ins = 'INSERT INTO turn\
         (turn_addr, loading, conn_state) VALUES(?, ?, ?)'

        self.turn_curs.execute(ins, (addr, loading, conn_state))
        self.turn_conn.commit()

    def delete_turn_info_disconnect(self):
        '''
        delete the turn server if it doesn't send data over 3 time windows(9 mins)
        '''

        pass

    def delete_turn_info(self, addr):
        '''
        delete turn server
        '''

        self.turn_curs.execute(
            '''DELETE FROM turn where turn_addr = ?''', (addr,))
        self.turn_conn.commit()
