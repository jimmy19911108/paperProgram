'''
handle connections of clients and the relay of stream
'''

import socket
import time
import signal
import os
import errno
import relay_manipulation as rm
import multiprocessing as mp
import db_manipulation as dbm
import network_interface as net_if


class ClientManipulation():
    def __init__(self):
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def subprocess(self, func, data):
        '''
        fork a process
        '''

        proc = mp.Process(target = func, args = (data,))
        proc.start()
    
    def wait_child(self, signum, frame):
        '''
        join child processes
        '''

        try:
            while True:
                cpid, _ = os.waitpid(-1, os.WNOHANG)
                if cpid == 0:
                    break
        
        except OSError as e:
            if e.errno == errno.ECHILD:
                print('LOG: current process has no existing unwaited-for child processes.')
            else:
                raise

        print("LOG: handle SIGCHLD end")

    def open_udp_socket(self):
        '''
        open a udp socket for clients' connection info
        '''

        try:
            self.udp_sock.bind((net_if.get_server_ip(), 3478))
        except:
            print("ERROR: Can not open socket")
            exit()

        print("LOG: Socket opened")

        signal.signal(signal.SIGCHLD, self.wait_child)

        while True:
            data, addr = self.udp_sock.recvfrom(1024)
            data = data.decode("utf-8").split(" ")

            if data[0] == "allocate":
                relay_port = rm.RelayManipulation().open_socket()
                
                if not relay_port:
                    self.send_data(addr, "Fail")
                else:
                    self.subprocess(self.waiting_remote_allocation, (data[1], addr, relay_port, data[2]))

    def waiting_remote_allocation(self, data):
        '''
        waiting for remote client's allocation
        '''

        dbm.DBManipulation().set_client_data(data[0], data[1][0], data[2], data[3])

        while True:
            remote_data = dbm.DBManipulation().get_client_by_id(data[3])
            
            if remote_data:
                # send relay_port remote_port
                self.send_data(data[1], data[2] + " " + remote_data[2])
                break
            
            time.sleep(1)

    def send_data(self, addr, msg):
        '''
        send messages over the socket
        '''

        self.udp_sock.sendto(msg.encode("utf-8"), addr)
