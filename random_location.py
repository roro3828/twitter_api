from twitter_api import update_user_profile
from random import randint,triangular, uniform

latitude=str(triangular(-180.000000,180.000000,0.0))
longitude=str(uniform(-90.000000,90.000000))
update_user_profile(location=longitude+','+latitude)