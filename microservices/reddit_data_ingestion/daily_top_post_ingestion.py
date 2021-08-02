# Importing Velkozz APIs:
from vdeveloper_api.velkozz_pipelines.social_media_pipelines.reddit_pipelines import RedditContentPipeline

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
config.read(".reddit.env")

# Extracting config params:
test_schedule_stat = config["velkozz_account"]["TEST_SCHEDULE"]
web_api_url = config["velkozz_account"]["VELKOZZ_API_URL"]

logger_host = config["velkozz_logger_config"]["LOGGER_HOST"]
logger_url = config["velkozz_logger_config"]["LOGGER_URL"]

subreddit_lst_file = "reddit_ingestion.txt"

print(f"Reddit Ingestion Script Active: \n -Test Scheduler: {test_schedule_stat} \n -url:{web_api_url} \n -Subreddit List Path: {subreddit_lst_file}")  

# Opening reddit_ingestion.txt file for list of subreddits:
with open(subreddit_lst_file) as json_file:
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
            VELKOZZ_API_URL = config["velkozz_account"]["VELKOZZ_API_URL"],
            token = config["velkozz_account"]["VELKOZZ_TOKEN"],
            LOGGER_HOST=logger_host,
            LOGGER_URL=logger_url)
        # Sleeping to avoid overloading the REST API:
        time.sleep(10)


# Adding the main function to the Scheduler:
# Config for rapid development testing:
if test_schedule_stat == "True": # Boolean read from file is string. Too lazy to convert and deal w/ string2bool.
    print("Job added with Test Scheduler")
    reddit_scheduler.add_job(write_subreddit_data, "interval", minutes=2)
else:
    print("Job added with Production Scheduler")
    reddit_scheduler.add_job(write_subreddit_data, "interval", hours=12)

reddit_scheduler.start()
