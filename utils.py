from flask import current_app
import twitter
from pytz import timezone
from datetime import datetime
import os
from PIL import Image

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


twitter_api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                  consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=TWITTER_ACCESS_TOKEN,
                  access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)


class Twitter:

    def __init__(self, handle):
        self.tweet = twitter_api.GetUserTimeline(screen_name=handle, count=1)
        self.twitdict = [i.AsDict() for i in self.tweet]
        self.user = self.twitdict[0]['user']['name']
        self.text = self.twitdict[0]['text']
        self.time = self.twitdict[0]['created_at']
        self.utc = timezone('UTC')
        self.est = timezone('US/Eastern')
        self.convert = self.time_convert()

    def time_convert(self):
        created_at = datetime.strptime(self.time, '%a %b %d %H:%M:%S +0000 %Y')
        utc_created_at = self.utc.localize(created_at)
        est_created_at = utc_created_at.astimezone(self.est)
        format_est = est_created_at.strftime('%b %d %Y at %I:%M EST')
        return format_est

    def format(self):
        tweet = self.user + ": " + self.text + " (" + self.convert + ")"
        return tweet


def save_picture(form_picture, name):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = 'image_' + name + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/menu/', picture_fn)

    if os.path.isfile(picture_path):
        os.remove(picture_path)

    i = Image.open(form_picture)

    return i.save(picture_path)








