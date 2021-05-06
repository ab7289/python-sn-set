from environs import Env

env = Env()
env.read_env()

USER = env.str("SN_USER_NAME")
PASSWORD = env.str("SN_PASSWORD")
