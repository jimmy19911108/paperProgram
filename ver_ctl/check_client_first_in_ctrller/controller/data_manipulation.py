'''
data module
'''

import ctrller_manipulation as ctrlm
import client_manipulation as clim
import turn_manipulation as tm


class DataManipulation():
    '''
    data manipulation
    '''

    def __init__(self):

        self.request_state = ("find", "turn", "turn_disconnect")
        self.client_handler = clim.ClientManipulation()
        self.ctller_handler = ctrlm.CtllerManipulation()
        self.turn_handler = tm.TurnManipulation()

    def data_handler(self, addr, data):
        '''
        data handler
        '''

        # find
        if data[0] == self.request_state[0]:
            turn_ip = self.client_handler.find_procedure(data)
            
            if not turn_ip:
                #send to upper layer
                return self.ctller_handler.upper_layer_turn(data)

            return turn_ip

        #turn
        elif data[0] == self.request_state[1]:
            print("LOG:TURN server " + addr[0] + " connected")
            self.turn_handler.turn_loading(data[1], data[2], data[3], data[4], addr)
        
        #turn disconnect
        elif data[0] == self.request_state[2]:
            print("LOG:TURN server " + addr[0] + " disconnected")
            self.turn_handler.turn_disconnect(addr)

        return False
