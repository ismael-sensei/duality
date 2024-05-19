import os
from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# REDIS
REDIS_URI = f'{os.getenv("REDIS_TLS_URL")}?ssl_cert_reqs=none'

# DB
DATABASE_URI = f'{os.getenv("DATABASE_URL").replace('postgres', 'postgresql')}?sslmode=require'