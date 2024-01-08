import argparse
from google.cloud import pubsub_v1
from uuid import uuid1

def callback(message):
    print(message.data)
    message.ack()

parser = argparse.ArgumentParser()
parser.add_argument('hashtag', type=str)
args = parser.parse_args()
hashtag = args.hashtag.split('#')[1]

topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='sac-emilianomaccaferri',
    topic=hashtag,  
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id='sac-emilianomaccaferri',
    sub=f'sac-sub-{uuid1()}',
)

with pubsub_v1.SubscriberClient() as subscriber:
    subscriber.create_subscription(
        name=subscription_name,
        topic=topic_name
    )
    print(f"listening on {hashtag}")
    fut = subscriber.subscribe(subscription_name, callback)
    try:
        fut.result()
    except KeyboardInterrupt:
        fut.cancel()
