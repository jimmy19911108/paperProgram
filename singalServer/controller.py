'''
respond the IP address of the controller which is in the area as same as the user who sent the request
'''

from geolite2 import geolite2


class Controller():

    def __init__(self):
        self.controller_ip = {"TW":"192.168.1.62", "US":"192.168.1.63"}

    def get_controller_ip(self, user_area):
        '''
        return the coresponding area
        '''

        #return self.controller_ip[user_area]
        return self.controller_ip["TW"]