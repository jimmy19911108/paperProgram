'''
manipulate the action for controller in the upper layer
'''

import socket

class CtllerManipulation():
    
    def __init__(self):
        self.sock = socket.socket()
        self.upper_ip = "192.168.1.1"
        self.cloud_ip = "192.168.1.1"

    def comf_connection(self):
        '''
        comferm the connection with upper layer controller
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("LOG: opened local socket")
        except:
            print("ERROR: Fail to open socket")
            exit()

        try:
            self.sock.connect((self.upper_ip, 5000))
            print("LOG: Checked connection")
            ctller_layer = "upper"
        except:
            print("LOG: Fail to connect to the controller in the upper layer")
            print("LOG: Try the controller in the cloud layer")

            try:
                self.sock.connect((self.cloud_ip, 5000))
                print("LOG: Checked connection")
                ctller_layer = "cloud"
            except:
                print("LOG: Fail to connect to the controller in the cloud layer")
                exit()

        self.sock.close()
        
        return ctller_layer
    
    def socket_open(self):
        '''
        open a socket for controller
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("LOG: opened local socket")
        except:
            print("ERROR: Fail to open socket")
            exit()

        try:
            self.sock.connect((server_ip, server_port))
            print("LOG: connected to signaling server")
        except:
            print("ERROR: Fail to connect to the controller")
            exit()

    def send_message(self, msg):
        '''
        encode and send message
        '''

        self.sock.send(msg.encode("utf-8"))
        return self.receive_data()

    def receive_data(self):
        '''
        receive data and decode
        '''

        try:
            return self.sock.recv(1024).decode("utf-8").split(" ")
        except:
            print("ERROR: fail to reveive data")
            self.sock.close()
            exit()

    def upper_layer_turn(self, msg):
        '''
        send request to the controller in the uppper layer\n
        and find the turn server
        '''
    
        self.send_message(msg[0] + " " + msg[1] + " " + msg[2] + " " + msg[3])

