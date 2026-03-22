#!/usr/bin/env python3
"""
御供養ボット - Twitter自動投稿スクリプト

ジャンル別ローテーション方式:
- 1日2回投稿（朝・夜）
- 6ジャンルを日付ベースで順番に切り替え
- 各ジャンル内はツイート番号でローテーション
"""

import json
import os
import sys
from datetime import date, timezone, timedelta

import tweepy


def load_tweets(filepath: str) -> dict:
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def select_tweet(data: dict, slot: int) -> str:
    """
    投稿するツイートを選択する。

    選択ロジック:
      - slot: 0=朝, 1=夜
      - JST日付の通算日数でジャンルとツイートをローテーション

    ジャンルインデックス = (通算日数 * 2 + slot) // tweets_per_genre % genre_count
    ツイートインデックス = (通算日数 * 2 + slot) % tweets_per_genre
    """
    genre_order = data["genre_order"]
    genres = data["genres"]

    # 全ジャンルのツイート数（最小値で揃える）
    tweets_per_genre = min(len(genres[g]) for g in genre_order)
    genre_count = len(genre_order)

    jst = timezone(timedelta(hours=9))
    today = date.today().toordinal()
    tick = today * 2 + slot

    genre_name = genre_order[(tick // tweets_per_genre) % genre_count]
    tweet_index = tick % tweets_per_genre

    tweet = genres[genre_name][tweet_index]
    return tweet["text"]


def post_tweet(text: str) -> None:
    client = tweepy.Client(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=text)
    print(f"投稿成功: tweet_id={response.data['id']}")
    print(f"内容: {text}")


def main() -> None:
    slot_arg = sys.argv[1] if len(sys.argv) > 1 else "0"
    slot = int(slot_arg)  # 0=朝, 1=夜

    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_path = os.path.join(script_dir, "..", "tweets", "content.json")

    data = load_tweets(content_path)
    text = select_tweet(data, slot)
    post_tweet(text)


if __name__ == "__main__":
    main()
