'''
a handler for client database
'''

import sqlite3


class ClientDBManipulation():
    
    def __init__(self):
        self.client_conn = sqlite3.connect('client.db')
        self.client_curs = self.client_conn.cursor()
        self.client_curs.execute('''CREATE TABLE IF NOT EXISTS client
        (client_id VARCHAR(20) PRIMARY KEY,
         remote_client_id VARCHAR(20),
         turn_addr VARCHAR(20))''')

    def add_client(self, client, remote_client, turn_addr = "0.0.0.0"):
        '''
        add a client
        '''
        
        ins = 'INSERT INTO client\
         (client_id, remote_client_id, turn_addr) VALUES(?, ?, ?)'

        self.client_curs.execute(ins, (client, remote_client, turn_addr))
        self.client_conn.commit()
    
    def delete_client(self, client):
        '''
        delete a client
        '''
        
        self.client_curs.execute(
            '''DELETE FROM client where client_id = ?''', (client,))
        self.client_conn.commit()

    def get_client(self, client):
        '''
        return client id, remote client id, turn address
        '''
        
        self.client_curs.execute(
            '''SELECT * from client where client_id = ?''', (client,))
        return self.client_curs.fetchone()

    def update_turn_addr(self, client, turn_addr):
        '''
        update the turn address of the client
        '''

        ins = 'UPDATE client SET turn_addr = ? WHERE client_id = ?'

        self.client_curs.execute(ins, (turn_addr, client,))
        self.client_conn.commit()