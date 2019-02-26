#!/usr/bin/env python3.5

'''
TURN server
'''

import ctrller_manipulation
import db_manipulation
import client_manipulation


def main():
    '''
    main function
    '''
    
    db_manipulation.DBManipulation().flush_db()

    # send resource usage to controller
    if ctrller_manipulation.CtrllerManipulation().open_socket():

        # udp socket for client connect
        if not client_manipulation.ClientManipulation().open_udp_socket():
            print("ERROR: open UDP socket fail")


if __name__ == "__main__":
    main()
