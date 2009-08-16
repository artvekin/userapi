class Position:
    def __init__(self, id_country, iso, id_city, city):
        self.id_country = None
        self.iso        = None
        self.id_city    = None
        self.city       = None


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


class Persons:
    def __init__(self, total, count, persons):
        self.total      = total
        self.count      = count
        self.persons    = persons



