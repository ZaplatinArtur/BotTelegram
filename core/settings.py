from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token:str
    admin_id:int

@dataclass
class Settings:
    bots: Bots

