'''
connection module
'''

import socket
import multiprocessing as mp
import data_manipulation as dm
import network_interface as net_if
import client_db_manipulation as cdbm


class ConnectionHandler():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 180)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 3)
        self.data_process = dm.DataManipulation()

    def sub_process(self, func, conn, addr):
        '''
        fork process
        '''

        proc = mp.Process(target = func, args = (conn, addr))
        proc.start()

    def socket_open(self, server_port):
        '''
        open socket
        '''

        try:
            self.sock.bind((net_if.get_server_addr(), int(server_port)))
        except:
            print("ERROR: Can not open socket")
            exit()

        print("LOG: Socket opened")
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            self.sub_process(self.data_receive, conn, addr)

    def send_data(self, conn, data):
        '''
        send data
        '''

        conn.send(data.encode("utf-8"))

    def conn_close(self, conn):
        '''
        close connection
        '''

        print("LOG: Client disconnect")
        conn.close()

    def data_receive(self, conn, addr):
        '''
        receive data and close socket after jobs done
        '''

        while True:
            
            data = conn.recv(1024).decode("utf-8")
                
            # check if client diconnected
            if not data:
                self.conn_close(conn)
                break

            msg = self.data_process.data_handler(addr, data.split(" "))
            if msg:
                self.send_data(conn, msg)
