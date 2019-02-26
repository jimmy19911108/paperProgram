'''
data module
'''

import user_manipulation as um
import controller


class DataManipulation():
    '''
    data manipulation
    '''

    def __init__(self):

        self.request_state = ("register", "bind", "requestCIP", "close")
        self.users = um.UserManipulation()

    def data_handler(self, addr, data):
        '''
        data handler
        '''

        # register
        if data[0] == self.request_state[0]:
            if self.users.check_permission(data[1], str(addr)):
                return "ok " + addr[0] + " " + str(addr[1])
            else:
                return "fail"
        # bind
        elif data[0] == self.request_state[1]:
            return self.users.bind_user(data[1], data[2], data[3], data[4])

        #request controller's IP
        elif data[0] == self.request_state[2]:
            ctl = controller.Controller()
            return ctl.get_controller_ip(ctl.check_users_area(data[1]))

        # close
        elif data[0] == self.request_state[3]:
            self.users.delete_user(data[1])
            return "ok"
