#!/usr/bin/env python3
"""
御供養ボット - Twitter自動投稿スクリプト

X API v2 (POST /2/tweets) + OAuth 1.0a User Auth
tweepy不使用。requests + requests-oauthlib で直接呼び出す。

A/Bテスト方式:
- slot 0 (朝): format=A の短文投稿をローテーション
- slot 1 (夜): format=B の長文投稿をローテーション
"""

import json
import os
import sys
from datetime import date

import requests
from requests_oauthlib import OAuth1


TWEET_URL = "https://api.twitter.com/2/tweets"


def load_content(filepath: str) -> dict:
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def build_tweet_map(data: dict) -> dict:
    tweet_map = {}
    for genre_tweets in data["genres"].values():
        for tweet in genre_tweets:
            tweet_map[tweet["id"]] = tweet["text"]
    return tweet_map


def select_tweet(data: dict, slot: int) -> str:
    format_key = "A" if slot == 0 else "B"
    tweet_ids = data["tweet_sets"][format_key]
    tweet_map = build_tweet_map(data)
    today = date.today().toordinal()
    index = today % len(tweet_ids)
    return tweet_map[tweet_ids[index]]


def post_tweet(text: str) -> None:
    # 認証情報の存在確認
    keys = ["TWITTER_API_KEY", "TWITTER_API_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET"]
    for k in keys:
        v = os.environ.get(k, "")
        print(f"{k}: {'SET (' + str(len(v)) + ' chars)' if v else 'MISSING'}")

    auth = OAuth1(
        os.environ["TWITTER_API_KEY"],
        os.environ["TWITTER_API_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    print(f"投稿テキスト ({len(text)} chars):\n{text[:100]}...")
    response = requests.post(TWEET_URL, auth=auth, json={"text": text})
    print(f"HTTP {response.status_code}")
    print(f"Response: {response.text}")
    if not response.ok:
        # GitHub Actions Annotation にエラーを表示
        print(f"::error::Twitter API Error {response.status_code}: {response.text}")
        sys.exit(1)
    data = response.json()
    print(f"投稿成功: tweet_id={data['data']['id']}")


def main() -> None:
    slot = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_path = os.path.join(script_dir, "..", "tweets", "content.json")
    data = load_content(content_path)
    text = select_tweet(data, slot)
    post_tweet(text)


if __name__ == "__main__":
    main()
