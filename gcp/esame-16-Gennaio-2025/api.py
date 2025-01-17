from flask import request
from flask_restful import Resource
from typing import Optional
from dao import santaDAO
from utils import email_validate

dao = santaDAO()

class cleanResource(Resource):
    def get(self) -> tuple[None, int]:
        dao.clean_db()
        return None,200
    
class santaEmailResource(Resource):

    def validate_body(self, body:Optional[dict]) -> bool:
        keys = ['firstName', 'lastName']
        for k in keys:
            if k not in body.keys():
                return False

        v1 = body['firstName']
        v2 = body['lastName']

        if not isinstance(v1, str) or not isinstance(v2, str):
            return False

        if v1 == '' or v2 == '':
            return False
                
        return True
    
    def get(self, email:Optional[str]) -> tuple[Optional[dict], int]:
        if not email_validate(email):
            return {'message':'Generic error'}, 400
        
        h = dao.get_giver_receiver(email)
        if h is None:
            return {'message':'Not Found'}, 404
        
        return h, 200
    
    def post(self, email:Optional[str]) -> tuple[Optional[dict], int]:
        if not email_validate(email):
            return {'message':'Generic error'}, 400
        
        body = request.json

        if not self.validate_body(body):
            return {'message':'Generic error'}, 400
        
        if dao.get_participant(email) is not None:
            return {'message': 'Conflict'}, 409
        
        h = dao.add_participant(email, body)
        return h, 201
        




