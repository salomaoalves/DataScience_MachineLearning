# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.13

# Install Chromium and its driver (used by Selenium to scrape the comments)
RUN apt-get update && apt-get install -y chromium chromium-driver && rm -rf /var/lib/apt/lists/*
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm
RUN python -m nltk.downloader stopwords

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
