from twitter_api import update_banner
from glob import glob
from random import randint

files=glob('./images/*')#imagesフォルダ内の画像をランダムに選択してバナーに設定する

select=files[randint(0,len(files)-1)]

update_banner(select)
print(select)