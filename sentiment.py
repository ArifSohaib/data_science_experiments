import tweepy
from textblob import TextBlob
import csv
#custom file to store api keys secretly and off the public repository
import access_api

def get_api_access():
    """
    gets an authenticated twitter api accessor object
    Returns:
        api: authenticated twitter api accessor object
    """
    consumer_key = access_api.consumer_key
    consuimer_secret = access_api.consuimer_secret

    access_token = access_api.access_token
    access_token_secret = access_api.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consuimer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api



def check_classifier(api,topic):
    '''
    prints out tweets and their sentiments based on bag of words model
    Args:
        api: the authenticated twitter api accessor object
        topic: the string to search for
    '''
    public_tweets = api.search(topic)

    for tweet in public_tweets:
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        print("polarity: {}".format(analysis.sentiment.polarity))
        print("subjectivity: {}".format(analysis.sentiment.subjectivity))
        print()

def make_csv(api, topic):
    public_tweets = api.search(topic)
    with open('tweet_sentiment.csv', 'w',newline='\n') as  f:
        fieldnames = ['tweet', 'sentiment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for tweet in public_tweets:
            analysis = TextBlob(tweet.text)
            polarity = 'Positive'
            if(analysis.sentiment.polarity < 0):
                polarity = 'Negative'
            writer.writerow({fieldnames[0]:tweet.text, fieldnames[1]:polarity})


def main():
    api = get_api_access()
    # check_classifier(api,'XKCD')
    make_csv(api, 'XKCD')

if __name__ == '__main__':
    main()
