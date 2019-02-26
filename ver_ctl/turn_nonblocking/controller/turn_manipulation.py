'''
handle imformation of turn servers
'''

import turn_db_manipulation as tdbm


class TurnManipulation():
    
    def __init__(self):

        self.data_base = tdbm.TurnDB()

    def turn_loading(self, cpu, mem, disk, bandwidth, addr):
        '''
        calculate the loading of turn servers
        '''

        loading = float(cpu) * 0.25 + float(mem) * 0.25 + float(disk) * 0.25 + float(bandwidth) * 0.25

        turn_info = self.data_base.get_turn_info(addr[0])

        if turn_info != None:
            history = turn_info[2] * 0.5 + loading * 0.5
            print(history)
            self.data_base.update_turn_info(addr[0], loading, history)
        else:
            self.data_base.add_turn_info(addr[0], loading)

    def turn_disconnect(self, addr):
        '''
        delete turn server
        '''

        self.data_base.delete_turn_info(addr)
