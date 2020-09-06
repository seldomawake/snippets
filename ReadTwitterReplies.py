import csv
import tweepy
from Twitter_Credentials import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
with open('replies.csv', 'w', encoding="utf-8") as csvfile:
        w = csv.writer(csvfile, delimiter='|')
        for row in tweepy.Cursor(api.search, q="to:domm, since_id:1302272984661422082").items(500):
            w.writerow([row.author.screen_name, row.in_reply_to_status_id, row.text.replace("\n", "")])
