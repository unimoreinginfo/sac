#!/usr/bin/python3
import re

message='This is a #message with the following topics: #hashtag1, #hashtag2. \nDo you like it? #iparsehashtags#iremoveduplicates, #hashtag1\na line with no hashtags!'

def get_hashtags(msg: str) -> list:
    return list(dict.fromkeys(re.findall('#(\w+)', msg)))
    
if __name__ == '__main__':
    print(get_hashtags(message))
