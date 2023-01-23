class Teammate:
    def __init__(self, email, is_admin, pending_token=None, username=None, scopes=None):
        self.email = email
        self.username = username or email.split("@")[0]
        self.pending_token = pending_token
        self.is_admin = is_admin
        self.scopes = scopes

    def to_dict(self):
        return self.__dict__
