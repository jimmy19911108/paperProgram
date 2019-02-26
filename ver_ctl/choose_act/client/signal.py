'''
signal module
'''

import socket
import network_control as netc


class Signal():
    '''
    signal
    '''

    sock = socket.socket()

    def __init__(self, local_id):

        self.local_id = local_id

    def socket_close(self):
        '''
        close socket
        '''

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
            self.socket_close()
            exit()

    def bind_waiting(self):
        '''
        waiting for bind request
        '''

        self.sock.send("bindwaiting " + self.local_id)

        while True:
            rec_data = self.receive()
            #print(rec_data)

            while rec_data[0] == "bind":
                input_data = input("accept to bind with user %s y/n?" % rec_data[1])
                # local user comfirms to bind with the user who send this request
                if input_data == "y":
                    return rec_data[1], rec_data[2]
                # local user rejects to bind with the user who send this request
                elif input_data == "n":
                    self.sock.send("reject")
                    break
                else:
                    print("ERROR: must input 'y' or 'n'")

    def bind_with_remote_user(self, remote_id, candidate):
        '''
        bind with remote user on sinalling server
        '''

        self.sock.send(("bind " + self.local_id + " " + remote_id + " " + candidate).encode("utf-8"))

        # waiting for signaling server return "ok"
        rec_data = self.receive()
        if rec_data[0] == "ok":
            print("LOG: binded successfully")
            return rec_data[1]
        else:
            print("WARRNING: remote user is busy")
            return False

    def reply_bind_with_remote_user(self, remote_id, candidate):
        '''
        reply bind request
        '''

        self.sock.send("replybind " + self.local_id + " " + remote_id + " " + candidate)
        print("LOG: reply bind")

    def register(self):
        '''
        regist and check permission
        '''

        try:
            data = ("register %s %s" % (self.local_id, netc.get_local_ip())).encode("utf-8")
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
            print("LOG: opened local socket")
        except:
            print("ERROR: Fail to open socket")
            exit()

        server_ip, server_port = netc.get_signalling_server()

        try:
            self.sock.connect((server_ip, server_port))
            print("LOG: connected to signaling server")
        except:
            print("ERROR: Fail to connect to signaling server")
            exit()
