class Privacy:
    def __init__(self, may_look_profile, may_look_wall, may_leave_messages):
        self.may_look_profile   = may_look_profile
        self.may_look_wall      = may_look_wall
        self.may_leave_messages = may_leave_messages

class Position:
    def __init__(self, id_country, iso, id_city, city):
        self.id_country = id_country
        self.iso        = iso
        self.id_city    = id_city
        self.city       = city

class MaritalStatus:
    def __init__(self, status):
        self.status = status

    def getStatus(self):
        return self.status


class PoliticView:
    def __init__(self, status):
        self.status = status

    def getStatus(self):
        return self.status


class PersonsProfile:
    def __init__(self):
        self.mother     = None
        self.position   = None
        self.birthday   = None
        self.state      = None
        self.politics   = None
        self.friends    = None
        self.friends_online = None
        self.shared_friends = None
        self.status     = None
        self.own_photos = None
        self.mark_photos= None
        self.privacy    = None
        self.wall       = None
        self.online     = None
        self.education_list = None
        self.requester_id         = None 
        self.is_requester_friend  = None 
        self.is_requester_invited = None 
        self.is_requester_favour  = None 
        
        
class Person:
    def __init__(self,
                 id, name, avatar, isOnline,  # Always
                 miniimg = None, sex = None,  # Message Parse
                 profile = None):             # Other parameters

        if profile == None:
            profile = PersonsProfile()
        
        self.id         = id
        self.name       = name
        self.mother     = profile.mother
        self.status     = profile.status
        self.position   = profile.position
        self.sex        = sex
        self.avatar     = avatar
        self.birthday   = profile.birthday
        self.state      = profile.state
        self.politics   = profile.politics
                      
        self.friends    = profile.friends
        self.friends_online = profile.friends_online
        self.shared_friends = profile.shared_friends

        self.own_photos = profile.own_photos
        self.mark_photos= profile.mark_photos

        self.privacy    = profile.privacy
        self.wall       = profile.wall

        self.online     = profile.online

        self.requester_id         = profile.requester_id
        self.is_requester_friend  = profile.is_requester_friend
        self.is_requester_invited = profile.is_requester_invited
        self.is_requester_favour  = profile.is_requester_favour

        self.education = profile.education_list


class Persons:
    def __init__(self, total, count, persons):
        self.total      = total
        self.count      = count
        self.persons    = persons



