from environs import Env


class Settings:
    def __init__(self):
        env = Env()
        self.user = env.str("SN_USER_NAME")
        self.password = env.str("SN_PASSWORD")

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password
