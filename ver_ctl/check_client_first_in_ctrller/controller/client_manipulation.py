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

    def check_client_area(self, area):
        '''
        check if the client and controller is in the same area
        '''

        return area in self.local_area

    def find_turn(self):
        '''
        Find an available turn server and return
        '''
        
        return self.turn_db.get_min_loading_turn_addr()

    def check_remote_user_turn(self, client, remote_client):
        '''
        check if the remote user has gotten the address of turn server
        '''

        # add the client to database and set turn address as 0.0.0.0
        self.client_db.add_client(client, remote_client)
        
        while True:
            # get remote client info
            remote_client_info = self.client_db.get_client(remote_client)

            # if the remote client has been assigned the turn address 
            # or send to the controller of upper layer
            if remote_client_info:
                if remote_client_info[2] != "0.0.0.0":
                    # return the turn address
                    return remote_client_info[2]
                # if the remote client has not been assigned the turn address
                else:
                    # keep checking the remote user's info
                    time.sleep(1)
                    continue
            # if the remote user does not exist in the databse
            else:
                return False
    
    def update_clinet_turn_addr(self, client, turn_addr):
        '''
        update the turn address of the client
        '''

    def find_procedure(self, data):
        '''
        start procedure for finding a turn server
        '''

        # check if the remote client's area is as same as this controller
        same_area = self.check_client_area(data[3])

        if same_area:
            # check if the remote user has been assigned the turn address
            turn_ip = self.check_remote_user_turn(data[1], data[2])

            # if the remote user does not exist in the database
            if turn_ip == False:
                # find a turn address
                turn_ip = self.find_turn()

            # update the turn addr
            self.update_clinet_turn_addr(data[1], turn_ip)
        
        if not same_area or not turn_ip:
            return False
        else:
            return turn_ip
