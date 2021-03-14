import os
from time import sleep
from requests_oauthlib import OAuth1Session
import json
import twitter_key#キー読み込み

import base64

ACCESS_TOKEN=twitter_key.access_token
ACCESS_TOKEN_SECRET=twitter_key.access_token_secret

CONSUMER_KEY=twitter_key.consumer_key
CONSUMER_SECRET=twitter_key.consumer_secret


def oath():
    return OAuth1Session(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

def search_tweets(text):#ツイートを検索
    url='https://api.twitter.com/2/tweets/search/recent?'

    params={'query':text,'max_results':10,'tweet.fields':'created_at'}

    response=oath().get(url,params=params)

    return json.loads(response.text)

def search_tweets_old(text):
    url='https://api.twitter.com/1.1/search/tweets.json'

    params={'q':text,'count':10}

    response=oath().get(url,params=params)

    return json.loads(response.text)

def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())

    return data.decode('utf-8')

def split_list(li:list,n=4):#リストをn個ずつの要素に分ける
    lists=[]
    for i in range(0,len(li),n):
        lists.append(li[i:i+n])
    return lists


def send_tweet(text,reply_id=None,media_id=None,place_id=None,attachment_url=None):#ツイートする
    url='https://api.twitter.com/1.1/statuses/update.json'
    params={'status':text}

    if reply_id!=None:
        params.setdefault('in_reply_to_status_id',reply_id)
        params.setdefault('auto_populate_reply_metadata','true')

    if media_id!=None:
        if type(media_id)==list:
            if len(media_id)<=4:
                media_ids=','.join(map(str,media_id))

            else:
                media_ids=','.join(map(str,media_id[:3]))

            params.setdefault('media_ids',media_ids)
        else:
            params.setdefault('media_ids',str(media_id))

    if place_id!=None:
        params.setdefault('place_id',place_id)

    if attachment_url!=None:
        params.setdefault('attachment_url',attachment_url)

    response=oath().post(url,params)

    response_json=json.loads(response.text)

    return response_json

def upload_media(path,return_id=True):#画像をアップロード
    url='https://upload.twitter.com/1.1/media/upload.json'

    media=image_file_to_base64(path)

    params={'media_data':media}

    response=oath().post(url,params)

    response_json=json.loads(response.text)

    if return_id:
        return response_json['media_id']
    else:
        return response_json

def create_favo(id,destroy=False):#いいねする
    if destroy:
        url='https://api.twitter.com/1.1/favorites/destroy.json'
    else:
        url='https://api.twitter.com/1.1/favorites/create.json'

    params={'id':id}

    response=oath().post(url,params)

    response_json=json.loads(response.text)

    return response_json

def destroy_tweet(id):#ツイートを削除
    url='https://api.twitter.com/1.1/statuses/destroy/'

    params=str(id)+'.json'

    response=oath().post(url+params)

    response_json=json.loads(response.text)

    return response_json

def tweet_lookup(id):#ツイートを取得
    url='https://api.twitter.com/2/tweets'

    params={'tweet.fields':'created_at,public_metrics,source,entities,geo','user.fields':'username','expansions':'author_id'}
    #params={'tweet.fields':'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld'}

    if type(id)==list:
        params.setdefault('ids',id)
    else:
        params.setdefault('ids',[id])

    response=oath().get(url,params=params)

    response_json=json.loads(response.text)

    return response_json

def timeline(count=5):
    url='https://api.twitter.com/1.1/statuses/home_timeline.json'

    params={'tweet.fields':'created_at','expansions':'author_id','count':count}

    response=oath().get(url,params=params)

    response_json=json.loads(response.text)

    return response_json

def user_timeline(user,count=5):
    url='https://api.twitter.com/1.1/statuses/user_timeline.json'

    params={'user_id':user,'tweet.fields':'created_at','count':count}

    response=oath().get(url,params=params)

    return json.loads(response.text)

def get_place_information(id):
    url='https://api.twitter.com/1.1/geo/id/'+str(id)+'.json'

    response=oath().get(url)

    return json.loads(response.text)

def retweet(id,unretweet=False):
    if unretweet:
        url='https://api.twitter.com/1.1/statuses/unretweet/'+str(id)+'.json'
    else:
        url='https://api.twitter.com/1.1/statuses/retweet/'+str(id)+'.json'

    response=oath().post(url)

    return json.loads(response.text)

def follow(id,destroy=False):
    if destroy:
        url='https://api.twitter.com/1.1/friendships/destroy.json'
    else:
        url='https://api.twitter.com/1.1/friendships/create.json'

    params={'user_id':id}

    response=oath().post(url,params)

    return json.loads(response.text)

def update_banner(path=None):
    if path==None:
        url='https://api.twitter.com/1.1/account/remove_profile_banner.json'
        oath().post(url)

    else:
        url='https://api.twitter.com/1.1/account/update_profile_banner.json'
        banner=image_file_to_base64(path)
        params={'banner':banner}
        oath().post(url,params)

def update_icon(path):
    url='https://api.twitter.com/1.1/account/update_profile_image.json'

    icon=image_file_to_base64(path)

    params={'image':icon,'skip_status':'true'}

    oath().post(url,params)

def update_user_profile(name=None,url=None,location=None,description=None):#ユーザーのプロファイル変更
    resource_url='https://api.twitter.com/1.1/account/update_profile.json'

    params={}

    if name!=None:
        params.setdefault('name',name)
    if url!=None:
        params.setdefault('url',url)
    if location!=None:
        params.setdefault('location',location)
    if description!=None:
        params.setdefault('description',description)
    
    if params!={}:
        response=oath().post(resource_url,params)
        return json.loads(response.text)

def twitter_upload_status(media_id):
    url='https://upload.twitter.com/1.1/media/upload.json'
    get_status={'command':'STATUS','media_id':media_id}
    response=oath().get(url,params=get_status).text
    return json.loads(response)


def upload_media_INIT(path):
    file_size=os.path.getsize(path)#ファイルのサイズ取得 byte
    media_type='video/mp4'

    url='https://upload.twitter.com/1.1/media/upload.json'

    params_init={'command':'INIT','total_bytes':file_size,'media_category': 'tweet_video'}

    response_init=json.loads(oath().post(url,params_init).text)
    media_id=response_init['media_id']

    sent_byte=0
    index=0
    file=open(path,'rb')
    while sent_byte<file_size:
        media=file.read(4194304)#4MB読み込む

        params_append={'command':'APPEND','media_id':media_id,'segment_index':index}

        files={'media':media}

        oath().post(url,data=params_append,files=files)

        index=index+1
        sent_byte=file.tell()
        print(str(file_size)+'中'+str(sent_byte)+'アップロード完了')

    print('完了')

    params_finalize={'command':'FINALIZE','media_id':media_id}

    response_finalize=oath().post(url,params_finalize)

    response=json.loads(response_finalize.text)

    status=twitter_upload_status(response['media_id'])

    while status['processing_info']['state']=='in_progress':
        print(str(status['processing_info']['progress_percent'])+'%処理済み')
        sleep(5)
        status=twitter_upload_status(response['media_id'])

    return response