#!/usr/bin/env python3
"""
御供養ボット - Twitter自動投稿スクリプト
v1.1 API (statuses/update) を使用
"""
import json
import os
import sys
from datetime import date, timezone, timedelta
import requests
from requests_oauthlib import OAuth1

def load_tweets(filepath: str) -> dict:
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def select_tweet(data: dict, slot: int) -> str:
    genre_order = data["genre_order"]
    genres = data["genres"]
    tweets_per_genre = min(len(genres[g]) for g in genre_order)
    genre_count = len(genre_order)
    today = date.today().toordinal()
    tick = today * 2 + slot
    genre_name = genre_order[(tick // tweets_per_genre) % genre_count]
    tweet_index = tick % tweets_per_genre
    tweet = genres[genre_name][tweet_index]
    return tweet["text"]

def post_tweet(text: str) -> None:
    auth = OAuth1(
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    url = "https://api.twitter.com/1.1/statuses/update.json"
    response = requests.post(url, auth=auth, data={"status": text})
    if response.status_code == 200:
        tweet_id = response.json()["id_str"]
        print(f"投稿成功: tweet_id={tweet_id}")
        print(f"内容: {text}")
    else:
        print(f"エラー: {response.status_code}")
        print(response.text)
        sys.exit(1)

def main() -> None:
    slot_arg = sys.argv[1] if len(sys.argv) > 1 else "0"
    slot = int(slot_arg)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_path = os.path.join(script_dir, "..", "tweets", "content.json")
    data = load_tweets(content_path)
    text = select_tweet(data, slot)
    post_tweet(text)

if __name__ == "__main__":
    main()
