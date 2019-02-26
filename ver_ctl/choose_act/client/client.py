#!/usr/bin/env python3.5

'''
client module
'''

import sys
import time
import multiprocessing as mp
import signal
import network_control as netc
import video
import stun_procedure


def subprocess(func, ip_addr):
    '''
    fork process
    '''

    proc = mp.Process(target = func, args = (ip_addr,))
    proc.start()

def user_name_check(local_id, remote_id):
    '''
    check if the remote id equal to the local id
    '''

    if local_id == remote_id:
        print("ERROR: same user name")
        return False
    return True

def insert_remote_user(local_id):
    '''
    insert remote user
    '''

    while True:
        remote_id = input("Input the remote user's ID: ")
        if user_name_check(local_id, remote_id):
            return remote_id

def choose_connection_act():
    '''
    select for active connection or passive connection
    '''

    while True:
        insert_data = input("\n1.Waiting for connecting\n2.Input remote user's ID to connect\n: ")
        if insert_data != "1" and insert_data != "2":
            print("ERROR: please input again: '1' or '2'")
        else:
            return insert_data

def main(local_id):
    '''
    main function
    '''

    # create socket and ICE object
    ice_process = stun_procedure.Stun()
    siganl_socket = signal.Signal(local_id)
    siganl_socket.socket_open()

    # connection procedure
    try:
        if siganl_socket.register():

            connection_act = choose_connection_act()
            # 1 for passive connection
            if connection_act == "1":
                # return "remote id" and "remote candidate" if local user permited to be binded
                remote_id, remote_candidate = siganl_socket.bind_waiting()
                # get reflex candidate with STUN server
                reflex_candidate = ice_process.check_nat_type()
                # reply bind
                siganl_socket.reply_bind_with_remote_user(remote_id, reflex_candidate)

            # 2 for active connection
            elif connection_act == "2":
                # local user inputs remote id
                remote_id = insert_remote_user(local_id)
                # get reflex candidate
                reflex_candidate = ice_process.check_nat_type()
                # bind with remote user
                remote_candidate = siganl_socket.bind_with_remote_user(remote_id, reflex_candidate)

            if remote_candidate and True:
                subprocess(video.stream, remote_candidate)
                subprocess(video.show_remote_cam, netc.get_local_ip())

            while True:
                time.sleep(2)
        else:
            exit()

    except KeyboardInterrupt:
        siganl_socket.socket_close()

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("ERROR: at least 1 argument are requered: ./client <local user's id>")
        exit()
