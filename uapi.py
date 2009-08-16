from userapi import *

USER = "test.vkontakte@mail.ru"
PASS = "yi8zXpHIs"
DID="11784322"
DID2="5368780"

        
try:
    session = Session()
    session.login(USER, PASS)
    
    test = UserAPI(session)
    
    print "Own ID: " + str(test.get_own_id())
    
    # print "-----------------------------"

    # Friends = test.v_friends(UserAPITypes.OnlineFirends, test.get_own_id(), 0, 100)
    # print "-----------------------------"

    # for friend in Friends:
    #     print friend.name + "\t<" + str(friend.id) + ">"

    
    # # print test.v_friends(None, 5368780, 1, 100)
    # # print test.v_friends(UserAPITypes.OnlineFirends, 5368780, 1, 100)

  
    
except UserAPIError as error:
    print "Get code: " + str(error.code) + " " + error.text

