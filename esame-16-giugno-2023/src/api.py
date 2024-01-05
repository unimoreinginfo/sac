from flask_restful import Resource
from flask import request
from utils import date_from_str
from google.cloud import firestore
from reading import Reading, Readings

class DeleteConsumi(Resource):
    def post(self):
        Readings.clear()
        None, 200

class PostConsumi(Resource):
    def validate_body(self, json_body):
        if 'value' not in json_body:
            return None
        
        if type(json_body['value']) is not int:
            return None
        
        if json_body['value'] < 0:
            return None

        return True
    
    def get(self, date):

        """
            questo metodo ha un duplice comportamento:
                - se alla data inserita vi è una lettura, ritornerà il valore di quella lettura
                - se alla data inserita non vi è una lettura, allora interpolerà il valore delle
                    letture precedenti mediante la formula scritta nella traccia 
                
            nel primo caso, isInterpolated sarà **sempre** false, mentre nel secondo, sarà true qualora
            vi siano almeno due letture precedenti alla data specificata
        """

        if date_from_str(date) == None:
            return None, 400
        
        if (reading := Reading.getOne(date)) is not None: 
            # l'operatore := permette di assegnare la variabile in maniera inline 
            return {
                "value": reading["value"],
                "isInterpolated": False
            }
        # reading è None, devo interpolare
        is_interpolated, value = Reading.interpolateFrom(date)

        return {
            "value": value,
            "isInterpolated": is_interpolated
        }, 200


    def post(self, date):

        """
            questo metodo inserisce la lettura a database dentro la 
            collezione 'letture'.
            se la lettura è già presente ritorna 409, altrimenti ritorna 201
            assieme al valore inserito a db
        """

        body = request.json
        if date_from_str(date) == None:
            return None, 400

        if self.validate_body(body) == None:
            return None, 400
        
        try: 
            if Reading.add(date, body['value']) == False:
                return None, 409
        except Exception as err:
            print(err)
            return {
                "description": "Generic error"
            }, 500
        
        return {
            "value": body['value'],
            "isInterpolated": False
        }, 201