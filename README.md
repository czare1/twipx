Twipx
====================

TWItter stream ProXy based on Tornad server.

Installation
-------
* Clone source
* Prepare virtualenv
* Install requirements
* Run the server with command:

```
python -m twipx.tweetwatcher
```


Sample client
-------

```python
#coding: utf-8

from tornado.ioloop import IOLoop
from tweetstream import TweetStream

auth_configuration = {
    "twitter_consumer_key": "A",
    "twitter_consumer_secret": "B",
    "twitter_access_token": "C",
    "twitter_access_token_secret": "D",
    "twitter_stream_host": "localhost",
    "twitter_stream_scheme": "http",
    "twitter_stream_port": 9000
}

ioloop = IOLoop.instance()
stream = TweetStream(auth_configuration, ioloop=ioloop)
def tweet_callback(message):
    """ Publish message """
    print message
# open sample stream
stream.fetch('/1/statuses/filter.json?track=apple', callback=tweet_callback)
ioloop.start()
```

Known issues
-------
* It does only handle GET requests
* It does not authenticate clients (each connection is authenticated)
* It does not handle errors
* No closing of clients connections

