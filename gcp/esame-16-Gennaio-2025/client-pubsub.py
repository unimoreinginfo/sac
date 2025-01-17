import argparse
from google.cloud import pubsub_v1
from uuid import uuid1
import json

parser = argparse.ArgumentParser()
parser.add_argument('topic', type=str)
parser.add_argument('email', type=str)
args = parser.parse_args()
topic=args.topic
email=args.email
print(topic)

def callback(message):
    msg = message.data.decode('utf-8')
    if 'Risposta: ' in msg:
        if email in msg:
            message.ack()
            print(msg)
            
    
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='uaas070120252',
    topic=topic,  
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id='uaas070120252',
    sub=f'sac-sub-{uuid1()}',
)

with pubsub_v1.SubscriberClient() as subscriber:
    subscriber.create_subscription(
        name=subscription_name,
        topic=topic_name
    )
    print(f"listening on {topic}")
    publisher = pubsub_v1.PublisherClient()
    message = f'Richiesta: {email}'
    publisher.publish(topic_name, json.dumps(message).encode('utf-8'))
    fut = subscriber.subscribe(subscription_name, callback)
    try:
        fut.result()
    except:
        fut.cancel()