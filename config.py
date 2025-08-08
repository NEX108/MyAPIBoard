# config.py

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_WEATHER=os.getenv("API_KEY_WEATHER")
API_KEY_FINANCE=os.getenv("API_KEY_FINANCE")
API_KEY_NASA=os.getenv("API_KEY_NASA")
API_KEY_FORTNITE=os.getenv("API_KEY_FORTNITE")
