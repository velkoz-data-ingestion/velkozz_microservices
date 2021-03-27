# Importing Velkozz APIs:
from social_media_pipelines.reddit_pipelines import RedditContentPipeline    

# Importing Scheduling packages:
import time
import datetime
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

# Import data managment packages:
from dotenv import load_dotenv, dotenv_values
import json
import configparser

# Scheduler initaliztion:
reddit_scheduler = BlockingScheduler()

# Specific Reddit Ingestion dotenv params:
config = configparser.ConfigParser()
config.read("../../service_configs/reddit_services/.reddit.env")

# Opening reddit_ingestion.txt file for list of subreddits:
with open("../../service_configs/reddit_services/reddit_ingestion.txt") as json_file:
    subreddits = json.load(json_file)

# Iterating over the list of subreddits provided and adding jobs to the scheduler:
for subreddit in subreddits:
    reddit_scheduler.add_job(
        RedditContentPipeline,
        "interval", 
        minutes=1,
        args=[subreddit],
        kwargs={
            "CLIENT_ID":config["praw_params"]["CLIENT_ID"],
            "CLIENT_SECRET":config["praw_params"]["CLIENT_SECRET"],
            "USER_AGENT":config["praw_params"]["USER_AGENT"],
            "token":config["velkozz_account"]["VELKOZZ_TOKEN"]
            }
        )

reddit_scheduler.start()