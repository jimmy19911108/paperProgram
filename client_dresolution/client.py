#!/usr/bin/env python3.5

'''
client module
'''

import sys
import time
import multiprocessing as mp
import signaling
import signal
import network_interface as net_if
import video
import stun_procedure
import controller
import turn_procedure


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
    siganl_socket = signaling.Signal(local_id)
    siganl_socket.socket_open()
    local_ip = net_if.get_local_ip()

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

                print("LOG: P2P")
                
                #subprocess(video.stream, remote_candidate)
                send_proc = mp.Process(target = video.stream, args = (remote_candidate))
                send_proc.start()
                #subprocess(video.show_remote_cam, local_ip + ":54320")
                recv_proc = mp.Process(target = video.show_remote_cam, args = (local_ip + ":54320"))
                recv_proc.start()

                siganl_socket.socket_close(1)
                
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
                        data = ctrller.request_turn(local_id, remote_id, remote_area)
                        
                        # if the controller return the ip of another controller
                        # update controller ip and send request again
                        if data[0] == "ctrl":
                            ctrller.set_ctrller_addr(data[1])

                        elif data[0] == "fail":
                            print("LOG: Fail to connect")
                            break
                        
                        # if the controller return the ip of a turn server
                        # send allocate request to turn server to allocate a port
                        else:
                            turn_ip = data[0]
                            resolution = data[1]

                            #print("LOG: create turn object with " + data[0])
                            turn = turn_procedure.TurnProcedure(turn_ip)
                            #print("LOG: turn procedure start")
                            relay_port, local_port = turn.start(local_id, remote_id)
                            #print("LOG: get relay port %s" % relay_port)
                            #print("LOG: get server addr %s" % str(server_addr))
                            
                            # if turn is available, start stream to turn
                            if relay_port:
                                #print("LOG: stream start, have not complete")
                                recv_proc = mp.Process(target = video.show_remote_cam, args = (local_ip + ":" + str(local_port)))
                                recv_proc.start()
                                #subprocess(video.show_remote_cam, local_ip + ":" + str(local_port))
                                while True:
                                    send_proc = mp.Process(target = video.stream, args = (turn_ip + ":" + relay_port, None, None, int(resolution)))
                                    send_proc.start()
                                    #subprocess(video.stream, data[0] + ":" + relay_port)
                                    resolution = ctrller.monitor_resolution(local_id)
                                    send_proc.terminate()

                                    while send_proc.exitcode != -signal.SIGTERM:
                                        time.sleep(0.1)

                            else:
                                print("LOG: Fail to Connect")
                            
                            break
                        
                ctrller.socket_close(local_id)

            #siganl_socket.socket_close(0)
            siganl_socket.socket_close(1)
        else:
            exit()

    except KeyboardInterrupt:
        ctrller.socket_close(local_id)
        siganl_socket.socket_close(1)

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("ERROR: at least 1 argument are requered: ./client <local user's id>")
        exit()
