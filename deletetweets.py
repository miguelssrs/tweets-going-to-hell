#!/usr/bin/env python

import argparse
from backports import csv
import sys
import time
import os
import twitter
import io
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.1.1"

def delete(api, date, r):
    with io.open("tweets.csv", encoding='utf-8') as file:
        count = 0

        for row in csv.DictReader(file):
            tweet_id = int(row["tweet_id"])
            tweet_date = parse(row["timestamp"], ignoretz=True).date()

            if date != "" and tweet_date >= parse(date).date():
                continue

            if (r == "retweet" and row["retweeted_status_id"] == "" or
                    r == "reply" and row["in_reply_to_status_id"] == ""):
                continue

            try:
                print("Deleting tweet #{0} ({1})".format(tweet_id, tweet_date))

                api.DestroyStatus(tweet_id)
                count += 1
                time.sleep(0.5)

            except twitter.TwitterError as err:
                print("Exception: %s\n" % err.message)

    print("Number of deleted tweets: %s\n" % count)

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")

    args = parser.parse_args()

    api = twitter.Api(consumer_key="YOUR_CONSUMER_KEY_HERE",
                      consumer_secret="YOUR_CONSUMER_SECRET_KEY_HERE",
                      access_token_key="YOUR_ACCESS_TOKEN_KEY",
                      access_token_secret="YOUR_ACCESS_SECRET_TOKEN_HERE")

    delete(api, args.date, args.restrict)


if __name__ == "__main__":
    main()