'''
data base module
'''

import sqlite3
import redis


class DBManipulation():
    '''
    data base manipulation
    '''

    def __init__(self):

        self.registed_user = redis.StrictRedis(host = 'localhost', port = 6379)
        self.user_candidate_conn = sqlite3.connect('user_candidate.db')
        self.user_candidate_curs = self.user_candidate_conn.cursor()
        self.user_candidate_curs.execute('''CREATE TABLE IF NOT EXISTS user_candidate
        (user_id VARCHAR(20) PRIMARY KEY,
         candidate VARCHAR(20), 
         remote_user_id VARCHAR(20),
         nat_type VARCHAR(20),
         bind_state BOOLEAN)''')

    def set_user_candidate(self, user_id, candidate, remote_id, nat_type, state = 0):
        '''
        =sqlite3= set user's candidate to database
        '''

        ins = 'INSERT INTO user_candidate\
         (user_id, candidate, remote_user_id, nat_type, bind_state) VALUES(?, ?, ?, ?, ?)'

        self.user_candidate_curs.execute(ins, (user_id, candidate, remote_id, nat_type, state))
        self.user_candidate_conn.commit()

    def update_user_bind_state(self, user_id, state):
        '''
        =sqlite3= update user's state for binding
        '''

        ins = 'UPDATE user_candidate SET bind_state = ? WHERE user_id = ?'

        self.user_candidate_curs.execute(ins, (state, user_id,))
        self.user_candidate_conn.commit()

    def get_user_candidate(self, user_id):
        '''
        =sqlite3=\n
        get user's candidate from database\n
        user id, candidate, remote user id, nat type, bind state
        '''

        self.user_candidate_curs.execute(
            '''SELECT * from user_candidate where user_id = ?''', (user_id,))
        return self.user_candidate_curs.fetchone()

    def delete_user_from_sq_db(self, user_id):
        '''
        =sqlite3= delete user from sqlite database
        '''

        self.user_candidate_curs.execute(
            '''DELETE FROM user_candidate where user_id = ?''', (user_id,))
        self.user_candidate_conn.commit()

    def close_sqlite3(self):
        '''
        =sqlite3= close sqlite3
        '''

        self.user_candidate_curs.close()
        self.user_candidate_conn.close()

    def set_registed_user(self, user_id, addr):
        '''
        =Redis= set registed user into redis server
        '''

        self.registed_user.set(user_id, addr)

    def get_registed_user(self, user_id):
        '''
        =Redis= get registed user's candidate from redis server
        '''

        data = self.registed_user.get(user_id)
        if data != None:
            return data.decode("utf-8")
        return data

    def exist_registed_user(self, user_id):
        '''
        =Redis= check if the user's id exists in the database
        '''

        return self.registed_user.exists(user_id)

    def flush_db(self):
        '''
        =Redis= flush redis databases
        '''

        self.registed_user.flushall()

    def delete_user(self, user_id):
        '''
        =Redis= delete a user
        '''

        if self.registed_user.delete(user_id):
            print("LOG: Deleted %s from DB" % user_id)
