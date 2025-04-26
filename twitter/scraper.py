# # twitter/scraper.py


# import snscrape.modules.twitter as sntwitter

# # Initialize an empty list to store tweet data
# tweets = []

# # Scraping the last 5 tweets from user 'nasa'
# for i, tweet in enumerate(sntwitter.TwitterUserScraper('nasa').get_items()):
#     if i >= 5:
#         break
#     tweets.append({
#         'username': tweet.user.username,
#         'text': tweet.content,
#         'created_at': tweet.date,
#         'likes': tweet.likeCount,
#         'retweets': tweet.retweetCount,
#         'url': tweet.url
#     })

# # Print the tweets
# for t in tweets:
#     print(f"{t['username']} tweeted at {t['created_at']}")
#     print(t['text'])
#     print(f"❤️ {t['likes']} | 🔁 {t['retweets']}")
#     print(f"🔗 {t['url']}")
#     print('-' * 50)
