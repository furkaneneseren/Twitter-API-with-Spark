import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import socket
import json
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()

consumer_key = os.getenv('api_key')
consumer_secret = os.getenv('api_key_secret')
access_token = os.getenv('access_token')
access_secret = os.getenv('access_token_secret')


class MyStreamListener(tweepy.StreamingClient):
    
  def on_connect(self):
        print("Connected")

  def on_tweet(self, tweet):
    # Displaying tweet in console
    if tweet.referenced_tweets == None:
        print(tweet.text)

  def on_data(self, data):
      try:
          msg = json.loads(data)
          print(msg['text'].encode('utf-8'))
          self.client_socket.send(msg['text'].encode('utf-8'))
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True


def sendData(c_socket):
    client = tweepy.Client(os.getenv('bearer_token'), os.getenv('api_key'), os.getenv('api_key_secret'), os.getenv('access_token'), os.getenv('access_token_secret'))
    auth = tweepy.OAuth1UserHandler(os.getenv('api_key'), os.getenv('api_key_secret'), os.getenv('access_token'), os.getenv('access_token_secret'))
    api = tweepy.API(auth)


    search_terms =  ["python", "programming", "coding"]
    stream = MyStreamListener(os.getenv('bearer_token'))

    for term in search_terms:
        stream.add_rules(tweepy.StreamRule(term))

   
    stream.filter(tweet_fields=["referenced_tweets"])

    """myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=['ether'])"""


if __name__ == "__main__":
    configure()
    s = socket.socket()         # Create a socket object
    host = "127.0.0.1"     # Get local machine name
    port = 5554                 # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port

    print("Listening on port: %s" % str(port))

    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.

    print( "Received request from: " + str( addr ) )

    sendData( c )
