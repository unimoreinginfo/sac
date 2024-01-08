import re

def get_hashtags(msg: str) -> list:
    return list(dict.fromkeys(re.findall('#(\w+)', msg)))