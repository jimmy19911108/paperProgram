'''
stun module
'''

import stun
import network_interface as net_if


class Stun():
    '''
    stun
    '''

    def __init__(self):
        self.nat_type = ("Full Cone", # 0
         "Restrict NAT", # 1
         "Restrict Port NAT", # 2
         "Symmetric NAT", # 3
         "Unknown NAT") # 4

    def get_nat_type(self):
        '''
        get External NAT Type, IP and Port
        '''

        nat_type, external_ip, external_port = stun.get_ip_info(stun_host = net_if.get_stun_server())

        print("\n\n=======================")
        print("NAT Type:", nat_type)
        print("External IP:", external_ip)
        print("External Port:", external_port)
        print("=======================\n\n")

        return nat_type, external_ip, external_port

    def check_nat_type(self):
        '''
        make a decision for the corresponding NAT type
        '''

        nat_type, external_ip, external_port = self.get_nat_type()

        if nat_type == self.nat_type[0]:
            print("LOG: P2P mode")
            return external_ip + ":" + str(external_port), "fullcone"
        elif nat_type == self.nat_type[1]:
            print("LOG: P2P mode")
            return external_ip + ":" + str(external_port), "restrict"
        else:
            print("LOG: Relay mode") #controller
            return external_ip + ":" + str(external_port), "symmetric"
