#!/usr/bin/python3
from datetime import *
from google.cloud import firestore
from dateutil.relativedelta import relativedelta

def aggiungi_bolletta(data, _):
    db = firestore.Client(database='sac-db')
    nuova_lettura = data['value']['fields']
    data_nuova_lettura = nuova_lettura['documentId']['stringValue']
    valore_nuova_lettura = int(nuova_lettura['value']['integerValue'])
    costo_nuova_lettura = valore_nuova_lettura * 0.5

    """
        la bolletta fa sempre riferimento al mese successivo.
        una lettura, quindi, viene sempre inserita nella bolletta del mese
        successivo alla lettura stessa!
    """

    bolletta_di_riferimento = date_from_str(data_nuova_lettura) + relativedelta(months=+1)
    bolletta_ref = db.collection('bollette').document(f'{bolletta_di_riferimento.month}-{bolletta_di_riferimento.year}')
    if not bolletta_ref.get().exists:
        bolletta_ref.set({
        "consumi": valore_nuova_lettura,
        "costo_complessivo": costo_nuova_lettura,
        "letture": [valore_nuova_lettura]
    })
    else:
        bolletta_ref.update({
            "consumi": firestore.Increment(valore_nuova_lettura),
            "costo_complessivo": firestore.Increment(costo_nuova_lettura),
            "letture": firestore.ArrayUnion([valore_nuova_lettura])
        })

def date_from_str(d: str) -> datetime:
    try: return datetime.strptime(d, '%d-%m-%Y')
    except: return None