import praw
from confluent_kafka import Producer

from config import praw_reddit_parameters
from constants import producer_config, reddit_topic

reddit_producer = Producer(producer_config)

reddit = praw.Reddit(**praw_reddit_parameters)

subreddit = reddit.subreddit('askreddit')

for comment in subreddit.stream.comments():
    reddit_producer.produce(reddit_topic, value=comment.body)

reddit_producer.flush()
