'''
handle database
'''

import redis
import sqlite3
import time


class DBManipulation():
    
    def __init__(self):
        
        # redis
        self.send_time = redis.StrictRedis(host = 'localhost', port = 6379)
        
        # sqlite3
        self.client_data_conn = sqlite3.connect('client_data.db')
        self.client_data_curs = self.client_data_conn.cursor()
        self.client_data_curs.execute('''CREATE TABLE IF NOT EXISTS client_data
        (client_id VARCHAR(20) PRIMARY KEY,
         server_reflex_address VARCHAR(20),
         relay_port VARCHAR(5),
         remote_id VARCHAR(20),
         port_state BOOLEAN)''')
    
    def set_time(self):
        '''
        =Redis= set new time to current time
        '''

        self.send_time.set("new_time", time.time())

    def set_time_to_zero(self):
        '''
        =Redis= set new time to zero for sending resource usage
        '''

        self.send_time.set("new_time", 0)

    def get_time(self):
        '''
        =Redis= set new time 
        '''

        new_time = self.send_time.get("new_time")

        if new_time == self.send_time.get("old_time"):
            return None
        else:
            self.send_time.set("old_time", new_time)
            return new_time

    def flush_db(self):
        '''
        =Redis= flush redis databases
        '''

        self.send_time.flushall()

    def set_client_data(self, client_id, server_reflex_address, relay_port, remote_id):
        '''
        =sqlite3= set client data
        '''

        ins = 'INSERT INTO client_data\
         (client_id, server_reflex_address, relay_port, remote_id, port_state) VALUES(?, ?, ?, ?, ?)'

        self.client_data_curs.execute(ins, (client_id, server_reflex_address, relay_port, remote_id, 0))
        self.client_data_conn.commit()
    
    def get_client_by_id(self, client_id):
        '''
        =sqlite3= get client data
        '''

        ins = 'SELECT * from client_data where client_id = ?'

        self.client_data_curs.execute(ins, (client_id,))
        
        return self.client_data_curs.fetchone()

    def get_client_by_port(self, port):
        '''
        =sqlite3= get client data
        '''

        ins = 'SELECT * from client_data where relay_port = ?'

        self.client_data_curs.execute(ins, (port,))

        return self.client_data_curs.fetchone()

    def update_client_port_state(self, server_reflex_address):
        '''
        =sqlite3= update client's port state
        '''

        ins = 'UPDATE client_data SET port_state = ? WHERE client_id = ?'

        self.client_data_curs.execute(ins, (1, server_reflex_address,))
        self.client_data_conn.commit()

    def delete_client_data(self, client_id):
        '''
        =sqlite3= delete client's data
        '''

        print(client_id + " disconnect")
        
        ins = 'DELETE FROM client_data where client_id = ?'

        self.client_data_curs.execute(ins, (client_id,))
        self.client_data_conn.commit()
