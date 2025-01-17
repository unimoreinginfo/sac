from google.cloud import firestore
from utils import generate_timestamp
class santaDAO(object):
    def __init__(self):
        self.db = firestore.Client()

    def clean_db(self):
        try:
            ref=self.db.collection('participant')
            for doc in ref.list_documents():
                doc.delete()
            another_ref=self.db.collection('secret-santa')
            for doc in another_ref.list_documents():
                doc.delete()
        except Exception as e:
            print(f'Exception caught in clean_db(): {str(e)}')
    
    def get_participant(self, email:str):
        h = self.db.collection('secret-santa').document(email).get()
        rv = h.to_dict() if h.exists else None
        return rv
    
    def add_participant(self, email:str, participant:dict):
        participant_ref=self.db.collection('participant')
        timestamp = generate_timestamp()
        participant_ref.document(email).set({**participant, 'timestamp': timestamp})

        secret_santa_ref=self.db.collection('secret-santa')
        last_added = self.get_most_recent_participants()

        if len(last_added) == 1:
            secret_santa_ref.document(email).set({'fromEmail': email, 'fromFirstName': participant['firstName'], 'fromLastName': participant['lastName'], 'toEmail': email, 'toFirstName': participant['firstName'], 'toLastName': participant['lastName']})
        elif len(last_added) == 2:
            from_gift = last_added[1]
            secret_santa_ref.document(from_gift['email']).set({'toEmail': email, 'toFirstName': participant['firstName'], 'toLastName': participant['lastName'], 'fromEmail': from_gift['email'], 'fromFirstName': from_gift['firstName'], 'fromLastName': from_gift['lastName']})
            
            first_added = self.get_least_recent_participant()[0]
            secret_santa_ref.document(email).set({'fromEmail': email, 'fromFirstName': participant['firstName'], 'fromLastName': participant['lastName'], 'toEmail': first_added['email'], 'toFirstName': first_added['firstName'], 'toLastName': first_added['lastName']})
        h = participant_ref.document(email).get()
        rv = h.to_dict() if h.exists else None
        if rv is not None:
            del rv['timestamp']
        return rv
    
    def get_giver_receiver(self, email:str):
        h = self.db.collection('secret-santa').document(email).get()
        rv = h.to_dict() if h.exists else None
        return rv

    def get_most_recent_participants(self) -> list[dict]:
        items = self.db.collection('participant').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(2).stream()
        rv = [{'email': item.id, **item.to_dict()} for item in items if item.exists]
        return rv

    def get_least_recent_participant(self) -> list[dict]:
        items = self.db.collection('participant').order_by('timestamp', direction=firestore.Query.ASCENDING).limit(1).stream()
        rv = [{'email': item.id, **item.to_dict()} for item in items if item.exists]
        return rv