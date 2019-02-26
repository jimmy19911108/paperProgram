'''
manipulate the action for controller in the upper layer
'''

import socket
import network_interface as net_if


class CtrllerManipulation():
    
    def __init__(self):
        self.sock = socket.socket()
    
    def socket_open(self):
        '''
        open a socket for controller
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("LOG: Opened local socket")
        except:
            print("ERROR: Fail to open socket")
            exit()

        try:
            self.sock.connect((net_if.get_upper_layer(), 5000))
            print("LOG: Connected to controller in the upper layer")
        except:
            try:
                self.sock.connect((net_if.get_cloud_layer(), 5000))
                print("LOG: Connected to controller in the cloud layer")
            except:
                print("LOG: Fail to connect to the controller in the cloud layer")
                self.sock.close()
                return False

        return True

    def send_message(self, msg):
        '''
        encode and send message
        '''

        self.sock.send(msg.encode("utf-8"))

    def receive_data(self):
        '''
        receive data and decode
        '''

        try:
            return self.sock.recv(1024).decode("utf-8")
        except:
            print("ERROR: fail to reveive data")
            self.sock.close()
            exit()

    def upper_layer_turn(self, msg):
        '''
        send request to the controller in the uppper layer\n
        and find the turn server
        '''
    
        if self.socket_open():
            self.send_message("c" + msg[0] + " " + msg[1] + " " + msg[2] + " " + msg[3])
            return self.receive_data()
        else:
            print("LOG: Fail to connect to upper layer controller")
            return False

