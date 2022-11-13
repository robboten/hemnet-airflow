# Install the base requirements for the app.
# This stage is to support development.
FROM apache/airflow:2.4.2
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
