'''
network control module
'''

import socket


def get_local_ip():
    '''
    return local ip
    '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    net_ip, _ = sock.getsockname()
    sock.close()

    return net_ip + ":54320"

def get_stun_server():
    '''
    return stun server ip
    '''

    return "192.168.1.98"

def get_signalling_server():
    '''
    return the ip and the port of signalling server
    '''

    return "192.168.1.42", 5000
