import requests

from requests_oauthlib import OAuth1


class Session(requests.Session):
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_secret: str
    ) -> None:
        super().__init__()

        self.auth = OAuth1(
            api_key,
            client_secret=api_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_secret
        )
