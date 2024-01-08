from flask_restful import Resource
from flask import request
from utils import get_hashtags
from chirps_dao import Chirps, publisher
import os

class CleanChirps(Resource):
    def post(self):
        Chirps.clean()

        return None, 200

class AddChirp(Resource):
    def validate_body(self, body):
        if type(body) is not str:
            return False
        
        if len(str(body).strip()) > 100 or len(str(body)) == 0:
            return False
        
        return True

    def post(self):
        body = request.json
        print(body)
        if not self.validate_body(body):
            return None, 400 
        
        hashtags = get_hashtags(body)
        uuid, timestamp = Chirps.add(body, hashtags)

        for hashtag in hashtags:
            path = publisher.topic_path('sac-emilianomaccaferri', hashtag)
            fut = publisher.publish(path, uuid.encode('utf-8'))
            fut.result()

        return {
            "message": body,
            "hashtags": hashtags,
            "timestamp": timestamp,
            "id": uuid
        }, 200
    
class GetChirp(Resource):
    def get(self, id: str):
        chirp = Chirps.getChirp(id.strip())
        if chirp is not None:
            return chirp, 200
        
        return None, 404