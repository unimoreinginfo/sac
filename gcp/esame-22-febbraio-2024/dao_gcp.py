import json
from google.cloud import firestore



class DAO(object):
    def __init__(self):
        self.db = firestore.Client()
        self.clean_db()
        self.populate_cantiere('cantiere.json')
        self.populate_umarell('umarell.json')

    ## populate (tested)
    def populate_umarell(self, filename):
        item_ref=self.db.collection('umarell')
        with open(filename) as f:
            items = json.load(f)
            for item in items:
                item_ref.document(str(item['id'])).set({'nome': item['nome'],'cognome': item['cognome'], 'cap': str(item['cap'])})
    
    def populate_cantiere(self, filename):
        item_ref=self.db.collection('cantiere')
        with open(filename) as f:
            items = json.load(f)
            for item in items:
                item_ref.document(str(item['id'])).set({'indirizzo': item['indirizzo'], 'cap': str(item['cap'])})
    
    
    ## clean (tested)
    def clean_db(self):
        try:
            ref=self.db.collection('cantiere')
            for doc in ref.list_documents():
                doc.delete()
            another_ref=self.db.collection('umarell')
            for doc in another_ref.list_documents():
                doc.delete()
        except Exception as e:
            print("Exception cought in clean_db(): {" + str(e) + "}")

    ## read 
    def get_umarell(self, iditem):
        h = self.db.collection('umarell').document(str(iditem)).get()
        rv = h.to_dict() if h.exists else None
        if rv is not None:
            rv['cap'] = int(rv['cap'])
        return rv
    
    ## read 
    def get_cantiere(self, iditem):
        h = self.db.collection('cantiere').document(str(iditem)).get()
        rv = h.to_dict() if h.exists else None
        if rv is not None:
            rv['cap'] = int(rv['cap'])
        return rv
    
    ## create (tested)
    def add_umarell(self,iditem,nome,cognome,cap):
        umarell_ref=self.db.collection('umarell')
        umarell_ref.document(str(iditem)).set({'nome': nome, 'cognome': cognome,'cap':str(cap)})
    
    def add_cantiere(self,iditem,indirizzo,cap):
        umarell_ref=self.db.collection('cantiere')
        umarell_ref.document(str(iditem)).set({'indirizzo': indirizzo, 'cap': str(cap)})
        ## querying ## (tested)
        
    def query(self,cap, umarell, cantiere,both):
        #:: Various operators
            # '=='
            # '!='
            # '>='
            # '<='
            # '>'
            # '<'
        print(both)
        if both is True:
            items = self.db.collection('umarell').where('cap', '==', str(cap)).stream()
            umarells = [item.to_dict() for item in items if item.exists]
            items = self.db.collection('cantiere').where('cap', '==', str(cap)).stream()
            cantieri = [item.to_dict() for item in items if item.exists]         
            return umarells,cantieri
        elif umarell is True:
            items = self.db.collection('umarell').where('cap', '==', str(cap)).stream()
            umarells = [item.to_dict() for item in items if item.exists]
            return umarells, []
        elif cantiere is True:
            items = self.db.collection('cantiere').where('cap', '==', str(cap)).stream()
            cantieri = [item.to_dict() for item in items if item.exists]
            return [], cantieri
        return [], []
    
    
######################################
    ## update(tested)
    def update_item(self,iditem,property,property2):
        object_ref = self.db.collection('items').document(str(iditem))
        object_ref.update({'property': property,'property2':property2})      
    
        
    ## delete (tested)
    def delete_item(self,iditem):
        ref = self.db.collection('collection_name'); 
        doc = ref.document(str(iditem)).get()  
        if doc.exists:     
            print(f'Document data: {doc.to_dict()}')     
            doc.reference.delete() 
        else:     
            print('No such document!')
    



    
    
    ## increment (tested)
    def increase_attribute(self,iditem):
        name=name.upper()
        self.db.collection('item').document(str(iditem)).update({"attribute": firestore.Increment(1)})

    ## order by attribute with a top k (tested)
    def get_most_viewed(self,top=4):
        items = self.db.collection('item').order_by('attribute', direction=firestore.Query.DESCENDING).limit(top).stream()
        rv = [item.to_dict() for item in items if item.exists]
        return rv
    
    
    def get_items_with_identifier(self):
        items = self.db.collection('item').stream()
        rv = [
            {**item.to_dict(), 'id': item.id} 
            for item in items if item.exists
        ]
        return rv
