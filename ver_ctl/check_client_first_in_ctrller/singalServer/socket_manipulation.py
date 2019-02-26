'''
socket module
'''

import socket
import multiprocessing as mp
import data_manipulation as dm


class SocketManipulation():
    '''
    socket manipulateion
    '''

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 180)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 3)
        self.data_process = dm.DataManipulation()

    def sub_process(self, func, conn, addr):
        '''
        fork a process
        '''

        proc = mp.Process(target = func, args = (conn, addr))
        proc.start()

    def socket_open(self, server_ip, server_port):
        '''
        open socket
        '''

        try:
            self.sock.bind((server_ip, int(server_port)))
        except TypeError:
            print("ERROR: Type error")
            exit()
        except ValueError:
            print("ERROR: Value error")
            exit()
        except:
            print("ERROR: Can not open socket")
            exit()

        print("LOG: Socket opened")
        
        while True:
            self.sock.listen(5)
            conn, addr = self.sock.accept()
            self.sub_process(self.data_receive, conn, addr)

    def socket_close(self):
        '''
        close socket
        '''

        self.sock.close()

    def conn_close(self, conn):
        '''
        close connection
        '''

        print("LOG: close client's connection")
        conn.close()

    def send_data(self, conn, data):
        '''
        send data
        '''

        conn.send(data.encode("utf-8"))

    def data_receive(self, conn, addr):
        '''
        receive data and close socket after jobs done
        '''

        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                # check if client diconnected
                if not data:
                    self.conn_close(conn)
                    break

                msg = self.data_process.data_handler(addr, data.split(" "))
                self.send_data(conn, msg)

            except:
                print("WARNING: Can not receive data from client %s" % str(addr))