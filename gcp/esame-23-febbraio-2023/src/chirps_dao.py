from google.cloud import pubsub_v1, firestore
from google.api_core.exceptions import AlreadyExists
import uuid
from datetime import datetime, timezone

db = firestore.Client(database='sac-db')
publisher = pubsub_v1.PublisherClient()


class Chirps():

    def clean():
        for message in db.collection('messages').stream():
            db.collection('messages').document(message.id).delete()

        for hashtag in db.collection('hashtags').stream():
            db.collection('hashtags').document(hashtag.id).delete()

    def getChirp(id: str,):
        chirp_ref = db.collection('messages').document(id).get()
        if chirp_ref.exists:
            return chirp_ref.to_dict()
        
        return None

    def add(message: str, hashtags: list) -> (str, int):
        id = str(uuid.uuid1())
        utc_timestamp = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())

        db.collection('messages').document(id).set({
            "message": message,
            "hashtags": hashtags,
            "timestamp": utc_timestamp
        })

        # aggiungo i messaggi al documento riguardante un hashtag
        for hashtag in hashtags:
            hashtag_ref = db.collection('hashtags').document(hashtag).get()
            # creo il topic per dopo in caso l'hashtag non esista a db
            if not hashtag_ref.exists:
                try:
                    path = publisher.topic_path('sac-emilianomaccaferri', hashtag)
                    publisher.create_topic(request={ "name": path })
                    print(f"topic: #{hashtag} creato")
                except AlreadyExists:
                    print(f"il topic #{hashtag} esiste già")

            db.collection('hashtags').document(hashtag).set({
                'messages': firestore.ArrayUnion([{ id: utc_timestamp }])
            })

        return id, utc_timestamp