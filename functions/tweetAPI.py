import tweepy
from tweepy import OAuthHandler

ACCESS_TOKEN = '1089991871634595842-M7Wj4WZ8JdT3VqsOqsLeDEYlzH5Aj7'
ACCESS_SECRET = 'MjeEMYaIR9oineTPDyFR7CSLhlSAW5q4cf10y1SPLLS4M'
CONSUMER_KEY = 'ldaCRtaZbnTyFPKzs1mmrbqZv'
CONSUMER_SECRET = 'w57Gc80WS2d8PijSeXu8GvEWI1VQ6yHmRBWMn8V2ZrTZKmr9jQ'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)
depression_tweets=[]
MAX_TWEETS = 500000000
# %23notjustsad / selbstmordgedanken/ freude/ positive Energie/ glücklichkeit
for tweet in tweepy.Cursor(api.search,q="#suizidgedanken",count=100,lang="de").items(limit=MAX_TWEETS):

    print(tweet.created_at, tweet.text)
    depression_tweets.append(tweet.text)
    #csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
#tweets = api.search(q='#notjustsad')
#print("tweets are: ",tweets)
print("tweet 76:",depression_tweets[0])
print("tweets length:", len(depression_tweets))
#print("type of tweets",type(tweets))