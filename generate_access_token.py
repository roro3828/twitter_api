import twitter_key
import twitter

def generate():
    return twitter.oauth_dance(twitter_key.name,twitter_key.consumer_key,twitter_key.consumer_secret,token_filename='./config.txt',open_browser=False)

print(generate())