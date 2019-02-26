'''
handle the turn server data
'''

import socket


class TurnProcedure():

    def __init__(self, turn_ip):
        #print("LOG: TurnProcedure Constructor")
        #print("LOG: open socket")
        self.open_socket()
        #print("LOG: save turn ip")
        self.turn_ip = turn_ip
    
    def open_socket(self):
        '''
        open a socket for turn server
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("LOG: Socket opened")
        except:
            print("ERROR: Fail to open socket")
            exit()

    def send_data(self, msg, port):
        '''
        send message to turn server
        '''

        #print("LOG: Send data --- " + msg + " through --- " + str(port))
        self.sock.sendto(msg.encode("utf-8"), (self.turn_ip, port))

    def allocate_request(self, client_id, remote_id):
        '''
        send allocate request to turn server
        '''

        #print("LOG: Allocate request")
        self.send_data(("allocate " + client_id + " " + remote_id), 3478)
        
        #print("LOG: Receive")
        msg, _ = self.sock.recvfrom(1024)
        #print("LOG: Receive from " + str(addr) + " --- " + msg)

        #print("LOG: msg decode")
        msg = msg.decode("utf-8").split(" ")

        if msg[0] == "Fail":
            #print("LOG: allocate fail, return false")
            return False
        else:
            #print("LOG: allocate success, return msg")
            return msg

    def binding(self, remote_relay_port):
        '''
        binding with the port of the turn server
        '''

        #print("LOG: Binding with " + remote_relay_port)
        self.send_data("bind", int(remote_relay_port))

        #print("LOG: Receive")
        msg, _ = self.sock.recvfrom(1024)
        #print("LOG: Receive from " + str(addr) + " --- " + msg)

        #print("LOG: msg decode")
        msg = msg.decode("utf-8")

        if msg == "ok":
            #print("LOG: binding success, return true")
            return True
        else:
            #print("ERROR: Relay Fail")
            return False

    def start(self, client_id, remote_id):
        '''
        start turn procedure
        '''

        #print("LOG: Start turn procedure")
        # server_port[0]: relay port, server_port[1]: remote relay port
        server_port = self.allocate_request(client_id, remote_id)
        #print("LOG: Get turn server port --- " + str(server_port))

        if server_port:
            #print("LOG: Start binding with " + server_port[1])
            if self.binding(server_port[1]):
                #print("LOG: Binding success, return " + server_port[0])
                local_port = self.sock.getsockname()[1]
                self.sock.close()
                return server_port[0], local_port
        
        #print("LOG: Binding fail, return false")
        return False, False
