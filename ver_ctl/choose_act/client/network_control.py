'''
network control module
'''

def get_local_ip():
    '''
    return local ip
    '''

    return "192.168.1.42:8000"

def get_stun_server():
    '''
    return stun server ip
    '''

    return "192.168.1.98"

def get_signalling_server():
    '''
    return the ip and the port of signalling server
    '''

    return "127.0.0.1", 5000
