from Parser import *
from Errors import *

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
  

def fix_unicode(val, encoding = 'utf-8', exclude = []):
    if isinstance(val, unicode):
        tmp = val.encode('latin-1')
        return unicode(tmp, encoding)
    elif isinstance(val, dict):
        result = {}
        for key in val:
            if key not in exclude:
                result[key] = fix_unicode(val[key], encoding)
            else:
                result[key] = val[key]
        return result
    elif isinstance(val, list):
        result = list(val)
        for i in range(0, len(result)):
            if i not in exclude:
                result[i] = fix_unicode(result[i], encoding)
        return result
    else:
        return val


class UserAPI:
    def __init__(self, session):
        self.session = session
        self.id      = 0
        
    def fix_json(self, data):
        res = ""
        state = ""
        number = ""
        for s in data:
            if state == "":
                if s == "\"":
                    res = res + s
                    state = "\""
                elif s.isdigit():
                    number = s
                    state = "n"
                else:
                    res = res + s
            elif state == "\"":
                if s == "\"":
                    res = res + s
                    state = ""
                else:
                    res = res + s
            elif state == "n":
                if s == ":":
                    res = res + "\"" + number + "\":"
                    state = ""
                elif s.isdigit():
                    number = number + s
                else:
                    res = res + number + s
                    state = ""
        return res

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

        data = self.fix_json(data)
        data = re.sub("\\t|\\x13", " ", data)

        contenttype = response.getheader('Content-Type')
        m = re.search("charset=(?P<charset>.*)", contenttype)
        charset = m.group('charset').lower()
        if charset == 'utf-8':
            encoding = 'utf-8'
        else:
            encoding = 'latin-1'
	
        try:
            return json.loads(data, encoding), charset
        except StandardError as error:
            raise JSONProblemError(data,
                                   { "error"    : error, 
                                     "encoding" : encoding})
            

    def v_friends(self, subtype, id, start, end):

        action = "friends"
        if subtype:
            action = action + "_" + subtype 
        
        data, charset = self.v_api(action, { "from" : start,
                                             "to"   : end,
                                             "id"   : id})
        if charset != 'utf-8':
            data = fix_unicode(data, 'cp1251')

        friends = []
        
        for person in data:
            friends.append(Parser(person).as_person(FRI_PERSON))

        return friends

    def v_messages(self, subtype, id, start, end, ts = None):
        action = "message"
        if subtype:
            action = subtype

        data, charset = self.v_api(action, { "from" : start,
                                             "to"   : end,
                                             "id"   : id,
                                             "ts"   : ts})
        if charset != 'utf-8':
            data = fix_unicode(data)
        return Parser(data).as_messages()


    def v_wall(self, id, start, end, ts = None):
        action = "wall"

        data, charset = self.v_api(action, { "from" : start,
                                             "to"   : end,
                                             "id"   : id,
                                             "ts"   : ts})
        if charset != 'utf-8':
            data = fix_unicode(data)
        return Parser(data).as_messages()


    def v_photos(self, subtype, id, start, end):
        action = "photos"
        if subtype:
            action = action + "_" + subtype

        data, charset = self.v_api(action, { "from" : start,
                                             "to"   : end,
                                             "id"   : id})
        
        return Parser(data).as_photos()

    def v_profile(self, id = None):
        action = "profile"
        
        data, charset = self.v_api(action, { "id"   : id})
        if charset != 'utf-8':
            broken_keys = ['fr', 'fro', 'frm']
            for key in broken_keys:
                data[key] = fix_unicode(data[key], 'cp1251')
            data = fix_unicode(data, exclude = broken_keys)

        return Parser(data).as_person(PRO_PERSON)

    def get_own_id(self):
        if self.id == 0:
            data, charset = self.v_api('profile', { "id" : None })
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


