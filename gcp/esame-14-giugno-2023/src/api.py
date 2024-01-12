from flask_restful import Resource
from flask import request
import ipaddress
from ip_dao import RoutingTable

class RouteIp(Resource):
    def post(self):
        ip = request.json
        routing_table = RoutingTable.list(dicts=True)
        try:
            real_ip = ipaddress.ip_address(ip)
            gateway = filter(lambda route: route["netmaskCIDR"] == 0, routing_table)
            for route in routing_table:
                network = ipaddress.ip_network(f'{route["ip"]}/{route["netmaskCIDR"]}', strict=True)
                if real_ip in network:
                    print("found", route)
                    return route["rule_id"], 200
                
            return gateway["rule_id"], 200
        
        except:
            return None, 400


class GetRule(Resource):
    def get(self, id):
        try: 
            int_id = int(id)
            if int_id < 0:
                return None, 400
            
            rule = RoutingTable.getRule(id)
            if rule is None:
                return None, 404
            
            return rule, 200
        except:
            return None, 400

class GetRules(Resource):
    def get(self, ):
        return RoutingTable.list(), 200

class DeleteRule(Resource):
    def delete(self, id: int):
        RoutingTable.delete(str(id))
        return None, 204

class PutRule(Resource):
    def put(self, id: int):
        body = request.json
        if len(body.keys()) == 0:
            return None, 400
        
        route = RoutingTable.update(str(id), body)
        if route is None:
            return None, 404

        return route, 200

class CleanTable(Resource):
    def post(self):
        RoutingTable.clean()
        return None, 200

class AddRule(Resource):
    def validate_body(self, body) -> bool:
        if "ip" not in body and "netmaskCIDR" not in body and "gw" not in body and "device" not in body:
            return False
        
        try:
            ip = ipaddress.ip_address(body["ip"])
            gw = ipaddress.ip_address(body["gw"])
            device = body["device"]
            netmask_cidr = body["netmaskCIDR"]
        
            if not type(device) is str:
                return False
            if not type(netmask_cidr) is int:
                return False
            if not type(body["gw"]) is str:
                return False
            
            ipaddress.IPv4Network(f'{body["ip"]}/{netmask_cidr}', strict=True) # controlla semplicemente se l'ip è di rete
        except ValueError:
            return False

        return True

    def post(self, id: str):
        body = request.json
        try: 
            int_id = int(id)
            if int_id < 0:
                return None, 400
            
            if not self.validate_body(body):
                return None, 400
            
        except:
            return None, 400
        
        else:
            if not RoutingTable.addRule(str(int_id), body):
                return None, 409
            
            return body, 201

        
