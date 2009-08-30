from Parser import *

import Session
import httplib
import re
import json


class Token:
    Standard    = None
    Login       = 0
    Action      = 1

class RetCodes:
    NoError     = 0
    Error       = 1

class UserAPITypes:
    Standard            = None
    Outbox              = "outbox"
    Inbox               = "inbox"
    MutualFriends       = "mutual"
    OnlineFirends       = "online"
    NewFriends          = "new"
    NewPhotos           = "new"
    MyPhotos            = "with"
  

class UserAPI:
    def __init__(self, session):
        self.session = session
        self.id      = 0
        
    def v_api(self, action, parameters):
        # self.renew_session()

        GET  = "/data?act=" + action + "&sid=" + self.session.get_sid()
        
        for key,val in parameters.iteritems():
            if val != None:
                GET = GET + "&" + str(key) + "=" + str(val)

        connection = httplib.HTTPConnection("userapi.com")
       
        connection.request('GET', GET, None, {"Cookie" : "remixpassword=" + self.session.remixpass})
        response = connection.getresponse()
        data     = response.read()
        connection.close()

        if response.status != 200:
            raise UserAPIError(0, action, "Couldn't connect")

        data = re.sub("([0-9]+):", "\"\\1\":", data)
        data = re.sub("\\t", " ", data)

        return json.loads(data, "utf-8")


    def v_friends(self, subtype, id, start, end):

        action = "friends"
        if subtype:
            action = action + "_" + subtype 
        
        data = self.v_api(action, { "from" : start,
                                    "to"   : end   ,
                                    "id"   : id    })


        friends = []
        
        for person in data:
            friends.append(Parser(person).as_person(Parser.FRI_PERSON))

        return friends

    def v_messages(self, subtype, id, start, end, ts = None):
        action = "message"
        if subtype:
            action = subtype

        data = self.v_api(action, { "from" : start,
                                    "to"   : end,
                                    "id"   : id,
                                    "ts"   : ts})

        return Parser(data).as_messages()

    def v_photos(self, subtype, id, start, end):
        action = "photos"
        if subtype:
            action = action + "_" + subtype

        data = self.v_api(action, { "from" : start,
                                    "to"   : end,
                                    "id"   : id})
        
        return Parser(data).as_photos()

    def v_profile(self, id = None):
        action = "profile"
        
        data = self.v_api(action, { "id"   : id})
        return Parser(data).as_person(PRO_PERSON)

    def get_own_id(self):
        if self.id == 0:
            data = self.v_api('profile', { "id" : None })
            self.id = data['us']
        
        return self.id


    def build_conversations(self, inbox, outbox):
        conversations = {}
        for message in inbox + outbox:
            person = message.mfrom if message.mfrom.id != self.get_own_id() else message.mto
            try:
                conversation = conversations[person.id]
            except:
                conversation = Conversation(person, [])
                conversations[person.id] = conversation
            conversation.messages.append(message)
        return conversations.values()


