import json
import datetime

from Message import *
from Person  import *
from Photo   import *

MSG_PERSON = 0
FRI_PERSON = 1
PRO_PERSON = 2

def listify(data, size):
    result = [None for i in range(0, size)]
    if isinstance(data, list):
        for i in range(0, len(data)):
            result[i] = data[i]
    elif isinstance(data, dict):
        for i in data:
            result[int(i)] = data[i]
    return result


def convert(val, type, default = None):
    if val is not None:
        return type(val)
    return default


class Parser:
    def __init__ (self, data):
        self.data = data

    def as_message(self):
        self.data = listify(self.data, 6)
        self.data[2] = listify(self.data[2], 8)

        return Message(int(self.data[0]),
                       int(self.data[1]),
                       self.data[2][0],
                       Parser(self.data[3]).as_person(MSG_PERSON),
                       Parser(self.data[4]).as_person(MSG_PERSON),
                       convert(self.data[5], bool, False),
                       convert(self.data[2][1], int, Message.TEXT),
                       self.data[2][2],
                       self.data[2][3],
                       self.data[2][4],
                       convert(self.data[2][5], int),
                       convert(self.data[2][6], int),
                       convert(self.data[2][7], int))
        
    def as_messages(self):
        messages = []

        for message_data in self.data['d']:
            messages.append(Parser(message_data).as_message())
    
        return Messages(int(self.data['n']),
                        int(self.data['h']),
                        len(self.data['d']),
                        messages)

    def as_person(self, parse_type):
        if     parse_type == MSG_PERSON:
            
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

        elif    parse_type == FRI_PERSON:

            self.data = listify(self.data, 4)

            id         = self.data[0]
            name       = None 
            avatar     = None 
            isOnline   = None 
            
            if len(self.data) > 1:
                name       = self.data[1]
                avatar     = self.data[2]
                isOnline   = self.data[3]

            return Person(id, name, avatar, isOnline)

        elif    parse_type == PRO_PERSON:
            prof = PersonsProfile()
            
            id         = self.data['id']
            name       = self.data['fn'] + ' ' + self.data['ln']
            sex        = self.data['sx']
            avatar     = self.data['bp']
            
            prof.mother     = self.data['mn']
            prof.status     = self.data['actv'] #TODO: Parse it
            prof.position   = Parser(self.data['ht']).as_position()
            prof.birthday   = datetime.date(self.data['by'], self.data['bm'], self.data['bd'])
            prof.state      = MaritalStatus(self.data['fs'])
            prof.politics   = PoliticView(self.data['pv'])

            prof.friends = Parser(self.data['fr']).as_persons(FRI_PERSON)
            prof.friends_online = Parser(self.data['fro']).as_persons(FRI_PERSON)
            prof.shared_friends = Parser(self.data['frm']).as_persons(FRI_PERSON)

            prof.own_photos = Parser(self.data['ph']).as_photos()
            prof.mark_photos = Parser(self.data['phw']).as_photos()
            # TODO: Fix it ?
            # prof.privacy     = Parser(self.data['pr']).as_privacy()
            
            prof.wall = None # TODO
            prof.online = self.data['on']
            
            prof.requester_id = self.data['us']
            prof.is_requester_friend = self.data['isf']
            prof.is_requester_invited = self.data['isi']
            prof.is_requester_favour  = self.data['f']
            
            prof.education_list = self.data['edu'] #TODO: Parse it


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

    def as_photo(self):
        self.data = listify(self.data, 3)
        return Photo(self.data[0],
                     self.data[2],
                     self.data[1])

    def as_uploadinfo(self):
        return PhotosUploadInfo(self.data['aid'],
                                self.data['url'],
                                self.data['hash'],
                                self.data['rhash'])
        
    def as_photos(self):
        photos = []

        for photo in self.data['d']:
            photos.append(Parser(photo).as_photo())

        if (len(self.data) > 2):
            upload_info = self.as_uploadinfo()
            ts = self.data['ts']
        else:
            upload_info = None
            ts = None

        return Photos(self.data['n'],
                      photos,
                      ts,
                      upload_info)

    def as_privacy(self):
        print self.a
        return Privacy(self.data['pa'],
                       self.data['wa'],
                       self.data['ms'])

