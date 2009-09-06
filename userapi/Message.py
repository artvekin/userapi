import Parser

class Message:
    TEXT   = 0
    PHOTO  = 1
    GRAPHITY = 2
    VIDEO = 3
    AUDIO = 4
    def __init__(self, id, time, text, mfrom, mto, isReaded,
                # Parameters defined at wall's messages retrieval
                message_type = 0, message_name = None,
                thumb_url = None, original_url = None,
                owner_id = None, item_id = None,
                item_size = None):
        self.id        = id
        self.time      = time
        self.text      = text
        self.mfrom     = mfrom
        self.mto       = mto
        self.isReaded  = isReaded
        self.message_type = message_type
        self.message_name = message_name
        self.thumb_url = thumb_url
        self.original_url = original_url
        self.owner_id  = owner_id
        self.item_id   = item_id
        self.item_size = item_size


class Messages:
    def __init__(self, total, history, count, messages):
        self.total     = total
        self.history   = history
        self.count     = count
        self.messages  = messages


class History:
    def __init__(self, version, action, message):
        self.version   = version
        self.action    = action
        self.message   = message


class Conversation:
    def __init__(self, mwith, messages):
        self.mwith     = mwith
        self.messages  = messages

