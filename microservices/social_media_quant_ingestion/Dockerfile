FROM python

COPY . /app/social_media_quant_pipeline/
 
WORKDIR /app/social_media_quant_pipeline/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "wsb_ticker_freq_ingestion.py"]