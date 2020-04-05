from api.model.representation import PrettyPrint


class Credentials(PrettyPrint):
    def __init__(self, refresh_token, user_id):
        self.user_id = user_id
        self.refresh_token = refresh_token
