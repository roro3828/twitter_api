from twitter_api import *

def main():
    print('ツイート内容を入力')
    text=input('>>').replace('\\n','\n')#\nを改行コードにする

    print('返信する場合id入力')
    id=input('>>')

    if id=='':
        id=None

    send_tweet(text,reply_id=id)

main()