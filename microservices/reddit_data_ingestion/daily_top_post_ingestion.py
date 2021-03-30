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

print("Running Subreddt Data Ingestion for the Following Subreddits:", subreddits)

# Function that writes all data to the database:
def write_subreddit_data():
    for subreddit in subreddits:
        RedditContentPipeline(
            subreddit,
            CLIENT_ID = config["praw_params"]["CLIENT_ID"],
            CLIENT_SECRET = config["praw_params"]["CLIENT_SECRET"],
            USER_AGENT = config["praw_params"]["USER_AGENT"],
            token = config["velkozz_account"]["VELKOZZ_TOKEN"]
        )
        # Sleeping to avoid overloading the REST API:
        time.sleep(5)


# Adding the main function to the Scheduler:
reddit_scheduler.add_job(write_subreddit_data, "interval", minutes=5)

reddit_scheduler.start()