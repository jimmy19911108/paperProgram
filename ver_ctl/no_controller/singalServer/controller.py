'''
respond the IP address of the controller which is in the area as same as the user who sent the request
'''

from geolite2 import geolite2


class Controller():

    controller_ip = {"TW":"192.168.1.62", "US":"192.168.1.63"}

    def check_users_area(self, user_ip):
        '''
        check user's area through the IP address
        '''

        reader = geolite2.reader()
        reader.get(user_ip)

        iso_code = reader['country']['iso_code']

        reader.close()

        return iso_code


    def get_controller_ip(self, user_area):
        '''
        return the coresponding area
        '''

        return self.controller_ip[user_area]