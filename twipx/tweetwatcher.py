#coding: utf-8

from collections import defaultdict

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, asynchronous
from tweetstream import TweetStream

PORT_NR = 9000

class TwitProxy(object):
    """ Should be instantiated only once
    """
    STREAMS = {}
    CLIENTS = defaultdict(list)
    # singleton
    instance = None

    def __init__(self):
        self.auth_configuration = {
            "twitter_consumer_key": "dz01IVTOxtqgvkn4h9JA",
            "twitter_consumer_secret": "vm3aJ2YNJgnBfoCZpr3xhAVPjqHOW2r9QLQ5wGgXh8",
            "twitter_access_token": "259601779-v9gIUoCsdnaDsyLUpbK248ZMyIk8g7Y12OB4uBOa",
            "twitter_access_token_secret": "u66JnIR4tN0238plQdxDm5La0J6G2OU12PdnwrZSvhk"
        }
        self.ioloop = IOLoop.instance()
        self.start_http_server()
        TwitProxy.instance = self
        self.ioloop.start()

    def start_http_server(self):
        """ Creates instance ofg HttpServer listening to 
        clients connections
        """
        app = Application([
            (r"(.*)", PollHandler)
        ], debug=True)
        app.listen(PORT_NR)

    def ensure_stream(self, path):
        """ Opens stream connection if not already existing.
        """
        if path in self.STREAMS:
            return
        # create stream instance
        stream = TweetStream(self.auth_configuration, ioloop=self.ioloop)
        # prepare callback function (usage of closures)
        def tweet_callback(message):
            """ Publish message """
            for client_connection in self.CLIENTS[path]:
                client_connection.write_message(message)
        # open stream
        stream.fetch(path, callback=tweet_callback)
        # save stream
        self.STREAMS[path] = stream

    def subscribe_stream(self, stream_path, client):
        """ Appends client to the list of stream's subscribers
        """
        self.CLIENTS[stream_path].append(client)
        self.ensure_stream(stream_path)


class PollHandler(RequestHandler):
        @asynchronous
        def get(self, path):
            """ Handles client connection. Subscribes user to requested stream
            """
            TwitProxy.instance.subscribe_stream(self.request.uri, self)

        def write_message(self, message):
            """ Writes message to the client."""
            self.write(message)
            self.flush()


if __name__ == "__main__":
    TwitProxy()
