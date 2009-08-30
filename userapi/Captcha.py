import webbrowser

class Captcha:
    def __init__(self):
        self.csid =4 # Chosed randomly!
        print "Look at browser and enter the captcha to console"
        
        webbrowser.open("http://userapi.com/data?act=captcha&csid=" + str(self.csid))
        
        self.text = raw_input("VKontakte captcha: ")


