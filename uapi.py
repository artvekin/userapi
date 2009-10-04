# -*- coding: utf-8 -*- 

from userapi import *

USER = "test.vkontakte@mail.ru"
PASS = "yi8zXpHIs"
DID="41657126"

def test_profile(id = None):
    profile = test.v_profile(id)
    print "Profile of user " + profile.name + " <" + str(profile.id) + "> "
    print "Mother: " + str(profile.mother)
    print "Status: "   + str(profile.status)
    print "Sex: "     + str(profile.sex)
    print "Pic: "     + str(profile.avatar)
    print "Birthday: " + str(profile.birthday)
    print "State: "   + str(profile.state.getStatus())
    print "Political: " + str(profile.politics.getStatus())
    print "Friends: "

    

    for friend in profile.friends.persons:
        print friend.name
        print friend.id
        print friend.name + " <" + str(friend.id) + ">"

    print "Friends on-line:"
    for friend in profile.friends_online.persons:
        print friend.name + " <" + str(friend.id) + ">"

    print "Friends shared:"
    for friend in profile.shared_friends.persons:
        print friend.name + " <" + str(friend.id) + ">"

    print "My photos:"
    for photo in profile.own_photos.photos:
        print str(photo.pic)

    print "Photos with me:"
    for photo in profile.mark_photos.photos:
        print str(photo.pic)

    print "Wall not yet implemented"

    print "On-line status: " + str(profile.online)

    print "Education statements not implemented fully yet:"
    print str(profile.education)


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
    test_profile()

def test_05_1():
    test_profile(5368780)

def test_06():
    wall = test.v_wall(test.get_own_id(), 0, 100)
    for message in wall.messages:
        print message.mfrom.name + "\t<" + message.text + ">" + "\t == " + (message.original_url or "--")



tests = [test_01, test_05, test_05_1, test_06]

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

except JSONProblemError as error:
    print "JSON data is a bullshit, storing to disk"
    f = file('bs', 'w')
    f.write(error.json_data)
    f.write("\n\n\n" + str(error.supplement))
    f.close()
