from environs import Env


class Settings:
    def __init__(self):
        env = Env()
        env.read_env()
        self.user: str = env.str("SN_USER_NAME")
        self.password: str = env.str("SN_PASSWORD")
        self.use_oauth: bool = env.bool("SN_SET_USE_OAUTH", False)
        if self.use_oauth:
            self.client_id: str = env.str("SN_SET_CLIENT_ID")
            self.client_secret: str = env.str("SN_SET_CLIENT_SECRET")
            self.grant_type: str = env.str("SN_SET_GRANT_TYPE", "password")

    def get_user(self) -> str:
        return self.user

    def get_password(self) -> str:
        return self.password

    def get_use_oauth(self) -> bool:
        return self.use_oauth

    def get_client_id(self) -> str | None:
        if self.use_oauth:
            return self.client_id

    def get_client_secret(self) -> str | None:
        if self.use_oauth:
            return self.client_secret

    def get_grant_type(self) -> str | None:
        if self.use_oauth:
            return self.grant_type
