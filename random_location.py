from twitter_api import update_user_profile
from random import triangular, uniform

latitude=str(uniform(-180.000000,180.000000))
longitude=str(triangular(-90.000000,90.000000,0.0))
update_user_profile(location=longitude+','+latitude)