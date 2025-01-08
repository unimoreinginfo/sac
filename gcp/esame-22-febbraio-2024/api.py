from flask import Flask, request
from flask_restful import Resource, Api
from dao_gcp import DAO

app = Flask(__name__,static_url_path='/static',static_folder='static')
api = Api(app)
dao= DAO()
basePath = '/api/v1'



project_id = 'progettinoprovinoterzo'
#topic_name=os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'cpu_temperature'
#topic_name2=os.environ['TOPIC2'] if 'TOPIC2' in os.environ.keys() else 'cpu_temperature_alert'
#project_id=os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys()  else 'myprj'

'''publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
topic_path2 = publisher.topic_path(project_id, topic_name2)
publisher.publish(topic_path2, json.dumps(data).encode('utf-8'))'''

class UmarellResource(Resource):
    def get(self,idumarell):
        item = dao.get_umarell(idumarell)
        if item is None:
            return None, 404
        else:
            return item, 200

    def post(self,idumarell):
        itemdata=request.json
        if not self.validate_itemdata(itemdata):
            return None, 400
        item = dao.get_umarell(idumarell) 
        if item is not None: ## Already exists
            return None, 409
        dao.add_umarell(idumarell,itemdata['nome'],itemdata['cognome'],itemdata['cap'])
        item = dao.get_umarell(idumarell)
        return item, 201
    
    '''def delete(self,iditem):
        item = dao.get_item(iditem) 
        if item is None: ## Does not exist
            return item, 404
        dao.delete_item(iditem)
        #item = dao.get_item(iditem)
        return None, 204
        #return None, 200
        
    def put(self,idumarell): ### tested (see what responses the validator wants)
        umarelldata=request.json
        umarell = dao.get_umarell(idumarell)
        if umarell is None :
            return None,404
        
        if not self.validate_umarelldata(umarelldata):
            return None, 400
        
        dao.update_umarell(idumarell,umarelldata['nome'],umarelldata['cognome'],umarelldata['cap'])
        umarell = dao.get_umarell(idumarell)
        return umarell, 201
    
    def delete(self,idumarell): ## tested (see the responses that the validator wants)
        umarell = dao.get_umarell(idumarell) 
        if umarell is None: ## Does not exist
            return umarell, 404
        dao.delete_umarell(idumarell)
        #umarell = dao.get_umarell(idumarell)
        return None, 204
        #return None, 200 '''      

        
    def validate_itemdata(self,itemdata):
        for k in ['nome','cognome','cap']:
             if k not in itemdata.keys():
                return False
        if not isinstance(itemdata['cap'],(int)) or not isinstance(itemdata['nome'],(str)) or not isinstance(itemdata['cognome'],(str)):
                return False
        return True       


class CantiereResource(Resource):
    def get(self,idcantiere):
        item = dao.get_cantiere(idcantiere)
        if item is None:
            return None, 404
        else:
            return item, 200

    def post(self,idcantiere):
        itemdata=request.json
        if not self.validate_itemdata(itemdata):
            return None, 400
        item = dao.get_cantiere(idcantiere) 
        if item is not None: ## Already exists
            return None, 409
        dao.add_cantiere(idcantiere,itemdata['indirizzo'],itemdata['cap'])
        item = dao.get_cantiere(idcantiere)
        return item, 201
    
    '''def delete(self,iditem):
        item = dao.get_item(iditem) 
        if item is None: ## Does not exist
            return item, 404
        dao.delete_item(iditem)
        #item = dao.get_item(iditem)
        return None, 204
        #return None, 200
        
    def put(self,idumarell): ### tested (see what responses the validator wants)
        umarelldata=request.json
        umarell = dao.get_umarell(idumarell)
        if umarell is None :
            return None,404
        
        if not self.validate_umarelldata(umarelldata):
            return None, 400
        
        dao.update_umarell(idumarell,umarelldata['nome'],umarelldata['cognome'],umarelldata['cap'])
        umarell = dao.get_umarell(idumarell)
        return umarell, 201
    
    def delete(self,idumarell): ## tested (see the responses that the validator wants)
        umarell = dao.get_umarell(idumarell) 
        if umarell is None: ## Does not exist
            return umarell, 404
        dao.delete_umarell(idumarell)
        #umarell = dao.get_umarell(idumarell)
        return None, 204
        #return None, 200 '''      

        
    def validate_itemdata(self,itemdata):
        for k in ['indirizzo','cap']:
             if k not in itemdata.keys():
                return False
        if not isinstance(itemdata['cap'],(int)) or not isinstance(itemdata['indirizzo'],(str)):
                return False
        return True



## Done and tested
class CleanResource(Resource):
    def get(self):
        dao.clean_db()
        return None, 200


api.add_resource(UmarellResource, f'{basePath}/umarell/<int:idumarell>')
api.add_resource(CantiereResource, f'{basePath}/cantiere/<int:idcantiere>')
#api.add_resource(CantiereResource, f'{basePath}/item/<string:idcantiere>')
api.add_resource(CleanResource, f'{basePath}/clean')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)