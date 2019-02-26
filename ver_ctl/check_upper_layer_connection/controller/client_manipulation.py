'''
client manipulation
'''

class ClientManipulation():
    
    def __init__(self):
        self.relay_area = {"TW"}

    def check_client_area(self, area):
        '''
        check if the client and controller is in the same area
        '''

        if area in self.relay_area:
            return True
        
        return False

    def find_turn(self):
        pass
