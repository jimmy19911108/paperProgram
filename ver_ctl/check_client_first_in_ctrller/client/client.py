#!/usr/bin/env python3.5

'''
client module
'''

import sys
import multiprocessing as mp
import signal
import network_interface as net_if
import video
import stun_procedure
import controller
import turn_procedure


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
    stun = stun_procedure.Stun()
    siganl_socket = signal.Signal(local_id)
    siganl_socket.socket_open()

    # connection procedure
    try:
        if siganl_socket.register():
            
            # local user inputs remote id
            remote_id = insert_remote_user(local_id)
            # get reflex candidate
            reflex_candidate, nat_type = stun.check_nat_type()
            # bind with remote user
            remote_candidate, remote_nat_type = siganl_socket.bind_with_remote_user(remote_id, reflex_candidate, nat_type)

            # if both client are behind the fullcone NAT
            # start stream and delete IDs on the signaling server
            if (nat_type == "fullcone" or nat_type == "restrict") and (
                remote_nat_type == "fullcone" or remote_nat_type == "restrict"):
                
                subprocess(video.stream, remote_candidate)
                subprocess(video.show_remote_cam, net_if.get_local_ip())
                
                siganl_socket.socket_close(1)
                
                print("close siganl")
            else:
                # get local and remote area
                local_area = net_if.get_area(reflex_candidate)
                remote_area = net_if.get_area(remote_candidate)
                
                # create a controller object and set the local controller ip
                ctrller = controller.Controller(
                    siganl_socket.request_controller_ip(local_area))

                while True:
                    if ctrller.socket_open():
                        # request to controller to get the turn server ip
                        msg = ctrller.request_turn(local_id, remote_id, remote_area)
                        
                        # if the controller return the ip of another controller
                        # update controller ip and send request again
                        if msg[0] == "ctrl":
                            ctrller.set_ctrller_addr(msg[1])
                            continue
                        
                        # if the controller return the ip of a turn server
                        # send allocate request to turn server to allocate a port
                        else:
                            turn = turn_procedure.TurnProcedure(msg[1])
                            relay_port = turn.start(local_id, remote_id)
                            
                            # if turn is available, start stream to turn
                            if relay_port:
                                subprocess(video.stream, relay_port)
                                subprocess(video.show_remote_cam, net_if.get_local_ip())
                            else:
                                print("LOG: Fail to Connect")
                        
                        ctrller.socket_close()

            #siganl_socket.socket_close(0)

            siganl_socket.socket_close(1)
            print("close siganl")
        else:
            exit()

    except KeyboardInterrupt:
        siganl_socket.socket_close(1)

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("ERROR: at least 1 argument are requered: ./client <local user's id>")
        exit()
