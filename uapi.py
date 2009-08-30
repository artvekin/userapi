# -*- coding: utf-8 -*- 

from userapi import *

USER = "test.vkontakte@mail.ru"
PASS = "yi8zXpHIs"
DID="41657126"

def test_01():
    print "Own ID: " + str(test.get_own_id())

def test_02():
    Friends = test.v_friends(UserAPITypes.OnlineFirends, test.get_own_id(), 0, 100)
    for friend in Friends:
        print friend.name + "\t<" + str(friend.id) + ">"

def test_03():
    print test.v_friends(None, DID, 1, 100)
    print test.v_friends(UserAPITypes.OnlineFirends, DID, 1, 100)

def test_04():
    inbox = test.v_messages(UserAPITypes.Inbox, None, 0, 100)
    outbox = test.v_messages(UserAPITypes.Outbox, None, 0, 100)
    conversations = test.build_conversations(inbox.messages, outbox.messages)
    for conversation in conversations:
        print "conversation: " + conversation.mwith.name
        for message in conversation.messages:
            print  "\t<" + message.text + ">"

def test_05():
    wall = test.v_wall(test.get_own_id(), 0, 100)
    for message in wall.messages:
        print message.mfrom.name + "\t<" + message.text + ">" + "\t == " + (message.original_url or "--")


tests = [test_01, test_04, test_05]

try:
    session = Session()
    session.login(USER, PASS)
    
    test = UserAPI(session)

    for testcase in tests:
        print "---------------------------"
        testcase()

    session.logout()

except UserAPIError as error:
    print "Get code: " + str(error.code) + " " + error.text

