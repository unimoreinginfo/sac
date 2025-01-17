from flask import Flask, request, render_template
from flask_restful import Api
import requests
from api import santaEmailResource, cleanResource
from form import participantForm, toForm
import os

app = Flask(__name__,
    static_folder='static',
    static_url_path='/static'
)
api = Api(app)
base_url = '/api/v1'
project_id = os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys() else 'uaas070120252'

api.add_resource(santaEmailResource, f'{base_url}/santa/<email>')
api.add_resource(cleanResource, f'{base_url}/clean')

@app.route('/', methods=['GET'])
def homepage():
    routes = ['secretSantaForm']
    return render_template('index.html', routes=routes)


@app.route('/secretSantaForm', methods=['GET', 'POST'])
def secret_santa():
    errore = ''
    errore2 = ''

    if request.method == 'POST':
        cform1 = participantForm(request.form)
        nome = cform1.nome.data
        cognome = cform1.cognome.data
        email = cform1.email.data
        
        if nome is None and cognome is None and email is None:
                errore = ''
        else:
            body = {
            'firstName': nome,
            'lastName' : cognome
            }
            
            r1 = requests.post(f'https://{project_id}.nw.r.appspot.com{base_url}/santa/{email}', json=body)
            if r1.status_code == 409:
                errore = 'Conflitto'
            elif r1.status_code == 400:
                errore = 'Formato errato di email, nome o cognome (o tutti e 3)'
            else:
                errore = f'Inserito {nome} {cognome} <{email}>'

        cform2 = toForm(request.form)
        email2 = cform2.email2.data
        if email2 is None:
                errore2= ''
        else: 
            r2 = requests.get(f'https://{project_id}.nw.r.appspot.com{base_url}/santa/{email2}')
            if r2.status_code == 404:
                errore2 = 'Non esisti nel database del secret santa!'
            elif r2.status_code == 400:
                errore2 = 'Formato errato di mail'
            else:
                content = r2.json()
                name = content['fromFirstName']
                destN = content['toFirstName']
                destS = content['toLastName']
                destE = content['toEmail']

                errore2 = f'Ehi {name} devi fare il regalo a {destN} {destS} <{destE}>'



    cform1 = participantForm()
    cform2 = toForm()
    return render_template(
        'form.html',
        form1=cform1,
        form2=cform2,
        errore=errore,
        errore2=errore2
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
