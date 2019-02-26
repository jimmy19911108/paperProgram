'''
data module
'''

import user_manipulation as um


class DataManipulation():
    '''
    data manipulation
    '''

    def __init__(self):

        self.request_state = ("register", "bind", "replybind", "bindwaiting", "close")
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
            return self.users.bind_user(data[1], data[2], data[3])

        # replybind
        elif data[0] == self.request_state[2]:
            self.users.reply_bind()

        # bindwaiting
        elif data[0] == self.request_state[3]:
            self.users.waiting_for_being_binded()

        # close
        elif data[0] == self.request_state[4]:
            self.users.delete_user(data[1])
            return "ok"
