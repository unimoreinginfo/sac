from pprint import pprint
import requests
from typing import Optional
import yaml
import json
import re


class ErrorCodes:
    OK = 0
    RC_ERROR = 1
    BODY_ERROR = 2
    INT_ERROR = 3
    _descriptions = {
        OK: 'OK', 
        RC_ERROR: 'RC_Error', 
        BODY_ERROR: 'Body_Error', 
        INT_ERROR: 'Internal_Error'
    }
    
    def is_error(e):
        return e != ErrorCodes.OK
    
    def get_error(e):
        return ErrorCodes._descriptions[e] if e in ErrorCodes._descriptions.keys() else ''
        

def get_json(r: requests.Response) -> Optional[dict]:
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        return None
    

def ret_format(err_code, exp_sc, res_sc, exp_bd, res_bd, req_url, req_met, req_bd) -> dict:
    return {'error': err_code, 
            'expected_sc': exp_sc, 
            'response_sc': res_sc, 
            'expected_bd': exp_bd, 
            'response_bd': res_bd,
            'request_url': req_url,
            'request_method': req_met,
            'request_bd': req_bd
            }

def assert_equal(r, exp_body, exp_sc, req_body=None):
    try:
        if r.status_code != exp_sc:
            return ret_format(ErrorCodes.RC_ERROR, exp_sc, r.status_code, exp_body, get_json(r), r.request.url, r.request.method, req_body)
        if get_json(r) != exp_body:
            return ret_format(ErrorCodes.BODY_ERROR, exp_sc, r.status_code, exp_body, get_json(r), r.request.url, r.request.method, req_body)
        return ret_format(ErrorCodes.OK, exp_sc, r.status_code, exp_body, get_json(r), r.request.url, r.request.method, req_body)
    except ValueError:
        print(r)
        return ret_format(ErrorCodes.INT_ERROR, None, None, None, None, None, None, None)

class TestEndpoints():
    def __init__(self, baseurl):
        self.baseurl=baseurl
        self.vars={}
        with open('tests.yaml') as f:
            self.config=yaml.load(f, Loader=yaml.Loader)
            
    def get_test_name(self):
        rv=''
        for api in self.config:
            rv+=f"{api['api_name']} " if 'api_name' in api.keys() else ''
        return rv

    def validate_apis(self):
        rv={}
        for api in self.config:
            rv[api['api_name']]=self.execute_tests(api['tests'])
        return rv

    def update_vars(self, template, obj):
        if template is None or obj is None:
            return
        if type(template) == str:
            #print(f'looking for string: {template}')
            m = re.search('\{\{(\w+)\}\}', template)
            #print('re.search()->', m)
            if m:
                varname=m.groups()[0]
                if varname not in self.vars.keys():
                    self.vars[varname]=obj
                    print(f'update_vars([{varname}]={obj})')
        elif type(template) == dict:
            for k in template.keys():
                try: self.update_vars(template[k], obj[k])
                except: pass
 
    def update_body(self, body):
        #print(f'update_body()-> {body} [{type(body)}]')
        if body is None:
            return
        if type(body) == str:
            body_vars = re.findall('\{\{(\w+)\}\}', body)
            for v in body_vars:
                var = self.vars[v] if v in self.vars.keys() else ''
                body = re.sub('\{\{%s\}\}'%v, var, body)
        if type(body) == dict:
            for k in body.keys():
                body[k]=self.update_body(body[k])
        if type(body) == list:
            body=[self.update_body(item) for item in body]
        return body
            
     
    def execute_tests(self, tests):
        rv={}
        for t in tests:
            rv[t['title']]=self.execute_test(t)
            print(f'{t["title"]} -> {ErrorCodes.get_error(rv[t["title"]]["error"])}')
        return rv

    def execute_test(self, t):
        t['exp_body']= None if 'exp_body' not in t.keys() else json_parse(t['exp_body'])
        t['body']= None if 'body' not in t.keys() else json_parse(t['body'])
        # de-reference vars
        t['body']=self.update_body(t['body'])
        t['url']=self.update_body(t['url'])
        r=None
        if 'exp_body' not in t.keys():
            print('missing exp_body')
            t['exp_body']=None
        if t['method']=='GET':
            r=requests.get(self.baseurl+t['url'])
        elif t['method']=='POST':
            r=requests.post(self.baseurl+t['url'], json=t['body'])
        elif t['method']=='PUT':
            r=requests.put(self.baseurl+t['url'], json=t['body'])
        elif t['method']=='DELETE':
            r=requests.delete(self.baseurl+t['url'])
        if r.status_code >=200 and r.status_code <300:
            #print(r)
            #print(r.request)
            #print(r.request.url)
            #print(r.request.body)
            #print(r.content)
            self.update_vars(t['exp_body'], get_json(r))
        t['exp_body']=self.update_body(t['exp_body'])
        rv = assert_equal(r, t['exp_body'], t['exp_rc'], req_body=t['body'])
        return rv

def json_parse(s):
    if s.strip().startswith('{') or s.strip().startswith('['):
        return json.loads(s)
    else:
        return s

if __name__ == "__main__":
    # test = TestEndpoints('https://[YOUR_PROJECT_ID].appspot.com')
    test = TestEndpoints('http://localhost:8080')        
    #test = TestEndpoints('https://sac230116rl.nw.r.appspot.com')        
    pprint(test.validate_apis())
    
