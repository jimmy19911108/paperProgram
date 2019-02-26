'''
data module
'''

import ctrller_manipulation as ctrlm
import client_manipulation as clim
import turn_manipulation as tm
import network_interface as net_if
import client_db_manipulation as cdbm


class DataManipulation():
    '''
    data manipulation
    '''

    def __init__(self):

        self.request_state = ("find", "cfind", "cget", "turn", "turn_disconnect", "start", "close")
        self.client_handler = clim.ClientManipulation()
        self.ctrller_handler = ctrlm.CtrllerManipulation()
        self.turn_handler = tm.TurnManipulation()

    def data_handler(self, addr, data):
        '''
        data handler
        '''

        # find & cfind
        if data[0] in self.request_state[0:2]:
            turn_ip = self.client_handler.find_procedure(data)
            
            # can find an available turn server
            if turn_ip:
                # find
                if data[0] == self.request_state[0]:
                    return turn_ip + " " + str(self.client_handler.get_turn_resolution(turn_ip))
                # cfind
                else:
                    return "ctrl " + net_if.get_server_addr()

            # client's location are different with controller
            else:
                #send to upper layer
                ctrl_ip = self.ctrller_handler.upper_layer_turn(data)
                if ctrl_ip:
                    return ctrl_ip
                else:
                    return "Fail"

        # cget
        elif data[0] == self.request_state[2]:
            return self.client_handler.get_turn_addr(data[1])

        # turn
        elif data[0] == self.request_state[3]:
            print("LOG:TURN server " + addr[0] + " connected")
            self.turn_handler.turn_loading(data[1], data[2], data[3], addr)

        # turn disconnect
        elif data[0] == self.request_state[4]:
            print("LOG:TURN server " + addr[0] + " disconnected")
            self.turn_handler.turn_disconnect(addr)

        # start
        elif data[0] == self.request_state[5]:
            return str(self.client_handler.client_start_relay(data[1]))

        # close
        elif data[0] == self.request_state[6]:
            cdbm.ClientDBManipulation().delete_client(data[1])
            return "ok"

        return False
