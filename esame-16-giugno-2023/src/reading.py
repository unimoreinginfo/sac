from utils import date_from_str, db

class Readings():
    def clear():
        for doc_ref in db.collection('letture').stream():
            doc = doc_ref.to_dict()['documentId']
            db.collection('letture').document(doc).delete()
        

class Reading():
    def add(date, value):
        """
            nota:
            nell'aggiunta della lettura, duplico anche il documentId (ovvero la data),
            questo perché non sono riuscito a far funzionare la query che c'è
            nel metodo interpolateFrom facendo la query sul nome del documento (non lo posso usare come predicato di filtering).
        """
        ref = db.collection('letture').document(date)
        if ref.get().exists:
            return False
        
        ref.set({
                "value": value,
                "documentId": date
            })

        return True
    
    def getOne(date,) -> (bool, int): 
        """ 
            la virgola, in questo caso, è necessaria, perché indica che
            il metodo è statico, poiché, se passassi un solo parametro senza la virgola,
            tale parametro verrebbe intepretato come "self"
        """
        ref = db.collection('letture').document(date)
        result = ref.get()
        if not result.exists:
            return None
        
        return result.to_dict()
    
    def interpolateFrom(date,):
        ref = db.collection('letture') \
            .where(
                field_path='documentId',
                op_string='<',
                value=date
            ) \
            .order_by('documentId') \
            .limit(2) \
            .get()
        
        

        if len(ref) == 0:
            return True, 0
        
        if len(ref) == 1:
            return True, int(ref[0].to_dict()['value']);

        c1 = int(ref[0].to_dict()['value'])
        c2 = int(ref[1].to_dict()['value'])
        t1 = date_from_str(ref[0].to_dict()['documentId'])
        t2 = date_from_str(ref[1].to_dict()['documentId'])
        now = date_from_str(date)
        delta = (t2 - t1).total_seconds()
        delta_now = (now - t2).total_seconds()

        cx = c2 + ((c2 - c1) / delta) * delta_now

        return True, int(cx)

        