from flask import Flask, render_template, request
from api import PostConsumi, DeleteConsumi
from flask_restful import Api
from utils import db, date_from_str
from dateutil.relativedelta import relativedelta

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='static', 
            template_folder='templates'
)

api = Api(app)
base = '/api/v1'
mesi = [
    'gennaio',
    'febbraio',
    'marzo',
    'aprile',
    'maggio',
    'giugno',
    'luglio',
    'agosto',
    'settembre',
    'ottobre',
    'novembre',
    'dicembre'
]

api.add_resource(PostConsumi, f'{base}/consumi/<string:date>')
api.add_resource(DeleteConsumi, f'{base}/clean')

@app.route('/bollette')
def list_bollette():
    bollette_coll = db.collection('bollette').limit(12).stream()
    bollette = []
    for bolletta in bollette_coll:
        print(bolletta.id)
        bollette.append(
            {
                'id': bolletta.id,
                **(db.collection('bollette').document(bolletta.id).get().to_dict())
            }
        )

    return render_template('bollette.html', lista_bollette=bollette)

@app.route('/bolletta/<id>')
def dettaglio_bolletta(id: str):
    bolletta_ref = db.collection('bollette').document(id).get()
    if not bolletta_ref.exists:
        return render_template("404_bolletta.html"), 404
    
    data_di_riferimento = date_from_str(f'01-{id}') + relativedelta(months=-1)
    mese = data_di_riferimento.month - 1;
    bolletta_dict = bolletta_ref.to_dict()

    return render_template(
        "bolletta.html", 
        rif=f'{mesi[mese]} {data_di_riferimento.year}', 
        bolletta={'id': id, **bolletta_dict},
        ultima_lettura=bolletta_dict['letture'][len(bolletta_dict['letture']) - 1]
    )
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)