'''
data base module
'''

import sqlite3
import time
import redis


class DBManipulation():
    '''
    data base manipulation
    '''

    def __init__(self):

        self.registed_user = redis.StrictRedis(host='localhost', port=6379)
        self.binded_user = redis.StrictRedis(host='localhost', port=6380)
        self.user_candidate_conn = sqlite3.connect('user_candidate.db')
        self.user_candidate_curs = self.user_candidate_conn.cursor()
        self.user_candidate_curs.execute('''CREATE TABLE IF NOT EXISTS user_cnadidate
        (user_id VARCHAR(20) PRIMARY KEY,
         candidate VARCHAR(20)), 
         remote_user_id VARCHAR(20)''')

    def set_user_candidate_to_db(self, user_id, candidate, remote_id):
        '''
        set user's candidate to database
        '''

        ins = 'INSERT INTO user_candidate (user_id, candidate, remote_user_id) VALUES(?, ?, ?)'

        self.user_candidate_curs.execute(ins, (user_id, candidate, remote_id))
        self.user_candidate_conn.commit()

    def get_user_candidate_from_db(self, user_id):
        '''
        get user's candidate from database
        '''

        self.user_candidate_curs.execute(
            '''SELECT * from user_candidate where user_id = ?''', (user_id,))
        return self.user_candidate_curs.fetchone()

    def delete_user_from_sq_db(self, user_id):
        '''
        delete user from sqlite database
        '''

        self.user_candidate_curs.execute(
            '''DELETE FROM user_candidate where user_id = ?''', (user_id,))
        self.user_candidate_conn.commit()

    def close_sqlite3(self):
        '''
        close sqlite3
        '''

        self.user_candidate_curs.close()
        self.user_candidate_conn.close()

    def set_registed_user(self, user_id, addr):
        '''
        set registed user into redis server
        '''

        self.registed_user.set(user_id, addr)

    def set_binded_user(self, local_user, remote_user):
        '''
        set binded users into redis server
        '''

        self.binded_user.set(local_user, remote_user)

    def get_registed_user(self, user_id):
        '''
        get registed user's candidate from redis server
        '''

        got_data = self.registed_user.get(user_id)
        if got_data != None:
            return got_data.decode("utf-8")
        return got_data

    def exist_registed_user(self, user_id):
        '''
        check if the user's id exists in the database
        '''

        return self.registed_user.exists(user_id)

    def exist_bind_user(self, user_id):
        '''
        check if userid have been binded or have bind the other
        '''

        return self.binded_user.exists(user_id)

    def get_binded_user(self, user_id):
        '''
        get binded user
        '''

        return self.binded_user.get(user_id).decode("utf-8")

    def flush_db(self):
        '''
        flush all of databases
        '''

        self.registed_user.flushall()
        self.binded_user.flushall()

    def delete_user(self, user_id):
        '''
        delete a user
        '''

        if self.registed_user.delete(user_id):
            print("Log: Deleted %s from DB" % user_id)
