'''
handle the turn server data
'''

import socket


class TurnProcedure():

    def __init__(self, turn_ip):
        self.sock = socket.socket()
        self.turn_ip = turn_ip
    
    def open_socket(self):
        '''
        open a socket for turn server
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("LOG: opened local socket")
        except:
            print("ERROR: Fail to open socket")
            exit()

    def send_data(self, msg, port):
        '''
        send message to turn server
        '''
        self.sock.sendto(msg.encode("utf-8"), (self.turn_ip, port))

    def allocate_request(self, client_id, remote_id):
        '''
        send allocate request to turn server
        '''

        self.send_data(("allocate " + client_id + " " + remote_id), 3478)
        
        msg, addr = self.sock.recvfrom(1484)

        msg.decode("utf-8").split(" ")

        if msg[0] == "Fail":
            return False
        else:
            return msg

    def binding(self, remote_relay_port):
        '''
        binding with the port of the turn server
        '''

        self.send_data("bind", remote_relay_port)

        msg, addr = self.sock.recvfrom(1484)

        if msg == "ok":
            return True
        else:
            print("ERROR: Relay Fail")
            return False

    def start(self, client_id, remote_id):
        '''
        start turn procedure
        '''

        # server_port[0]: relay port, server_port[1]: remote relay port
        server_port = self.allocate_request(client_id, remote_id)

        if server_port:
            if self.binding(server_port[1]):
                return server_port[0]
        else:
            return False
