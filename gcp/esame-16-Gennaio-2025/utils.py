import re
from typing import Optional
from datetime import datetime


def email_validate(email:Optional[str]):
    if not isinstance(email, str):
        return False
    
    pattern = r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_timestamp() -> str:
    return str(datetime.now().timestamp())