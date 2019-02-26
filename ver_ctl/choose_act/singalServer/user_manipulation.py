'''
user module
'''

import db_manipulation as dbm


class UserManipulation():
    '''
    user manipulation
    '''

    def __init__(self):
        self.users = dbm.DBManipulation()

    def add_user(self, user_id, user_ip):
        '''
        add the user into the database
        '''

        self.users.set_registed_user(user_id, user_ip)
        print("LOG: %s from %s has been added" % (user_id, user_ip))

    def check_permission(self, user_id, user_ip):
        '''
        add the user if the user doesn't exist
        '''

        if self.users.exist_registed_user(user_id):
            return False
        else:
            self.add_user(user_id, user_ip)
            return True

    def bind_user(self, user_id, binded_id, candidate):
        '''
        bind users
        '''

        # check if the remote user has registed
        if self.users.exist_registed_user(binded_id):
            # check if the local user and the remote user has bound
            if not self.users.exist_bind_user(user_id) and not self.users.exist_bind_user(binded_id):
                # send request

                # wait for response

                # add bind imformation into the database if remote user comfirmed the request
                self.users.set_binded_user(user_id, binded_id)
                print("LOG: %s is bined with %s" % (user_id, binded_id))

                #return remote user's candidate
                return "ok"

        # the remote user doesn't exist in the database
        print("WARRING: fail to bind user %s with %s" % (user_id, binded_id))
        return "fail"

    def waiting_for_being_binded(self):
        '''
        waiting for being binded
        '''

    def reply_bind(self):
        '''
        reply bind
        '''
        pass

    def delete_user(self, user_id):
        '''
        delete user
        '''

        self.users.delete_user(user_id)
