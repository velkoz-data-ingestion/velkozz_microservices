# Importing Velkozz APIs:
from vdeveloper_api.velkozz_pipelines.structured_quant_data_pipelines.reddit_quant_pipeline import WSBTickerFrequencyPipeline

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
wsb_quant_scheduler = BlockingScheduler()

# Specific Reddit Ingestion dotenv params:
config = configparser.ConfigParser()
config.read(".quant.env")

# Extracting config params:
test_schedule_stat = config["velkozz_account"]["TEST_SCHEDULE"]
web_api_url = config["velkozz_account"]["VELKOZZ_API_URL"]

logger_host = config["velkozz_logger_config"]["LOGGER_HOST"]
logger_url = config["velkozz_logger_config"]["LOGGER_URL"]

print(f"WallstreetBets Frequency Ticker Counts Ingestion Script Active: \n -Test Scheduler: {test_schedule_stat} \n -url:{web_api_url}")

# Function that executes ETL pipeline job:
def write_wsb_freq_count():
    WSBTickerFrequencyPipeline(
        token=config["velkozz_account"]["TOKEN"],
        VELKOZZ_API_URL=web_api_url,
        LOGGER_HOST=logger_host,
        LOGGER_URL=logger_url)

# Adding the main function to the Scheduler:
# Config for rapid development testing:
if test_schedule_stat == "True": # Boolean read from file is string. Too lazy to convert and deal w/ string2bool.
    print("Job added with Test Scheduler")
    wsb_quant_scheduler.add_job(write_wsb_freq_count, "interval", minutes=2)
else:
    print("Job added with Production Scheduler")
    wsb_quant_scheduler.add_job(write_wsb_freq_count, "interval", hours=12)

wsb_quant_scheduler.start()