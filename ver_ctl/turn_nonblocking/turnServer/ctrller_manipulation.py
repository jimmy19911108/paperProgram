'''
a handler for connections of the controller
'''

import socket
import time
import resource_monitor
import db_manipulation
import multiprocessing as mp
import network_interface as net_if


class CtrllerManipulation():

    def __init__(self):
        self.res_usage = resource_monitor.RsourceMonitor()
        self.database = db_manipulation.DBManipulation()

    def open_socket(self):
        '''
        open a socket for controller
        '''

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("ERROR: Fail to open socket")
            return False

        try:
            self.sock.connect((net_if.get_ctrller_ip(), 5001))
        except:
            print("ERROR: Fail to connect to controller")
            return False

        proc = mp.Process(target = self.socket_io)
        proc.start()

        return True

    def send_data(self, msg):
        '''
        send data through socket
        '''

        self.sock.send(msg.encode("utf-8"))

    def close_socket(self):
        '''
        close socket
        '''

        self.send_data("turn_diconnect")

        self.sock.close()

    def get_sleep_time(self):
        '''
        if client reset sleep time, return client's time\n
        else return current time
        '''

        new_time = self.database.get_time()

        if new_time:
            return new_time
        else:
            return time.time()

    def socket_io(self):
        '''
        send resourse usage to controller
        '''

        old_time = 0

        try:
            while True:
                sleep_time = time.time()-old_time
                if sleep_time >= 300:
                    all_usage = self.res_usage.get_all_info()
                    self.send_data(
                        "turn " + str(all_usage[0]) + " " + str(all_usage[1]) + " " + str(all_usage[2]) + " "+ str(all_usage[3]))
                    old_time = self.get_sleep_time()
                else:
                    time.sleep(300-sleep_time)
        except KeyboardInterrupt:
            self.close_socket()
