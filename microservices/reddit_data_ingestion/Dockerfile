FROM python

COPY . /app/reddit_pipeline/
 
WORKDIR /app/reddit_pipeline/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "daily_top_post_ingestion.py"]