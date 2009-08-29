import Parser

class Message:
    def __init__(self, id, time, text, mfrom, mto, isReaded):
        self.id        = id
        self.time      = time
        self.text      = text
        self.mfrom     = mfrom
        self.mto       = mto
        self.isReaded  = isReaded


class Messages:
    def __init__(self, total, history, count, messages):
        self.total     = total
        self.history   = history
        self.count     = count
        self.messages  = messages


class Conversation:
    def __init__(self, mwith, messages):
        self.mwith     = mwith
        self.messages  = messages

