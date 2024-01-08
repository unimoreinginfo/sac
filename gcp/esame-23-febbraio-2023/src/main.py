from flask import Flask, render_template, request
from flask_restful import Api
from api import AddChirp, GetChirp, CleanChirps
from chirps_dao import db

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='static', 
            template_folder='templates'
)

api = Api(app)
base =  '/api/v1'

api.add_resource(AddChirp, f'{base}/chirps')
api.add_resource(GetChirp, f'{base}/chirps/<id>')
api.add_resource(CleanChirps, f'{base}/clean')

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/chirptag')
def hashtag_page():
    chirptag = request.args.get('value')
    chirptag_ref = db.collection('hashtags').document(chirptag).get()

    if chirptag_ref.exists:
        chirp_dict = chirptag_ref.to_dict()
        print(chirp_dict)
        return render_template(
            'chirptag.html', 
            chirptag=chirp_dict, 
            mess_keys=map(lambda mess: list(mess.keys()), chirp_dict['messages']), 
            chirptag_name=chirptag
        )
    else:
        return render_template('chirptag_404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)