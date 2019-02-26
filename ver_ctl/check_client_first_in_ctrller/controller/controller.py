#!/usr/bin/env python3.5

'''
controller
'''

import multiprocessing as mp
import connection_handler as ch
import sys


def sub_process(fnc, server_ip, port):
    '''
    fork a process
    '''

    proc = mp.Process(target = fnc, args = (server_ip, port))
    proc.start()

def main(server_ip, buttom, cloud):
    '''
    main function
    '''

    client_socket = ch.ConnectionHandler()
    sub_process(client_socket.socket_open, server_ip, 5000)

    turn_socket = ch.ConnectionHandler()
    sub_process(turn_socket.socket_open, server_ip, 5001)


if __name__ == "__main__":
    
    try:
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    except IndexError:
        print("ERROR: at least 2 argument are requered:")
        print("./client <server IP> <1 or 0> <1 or 0>")
        print("The 1st argument is for the IP address of this server.")
        print("The 2st argument is for the controller in the lowest layer.")
        print("The 3nd argument is for the controller in the cloud layer.")
        exit()
