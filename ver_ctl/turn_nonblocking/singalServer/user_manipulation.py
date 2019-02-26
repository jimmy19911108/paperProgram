'''
user module
'''

import time
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

    def bind_user(self, user_id, candidate, binded_id, nat_type):
        '''
        bind users
        '''

        # check if the remote user has registed
        if self.users.exist_registed_user(binded_id):
            # add the user to the database
            self.users.set_user_candidate(user_id, candidate, binded_id, nat_type, 0)

            # find the remote user's candidate from the database
            start_timer = time.time()
            while True:
                remote_user_info = self.users.get_user_candidate(binded_id)

                if remote_user_info != None and remote_user_info[2] == user_id:
                    break

                time.sleep(1)

                # 3 minutes time out
                now_timer = time.time()
                if now_timer - start_timer >= 180:
                    return "fail"

            # set the user's state as binding
            self.users.update_user_bind_state(user_id, 1)
            print("LOG: %s is binding with %s" % (user_id, binded_id))

            # check the remote user's state,
            # and delete both users if the state is binding
            while remote_user_info[3] == 0:
                remote_user_info = self.users.get_user_candidate(binded_id)
                time.sleep(1)
            self.users.delete_user_from_sq_db(binded_id)

            #return remote user's candidate and NAT type
            print("LOG: remote user's candidate" + remote_user_info[1])
            return "ok " + remote_user_info[1] + " " + remote_user_info[3]

        # the remote user doesn't exist in the database
        print("WARRING: fail to bind user %s with %s" % (user_id, binded_id))
        return "fail"

    def delete_user(self, user_id):
        '''
        delete user
        '''

        self.users.delete_user(user_id)
