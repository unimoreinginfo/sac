from datetime import *
from google.cloud import firestore

db = firestore.Client(database='sac-db')

def date_from_str(d: str) -> datetime:
    try: return datetime.strptime(d, '%d-%m-%Y')
    except: return None

def str_from_date(d):
    return d.strftime('%d-%m-%Y')