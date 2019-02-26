'''
handle the relay operation
'''

import socket
import network_interface as net_if
import multiprocessing as mp
import time
import db_manipulation as dbm


class RelayManipulation():

    def __init__(self):
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.setblocking(0)

    def subprocess(self, func):
        '''
        fork a process
        '''

        proc = mp.Process(target = func)
        proc.start()


    def open_socket(self):
        '''
        open udp relay socket
        '''

        try:
            self.udp_sock.bind((net_if.get_server_ip(), 0))
        except:
            return False

        print("LOG: Open Relay Socket")

        self.subprocess(self.receive_remote_port)

        return str(self.udp_sock.getsockname()[1])

    def relay_start(self):
        '''
        receive data
        '''

        recv_time = time.time()

        # if not receive data over 30 seconds, diconnect and delete client info
        while True:
            try:
                data, addr = self.udp_sock.recvfrom(1484)
            except socket.error:
                if time.time()-recv_time >= 30:
                    break
                continue
            else:
                recv_time = time.time()
                self.udp_sock.sendto(data, self.remote_address)
        
        dbm.DBManipulation().delete_client_data(self.client_data[0])

    def receive_remote_port(self):
        '''
        waiting for puching packets and reply
        '''

        while True:
            try:
                data, addr = self.udp_sock.recvfrom(1484)
            except socket.error:
                print(socket.error)
            else:
                data = data.decode("utf-8")

                if data == "bind":
                    self.remote_address = addr

                    self.waiting_remote_port_ready()
                    self.udp_sock.sendto("ok".encode("utf-8"), addr)
                    
                    self.relay_start()
                    
                    self.udp_sock.close()
                    break
            

    def waiting_remote_port_ready(self):
        '''
        return true if the remote port have been ready
        '''

        self.client_data = dbm.DBManipulation().get_client_by_port(self.udp_sock.getsockname()[1])
        dbm.DBManipulation().update_client_port_state(self.client_data[0])

        while True:
            # client_data[3] == remote client's id
            if dbm.DBManipulation().get_client_by_id(self.client_data[3])[4]:
                break
            time.sleep(0.5)
