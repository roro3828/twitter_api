from twitter_api import update_icon
from glob import glob
from random import randint

files=glob('./images/*')#imagesフォルダ内の画像をランダムに選択する

select=files[randint(0,len(files))]

update_icon(select)