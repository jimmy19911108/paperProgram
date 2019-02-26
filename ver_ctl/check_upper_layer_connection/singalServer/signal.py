#!/usr/bin/env python3.5

'''
main module
'''

import sys
import socket_manipulation as sm
import db_manipulation as dbm


def main(server_ip, server_port):
    '''
    main function
    '''

    dbm.DBManipulation().flush_db()
    server_socket = sm.SocketManipulation()
    server_socket.socket_open(server_ip, server_port)

if __name__ == "__main__":
    
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        print("ERROR: 2 pareameters are requered : ./signal <server ip> <server port>")
