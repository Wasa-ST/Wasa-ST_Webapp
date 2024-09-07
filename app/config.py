import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", None)
ALGORITHM = os.environ.get("ALGORITHM", None)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
ALGORITHM = os.environ.get("ALGORITHM", None)
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))
