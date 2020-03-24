class Credentials:
    def __init__(self, refresh_token, user_id):
        self.user_id = user_id
        self.refresh_token = refresh_token

    def __repr__(self):
        return f'USER_ID: {self.user_id} REFRESH_TOKEN: {self.refresh_token}'
