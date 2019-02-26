'''
data module
'''

import ctller_manipulation as ctlm
import client_manipulation as clim
import turn_manipulation as tm


class DataManipulation():
    '''
    data manipulation
    '''

    def __init__(self):

        self.request_state = ("find", "turn")
        self.client_handler = clim.ClientManipulation()
        self.ctller_handler = ctlm.CtllerManipulation()

    def data_handler(self, addr, data):
        '''
        data handler
        '''

        # find
        if data[0] == self.request_state[0]:
            same_area = self.client_handler.check_client_area(data[3])
            if same_area:
                turn_ip = self.client_handler.find_turn()
            
            if not same_area or not turn_ip:
                #send to upper layer
                self.ctller_handler.upper_layer_turn(data)

        #turn
        elif data[0] == self.request_state[2]:
            pass
