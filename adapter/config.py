import os
from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASS = os.getenv("REDIS_PASS")
REDIS_DRIVER = os.getenv("REDIS_DRIVER")
REDIS_DB = 0
REDIS_URI = f'{REDIS_DRIVER}://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?ssl_cert_reqs=none'

# DB
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DRIVER = "postgresql"


DB_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
print(DB_URI)