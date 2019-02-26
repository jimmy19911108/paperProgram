'''
network interface parameter
'''


def get_server_addr():
    '''
    return server ip
    '''

    return "192.168.1.42"

def get_upper_layer():
    '''
    return upper layer controller's address
    '''

    if get_server_layer():
        return None
    else:
        return "192.168.1.201"

def get_cloud_layer():
    '''
    return cloud layer controller's address
    '''

    if get_server_layer():
        return None
    else:
        return "192.168.1.201"

def get_server_layer():
    '''
    return server layer\n
    1 for cloud, 0 for others
    '''

    return 1
