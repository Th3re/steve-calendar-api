from api.token.service import TokenService, Token


class SteveTokenService(TokenService):
    def fetch(self, user_id: str) -> Token:
        return Token(value='3xi4n23x42')