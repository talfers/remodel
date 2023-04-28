import os
from log import logging
from dotenv import load_dotenv

load_dotenv('../secrets.env')

logger = logging.getLogger('config.py')

class Config:
    def __init__(self):
        self.postgres_auth = os.getenv('RDEI_AUTH', 'NOT PROVIDED') 
        self.cleversafe_auth = os.getenv('CLEVERSAFE_AUTH', 'NOT PROVIDED')
        self.slack_bot_key = os.getenv('SLACK_BOT_KEY', 'NOT PROVIDED')