# Importing Daily Youtube Channel Pipeline Object:
from vdeveloper_api.velkozz_pipelines.social_media_pipelines.youtube_pipelines import DailyYoutubeChannelStatsPipeline

# Importing Scheduling packages:
import time
import datetime
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

# Import data managment packages:
from dotenv import load_dotenv, dotenv_values
import json
import configparser
import pandas as pd

# Scheduler Initaliztion:
youtube_scheduler = BlockingScheduler()

# Loading config params:
config = configparser.ConfigParser()
config.read(".youtube.env")

# Loading Environmental Configuations for the Scheduler:
test_schedule_stat = config["velkozz_account"]["TEST_SCHEDULE"]
web_api_url = config["velkozz_account"]["VELKOZZ_API_URL"]
velkozz_token = config["velkozz_account"]["VELKOZZ_TOKEN"]

logger_host = config["velkozz_logger_config"]["LOGGER_HOST"]
logger_url = config["velkozz_logger_config"]["LOGGER_URL"]
google_api_key = config["google_api"]["GOOGLE_YOUTUBE_API_KEY"]

youtube_channel_csv = "youtube_channels.csv"

# Extracting the dict of youtube channels from the csv file:
youtube_channel_dict = pd.read_csv(youtube_channel_csv, header=0).to_dict("records")

print(f"Youtube Channel Data Ingestion Script Active: \n -Test Scheduler: {test_schedule_stat} \n -url:{web_api_url} \n -Google Youtube Accounts List Path: {youtube_channel_csv}")  
    
# Function that writes all data to the database:
def write_youtube_data():
    # Iterating over the youtube channels executing the pipeline:
    for channel in youtube_channel_dict:
        DailyYoutubeChannelStatsPipeline(
            VELKOZZ_API_URL = web_api_url,
            token = velkozz_token,
            LOGGER_HOST=logger_host,
            LOGGER_URL=logger_url,
            GOOGLE_API_KEY= google_api_key,
            CHANNEL_ID=channel["channel_id"],
            CHANNEL_NAME=channel["channel_name"]
        )
        time.sleep(15)

# Adding the main function to the Scheduler:
# Config for rapid development testing:
if test_schedule_stat == "True": # Boolean read from file is string. Too lazy to convert and deal w/ string2bool.
    print("Job added with Test Scheduler")
    youtube_scheduler.add_job(write_youtube_data, "interval", minutes=5)
else:
    print("Job added with Production Scheduler")
    youtube_scheduler.add_job(write_youtube_data, "interval", hours=6)

youtube_scheduler.start()


