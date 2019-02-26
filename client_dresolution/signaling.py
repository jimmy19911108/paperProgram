'''
signal module
'''

import socket
import network_interface as net_if


class Signal():
    '''
    signal
    '''

    sock = socket.socket()

    def __init__(self, local_id):

        self.local_id = local_id

    def socket_close(self, stun):
        '''
        close socket;
        1 for delete local id from the signaling server;
        0 for keep local id in the signaling server
        '''

        # close socket and delete local id from the signaling server
        if stun:
            self.sock.send(("close " + self.local_id).encode("utf-8"))

        self.sock.close()

    def receive(self):
        '''
        receive data and decode
        '''

        try:
            return self.sock.recv(1024).decode("utf-8").split(" ")
        except:
            print("ERROR: fail to reveive data")
            self.socket_close(0)
            exit()

    def bind_with_remote_user(self, remote_id, candidate, nat_type):
        '''
        bind with remote user on sinalling server
        '''

        self.sock.send(("bind " + self.local_id + " " + candidate + " " + remote_id + " " + nat_type).encode("utf-8"))

        # waiting for signaling server return "ok"
        rec_data = self.receive()
        if rec_data[0] == "ok":
            print("LOG: binding success")
            return rec_data[1], rec_data[2]
        else:
            print("WARRNING: remote user is busy")
            return False, False

    def register(self):
        '''
        regist and check permission
        '''

        try:
            data = ("register %s %s:54320" % (self.local_id, net_if.get_local_ip())).encode("utf-8")
            self.sock.send(data)
        except BrokenPipeError:
            print("ERROR: can not send data")
            exit()

        rec_data = self.receive()
        if rec_data[0] == "ok":
            print("LOG: successful registration")
            return True
        else:
            print("ERROR: Permision denied")
            return False

    def socket_open(self):
        '''
        open a socket for signaling server
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("LOG: Socket open")
        except:
            print("ERROR: Fail to open socket")
            exit()

        server_ip, server_port = net_if.get_signalling_server()

        try:
            self.sock.connect((server_ip, server_port))
            print("LOG: connected to signaling server")
        except:
            print("ERROR: Fail to connect to signaling server")
            exit()

    def request_controller_ip(self, area):
        '''
        request local controller's ip
        '''

        self.sock.send(("requestCIP " + area).encode("utf-8"))
        rec_data = self.receive()

        return rec_data[0]
