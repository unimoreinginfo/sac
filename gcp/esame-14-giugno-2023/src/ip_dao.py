from google.cloud import firestore
db = firestore.Client(database='sac-db')

class RoutingTable():
    def getRule(id: str, ):
        rule = db.collection('routing').document(id).get()
        if not rule.exists:
            return None
        
        return rule.to_dict()


    def list(dicts=False,):
        rules = []
        for rule in db.collection('routing') \
            .order_by('netmaskCIDR', direction=firestore.Query.DESCENDING).stream():
                if dicts:
                    rules.append({**rule.to_dict(), "rule_id": rule.id})
                else:
                    rules.append(rule.id)

        return rules

    def delete(id: str, ):
        db.collection('routing').document(id).delete()

    def update(id: str, rule):
        if not db.collection('routing').document(id).get().exists:
            return None
        
        db.collection('routing').document(id).update(rule)
        return db.collection('routing').document(id).get().to_dict()

    def clean():
        for document in db.collection('routing').stream():
            db.collection('routing').document(document.id).delete()

    def addRule(id: str, rule) -> bool:
        rule_ref = db.collection('routing').document(id).get()
        if rule_ref.exists:
            return False
        
        db.collection('routing').document(id).set(rule)
        return True