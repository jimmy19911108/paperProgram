#!/usr/bin/env python3.5

'''
controller
'''

import multiprocessing as mp
import connection_manipulation as cm


def main():
    '''
    main function
    '''

    turn_socket = cm.ConnectionHandler()
    proc = mp.Process(target = turn_socket.socket_open, args = (5001,))
    proc.start()

    client_socket = cm.ConnectionHandler()
    client_socket.socket_open(5000)

if __name__ == "__main__":
    main()
