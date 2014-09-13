# -*- coding: utf-8 -*-
import os
import pyowm
import tweepy

owm = pyowm.OWM(os.environ['APPID'])
auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
twttr = tweepy.API(auth)

def mps_to_kms(mps):
    return int(mps / 0.621371)

class MyStream(tweepy.StreamListener):
    def on_connect(self):
        print "* Connexion à la timeline"

    def answer(self, tweet, string):
        try:
            twttr.update_status(status=string,
                                in_reply_to_status_id=tweet.id)
        except tweepy.TweepError:
            print "Could not send tweet '{}'".format(string)

    def on_status(self, tweet):
        if tweet.user.screen_name == "QuelTempsFaitIl":
            return # On ignore nos propre tweet

        try:
            city = tweet.entities["hashtags"][0]["text"]
            print tweet.text
        except IndexError:
            pass # Le tweet ne contient pas de hashtag
        else:
            observation = owm.weather_at_place(str(city))
            w = observation.get_weather()
            self.answer(tweet, "@{} Il fait {}° avec {}% d'humidité et {} km/s de vent à #{}"
                        .format(tweet.user.screen_name,
                                w.get_temperature('celsius')["temp"],
                                w.get_humidity(),
                                mps_to_kms(w.get_wind()["speed"]),
                                str(city)))
    def on_error(self, code):
        return True

def main():
    stream = tweepy.Stream(auth, MyStream(), timeout=50)
    try:
        stream.userstream()
    except KeyboardInterrupt:
        print "* Déconnexion"

if __name__ == "__main__":
    main()
