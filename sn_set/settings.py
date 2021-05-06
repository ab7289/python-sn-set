from environs import Env

env = Env()
env.read_env()

USER = env.str("USER_NAME")
PASSWORD = env.str("PASSWORD")
