from Message import *
from Person  import *
import json

MSG_PERSON = 0
FRI_PERSON = 1
PRO_PERSON = 2




class Parser:
    def __init__ (self, data):
        self.data = data

    def as_message(self):
            return Message(int(self.data['0']),
                           int(self.data['1']),
                           str(self.data['2']),
                           Parser(self.data['3']).as_person(MSG_PERSON),
                           Parser(self.data['4']).as_person(MSG_PERSON),
                           bool(self.data['5']))
        
    def as_messages(self):
        messages = []

        for message_data in self.data['d']:
            messages.append(Parser(message_data).as_message())
    
        return Messages(int(self.data['n']),
                        int(self.data['h']),
                        len(self.data['d']),
                        messages)

    def as_person(self, type):
        if      type == MSG_PERSON:
            id         = self.data[0]
            name       = None 
            avatar     = None 
            miniimg    = None 
            sex        = None 
            isOnline   = None 
            
            if len(self.data) > 1:
                name       = self.data[1]
                avatar     = self.data[2]
                miniimg    = self.data[3]
                sex        = self.data[4]
                isOnline   = self.data[5]

            return Person(id, name, avatar, isOnline, miniimg, sex)

        elif    type == FRI_PERSON:
            id         = self.data[0]
            name       = None 
            avatar     = None 
            isOnline   = None 
            
            if len(self.data) > 1:
                name       = self.data[1]
                avatar     = self.data[2]
                isOnline   = self.data[3]

            return Person(id, name, avatar, isOnline)

        elif    type == PRO_PERSON:
            prof = PersonsProfile()
            
            id         = self.data['id']
            name       = self.data['fn'] + ' ' + self.data['ln']
            sex        = self.data['sx']
            avatar     = self.data['bp']
            
            prof.mother     = self.data['mn']
            prof.status     = self.data['actv']
            prof.position   = self.data['ht']
            prof.birthday   = datetime(self.data['by'], self.data['bm'], self.data['bd'])
            prof.state      = self.data['fs'] # Add parse here
            prof.politics   = self.data['pv'] # Add politics here

            prof.friends    = []

            for friend in self.data['fr']:
                prof.friends.append(Parser(friend).as_person(FRI_PERSON))

            self.on_friends = []

            for friend in self.data['fo']:
                prof.on_friends.append(Parser(friend).as_person(FRI_PERSON))

            prof.shared_friends = []

            for friend in self.data['frm']:
                prof.on_friends.append(Parser(friend).as_person(FRI_PERSON))


            return Person(id, name, avatar, None,
                          None, sex,
                          prof)


    def as_persons(self, person_type):
        persons    = []
        
        for person in self.data['d']:
            persons.append(Parser(person).as_person(person_type))

        return Persons(int(self.data['n']),
                       len(self.data['d']),
                       persons)

    def as_position(self):
        return Position(self.data['coi'],
                        self.data['con'],
                        self.data['cii'],
                        self.data['cin'])






