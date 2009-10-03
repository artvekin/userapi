class UserAPIError:
    def __init__(this, code, action, text):
        this.code = code
        this.action = action
        this.text = text


class JSONProblemError(Exception):
    def __init__(self, json_data, supplement):
        self.json_data = json_data
        self.supplement = supplement
