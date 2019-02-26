#!/usr/bin/env python3.5

'''
client module
'''

import sys
import multiprocessing as mp
import signal
import network_control as netc
import video
import stun_procedure
import controller


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
            # local user inputs remote id
            remote_id = insert_remote_user(local_id)
            # get reflex candidate
            reflex_candidate, nat_type = ice_process.check_nat_type()
            # bind with remote user
            remote_candidate, remote_nat_type = siganl_socket.bind_with_remote_user(remote_id, reflex_candidate, nat_type)

            if nat_type == "fullcone" and remote_nat_type == "fullcone":
                subprocess(video.stream, remote_candidate)
                subprocess(video.show_remote_cam, netc.get_local_ip())
                siganl_socket.socket_close()
                print("close siganl")
            else:
                ctl_ip = siganl_socket.request_controller_ip(reflex_candidate)
                ctl = controller.Controller(ctl_ip)
                ctl.socket_open()

            siganl_socket.socket_close()
            print("close siganl")
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
