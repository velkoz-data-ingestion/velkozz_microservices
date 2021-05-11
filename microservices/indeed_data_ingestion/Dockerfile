FROM python

COPY . /app/indeed_data_ingestion_pipeline/
 
WORKDIR /app/indeed_data_ingestion_pipeline/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "indeed_jobs_listings_ingestion.py"]