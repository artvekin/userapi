# -*- coding: utf-8 -*- 

from userapi import *

USER = "test.vkontakte@mail.ru"
PASS = "yi8zXpHIs"
DID="11784322"
DID2="5368780"

def test_01():
    print "Own ID: " + str(test.get_own_id())

def test_02():
    Friends = test.v_friends(UserAPITypes.OnlineFirends, test.get_own_id(), 0, 100)
    for friend in Friends:
        print friend.name + "\t<" + str(friend.id) + ">"

def test_03():
    print test.v_friends(None, 5368780, 1, 100)
    print test.v_friends(UserAPITypes.OnlineFirends, 5368780, 1, 100)

def test_04():
    inbox = test.v_messages(UserAPITypes.Inbox, None, 0, 100)
    outbox = test.v_messages(UserAPITypes.Outbox, None, 0, 100)
    conversations = test.build_conversations(inbox.messages, outbox.messages)
    for conversation in conversations:
        print "conversation: " + conversation.mwith.name
        for message in conversation.messages:
            print  "\t<" + message.text + ">"


tests = [test_01, test_04]

try:
    session = Session()
    session.login(USER, PASS)
    
    test = UserAPI(session)
    
    print "Own ID: " + str(test.get_own_id())
    
    for testcase in tests:
        print "---------------------------"
        testcase()

    session.logout()

except UserAPIError as error:
    print "Get code: " + str(error.code) + " " + error.text

