# Importing Velkozz APIs:
from vdeveloper_api.velkozz_pipelines.social_media_pipelines.indeed_pipelines import IndeedJobListingsPipeline

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
indeed_scheduler = BlockingScheduler()

# Loading config params:
config = configparser.ConfigParser()
config.read(".indeed.env")

# Loading indeed job post configurations:
test_schedule_stat = config["velkozz_account"]["TEST_SCHEDULE"]
web_api_url = config["velkozz_account"]["VELKOZZ_API_URL"]
indeed_jobs_lst_file = "indeed_ingestion.txt"

print(f"Indeed Jobs Ingestion Script Active: \n -Test Scheduler: {test_schedule_stat} \n -url:{web_api_url} \n -Indeed Jobs List Path: {indeed_jobs_lst_file}")  

# Opening indeed_ingestion.txt file for list of jobs to search:
with open(indeed_jobs_lst_file) as json_file:
    indeed_params = json.load(json_file)

jobs = indeed_params[0]
locations = indeed_params[1]

print("Running Indeed Data Ingestion for the Following Jobs:", jobs, "\nIndeed Data Ingestion for Following Locations:", locations)

# Function that writes all data to the database:
def write_indeed_data():
    # Executing a pipeline for each Location and for each job O(n^2):
    for location in locations:
        for job in jobs:
            IndeedJobListingsPipeline(
            job,
            location,   
            3,
            VELKOZZ_API_URL = web_api_url,
            token = config["velkozz_account"]["VELKOZZ_TOKEN"])

            # Sleeping to avoid overloading the REST API:
            time.sleep(20)
    time.sleep(10)

# Adding the main function to the Scheduler:
# Config for rapid development testing:
if test_schedule_stat == "True": # Boolean read from file is string. Too lazy to convert and deal w/ string2bool.
    print("Job added with Test Scheduler")
    indeed_scheduler.add_job(write_indeed_data, "interval", minutes=5)
else:
    print("Job added with Production Scheduler")
    indeed_scheduler.add_job(write_indeed_data, "interval", hours=6)

indeed_scheduler.start()


