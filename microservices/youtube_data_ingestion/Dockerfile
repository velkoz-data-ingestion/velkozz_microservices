FROM python

COPY . /app/daily_youtube_channel_data/
 
WORKDIR /app/daily_youtube_channel_data/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "daily_youtube_channel_data_ingestion.py"]
