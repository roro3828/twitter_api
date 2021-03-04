import twitter_api
import glob

files=glob.glob('./images/*')
ids=[]
for i in files:
    a=twitter_api.upload_media(i)
    ids.append(a)

text=input()

twitter_api.send_tweet(text=text,media_id=ids)