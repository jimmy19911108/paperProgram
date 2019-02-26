'''
client manipulation
'''

import turn_db_manipulation as tdbm
import client_db_manipulation as cdbm
import time


class ClientManipulation():
    
    def __init__(self):
        self.turn_db = tdbm.TurnDB()
        self.client_db = cdbm.ClientDBManipulation()
        self.local_area = {"TW"}

    def get_remote_client_turn(self, client, remote_client):
        '''
        check if the remote user has gotten the address of turn server
        '''
        
        while True:
            remote_client_info = self.client_db.get_client(remote_client)

            if remote_client_info:
                return remote_client_info[2]
            
            time.sleep(0.1)

    def find_procedure(self, data):
        '''
        start procedure for finding a turn server\n
        Return: /False/ for can not operate in this layer\n
            /Turn IP/ for success
        '''

        # check if the remote client's area is as same as this controller
        if data[3] in self.local_area:
            # if client id > remote client id, find a available turn address
            # or waiting for remote client get the turn address
            if data[1] > data[2]:
                turn_ip = self.turn_db.get_min_loading_turn_addr()
                self.client_db.add_client(data[1], data[2], turn_ip)

                if turn_ip == "0.0.0.0":
                    return False

            else:
                turn_ip = self.get_remote_client_turn(data[1], data[2])
                
                if turn_ip == "0.0.0.0":
                    self.client_db.delete_client(data[2])
                    return False
                else:
                    self.client_db.add_client(data[1], data[2], turn_ip)

            return turn_ip
        else:
            return False
        
    def get_turn_addr(self, client_id):
        '''
        return turn addr
        '''

        client_info = self.client_db.get_client(client_id)

        return client_info[2]
