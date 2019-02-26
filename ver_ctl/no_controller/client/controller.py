'''
controller module
'''

import socket

class Controller():
    
    def __init__(self, ctl_ip):

        self.ctl_ip = ctl_ip

    def socket_open(self):
        '''
        open a socket for controller
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ctl_ip, 8000))
            print("LOG: connected to controller")
        except:
            print("ERROR: Fail to open socket")
            exit()
