import requests

url="https://exam-240222.nw.r.appspot.com/api/v1"

body = {
            'nome': 'Mario',
            'cognome': 'Rossi',
            'cap': 41125
        }

print("GET: "+url+"/clean")
resp = requests.get(url+'/clean')
print(str(resp) + ":" + resp.text)
print('\n\n')

print("POST: "+url+"/umarell/0\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/0', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')

body = {
            'nome': 'Valter',
            'cognome': 'Ometti',
            'cap': 41121
        }
print("POST: "+url+"/umarell/0\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/0', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')

body = {
            'nome': 'Valter',
            'surname': 'Ometti',
            'cap': 41121
        }
print("POST: "+url+"/umarell/7\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/7', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')

body = {
            '12': 'Valter',
            'cognome': 'Ometti',
            'cap': 41121
        }
print("POST: "+url+"/umarell/7\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/7', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')

body = {
            'nome': 'Valter',
            'cognome': 'Ometti',
            'cap': 41121
        }
print("POST: "+url+"/umarell/7\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/7', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')

body = {
            'nome': 'Ernesto',
            'cognome': 'Guardalocchi',
            'cap': 212.43
        }
print("POST: "+url+"/umarell/3\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/3', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')

body = {
            'nome': 'Ernesto',
            'cognome': 'Guardalocchi',
            'cap': 42122
        }
print("POST: "+url+"/umarell/3\nBODY: "+ str(body))
resp = requests.post(url+'/umarell/3', json= body)
print(str(resp) + ":" + resp.text)
print('\n\n')


print("GET: "+url+"/umarell/3")
resp = requests.get(url+'/umarell/3')
print(str(resp) + ":" + resp.text)
print('\n\n')

print("GET: "+url+"/umarell/0")
resp = requests.get(url+'/umarell/0')
print(str(resp) + ":" + resp.text)
print('\n\n')

print("GET: "+url+"/umarell/7")
resp = requests.get(url+'/umarell/7')
print(str(resp) + ":" + resp.text)
print('\n\n')

print("GET: "+url+"/umarell/123")
resp = requests.get(url+'/umarell/123')
print(str(resp) + ":" + resp.text)
print('\n\n')

print("GET: "+url+"/umarell/sciascemo")
resp = requests.get(url+'/umarell/ciaoscemo')
print(str(resp) + ":" + resp.text)
print('\n\n')