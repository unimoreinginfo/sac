#!/usr/bin/python3
import os
import json
import datetime
from google.cloud import pubsub_v1
from sys import argv
project_id = 'umarellasservice'
subscription_name='ISCRIZIONE'

cap = None
def callback(message):
    print("ricevuto qualcosa")
    message.ack()
    msg = message.data.decode('utf-8')
    if cap is not None:
       filter = 'CAP: ' + str(cap)
       if str(filter) in msg:
           print(msg)
    else:
        print(msg)
    ### here we can apply our filtering like if str(value) in msg
    
 

if __name__=='__main__':    
    #### Argument checks this is an example with cap
    if len(argv)>1:
        try:
            cap = int(argv[1])
            if cap < 0 or cap > 99999:
                print("Argument error. Usage is:\n./"+argv[0]+" {int_value"+"}\nint_value must be in range(0,99999) (inclusive)")
        except:
            print("Argument error. Usage is:\n./"+argv[0]+" {int_value"+"}\nint_value must be in range(0,99999) (inclusive)")
            quit()
    
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    pull = subscriber.subscribe(subscription_path, callback=callback)
    try:
        pull.result()
    except Exception as e:
        print(e)
        pull.cancel()
