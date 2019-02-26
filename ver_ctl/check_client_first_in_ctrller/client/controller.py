'''
controller module
'''

import socket

class Controller():
    
    def __init__(self, ctrller_ip):

        self.ctrller_ip = ctrller_ip

    def socket_open(self):
        '''
        open a socket for controller
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ctrller_ip, 5000))
            print("LOG: connected to controller")
            return True
        except:
            print("ERROR: Fail to open socket")
            return False

    def socket_close(self):
        self.sock.close()

    def request_turn(self, local_id, remote_id, remote_area):
        '''
        request the IP of TURN server
        '''

        self.sock.send(("find " + local_id + " " + remote_id + " " + remote_area).encode("utf-8"))

        return self.sock.recv(1024).decode("utf-8").split(" ")

    def set_ctrller_addr(self, ctrller_ip):
        '''
        set controller ip
        '''

        self.ctrller_ip = ctrller_ip
