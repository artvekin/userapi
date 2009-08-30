import Captcha
from Errors import UserAPIError

import httplib
import re

ID="1"
USERAPI_HOST="login.userapi.com"

class Session:
    def __init__(self, filename = None):
        if filename:
            self.load_session(filename)
            self.renew_session()
        else:
            self.sid = None
            self.remixpass = None
            

    def login(self, user, password, captcha = None):

        connection = httplib.HTTPConnection(USERAPI_HOST)

        login_request = "/auth?login=force&site=" + str(ID)+ "&email=" + user + "&pass=" + password

        if captcha:
            login_request = login_request + "&fcsid=" + str(captcha.csid) + "&fccode=" + captcha.text
        
        connection.request('GET',login_request)
        response = connection.getresponse()
        connection.close()

        if response.status != 302:
            raise UserAPIError(0, "login", "Couldn't connect")

        match = re.search("sid=([\-0-9a-z]+)", response.getheader("location"))
        sid = match.group(1)

        if sid == "-2":
            return self.login(user, password, Captcha())
        
        if sid == "0" or sid == "-1":
            raise UserAPIError(sid, "login", "Bad-bad error while login")

        match = re.search("remixpassword=([a-z0-9]+);",
                                   response.getheader("set-cookie"))

        if not match:
            raise UserAPIError(sid, "login", "Login incorrect (Full login)")

        self.remixpass = match.group(1)
        
        self.sid = sid
        return sid

    def logout(self):

        connection = httplib.HTTPConnection(USERAPI_HOST)

        login_request = "/auth?login=logout&site=" + str(ID) + "&sid=" + self.sid

      
        connection.request('GET',login_request)
        response = connection.getresponse()
        connection.close()

        if response.status != 302:
            raise UserAPIError(0, "login", "Couldn't connect")

        self.sid = None

    def save_session(self, file):
        save = open(file, "w")
        save.write(self.remixpass)
        save.close()
        
    def load_session(self, file):
        load = open(file, "r")
        self.remixpass = load.read()
        load.close()

    def renew_session(self):
        connection = httplib.HTTPConnection("login.userapi.com")

        login_request = "/auth?login=auto&site=" + str(ID)


        connection.request('GET',login_request, None, {"Cookie" : "remixpassword=" + self.remixpass})
        
        response = connection.getresponse()
        connection.close()

        if response.status != 302:
            raise UserAPIError(0, "login", "Couldn't connect")

        match = re.search("remixpassword=([a-z0-9]+);",
                          response.getheader("set-cookie"))

    
        match = re.search("sid=([\-0-9a-z]+)", response.getheader("location"))
        sid = match.group(1)

        if sid == "-2":
            return self.login(user, password, self.captcha())
        if sid == "0" or sid == "-1":
            raise UserAPIError(sid, "login", "Bad-bad error while login")
        
        self.sid = sid
        return sid

    def get_sid(self):
        return self.sid


