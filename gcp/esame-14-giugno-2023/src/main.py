from flask import Flask, render_template
from flask_restful import Api
from api import AddRule, CleanTable, PutRule, DeleteRule, GetRules, GetRule, RouteIp
from ip_dao import RoutingTable

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='static', 
            template_folder='templates'
)

api = Api(app)
base =  '/api/v1'

api.add_resource(AddRule, f'{base}/routing/<int:id>')
api.add_resource(PutRule, f'{base}/routing/<int:id>')
api.add_resource(DeleteRule, f'{base}/routing/<int:id>')
api.add_resource(GetRule, f'{base}/routing/<string:id>')
api.add_resource(GetRules, f'{base}/routing/')
api.add_resource(RouteIp, f'{base}/routing/')
api.add_resource(CleanTable, f'{base}/clean')

@app.get('/')
def index():
    routing_table = RoutingTable.list(dicts=True)
    return render_template('index.html', routing_table=routing_table)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)