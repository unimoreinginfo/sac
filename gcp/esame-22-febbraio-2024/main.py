from flask import Flask, render_template_string,render_template, request
from dao_gcp import DAO
from myForm import MyForm, CantiereForm
import json
import os
from google.cloud import pubsub_v1


app = Flask(__name__, static_url_path='/static', static_folder='static') ## instanzia oggetto Flask

dao = DAO()

topic_name='NUOVO-CANTIERE'
project_id='umarellasservice'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)



##### Index page of the web app
@app.route('/search', methods=['GET','POST'])
def search():
    cantieri=[]
    umarells=[]
    if request.method == 'POST':
        cform = MyForm(request.form)
        cap = cform.cap.data
        umarell = cform.umarell.data
        cantiere = cform.cantiere.data
        both = cform.both.data
        umarells,cantieri = dao.query(cap,umarell,cantiere,both)
        print(umarells)
        print(cantieri)
        ### post
        

    cform = MyForm()
    return render_template('item_form.html', form=cform,cantieri=cantieri,umarells=umarells)

@app.route('/addCantiere', methods=['GET','POST'])
def add_cantiere():
    if request.method == 'POST':
        cform = CantiereForm(request.form)
        cap = cform.cap.data
        id = cform.id.data
        indirizzo = cform.indirizzo.data
        dao.add_cantiere(id,indirizzo,cap)
        if dao.get_cantiere(id) is not None:
           publisher.publish(topic_path, json.dumps("Nuovo cantiere " + str(indirizzo) + "CAP: "+str(cap)).encode('utf-8'))
        ### post
        

    cform = CantiereForm()
    return render_template('cantiere_form.html', form=cform)

    
    
##### Index page of the web app
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', item=None)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',path=request.path),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)