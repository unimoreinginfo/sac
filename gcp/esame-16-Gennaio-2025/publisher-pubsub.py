from google.cloud import pubsub_v1
import json
import requests
import os
from utils import email_validate

project_id = os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys() else 'uaas070120252'
topic = os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'secretsanta'
sub = 'req'
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = f'projects/{project_id}/topics/{topic}'
subsciption_name = f'projects/{project_id}/subscriptions/{sub}'

def send_message(message):
    msg = message.data.decode('utf-8')
    if 'Richiesta: ' in msg:
        email = msg.replace('Richiesta: ', '').replace('"', '')

        print(msg)
        if email_validate(email):
            r2 = requests.get(f'https://uaas070120252.nw.r.appspot.com/api/v1/santa/{email}')

            if r2.status_code == 200:
                content = r2.json()
                name = content['fromFirstName']
                destN = content['toFirstName']
                destS = content['toLastName']
                destE = content['toEmail']
                message_p = f'Risposta: Ehi {name} - {email} devi fare il regalo a {destN} {destS} <{destE}>'
                publisher.publish(topic_path, json.dumps(message_p).encode('utf-8'))

            else: 
                message_p = f'Risposta: Ehi {name}, sembra che ci sia stato un problema'
                publisher.publish(topic_path, json.dumps(message_p).encode('utf-8'))
        else:
            message_p = f'Risposta: La mail {email} non e valida (Uso protocollo: Richiesta: <email>)'
            publisher.publish(topic_path, json.dumps(message_p).encode('utf-8'))
        
        message.ack()

if __name__ == '__main__':
    fut = subscriber.subscribe(subsciption_name, send_message)
    print('Aspetto richieste')
    try:
        fut.result()
    except KeyboardInterrupt:
        fut.cancel()