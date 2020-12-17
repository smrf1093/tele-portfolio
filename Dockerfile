FROM python:alpine3.6

# Copy the script in
COPY . /app/src
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install -r /requirements.txt

WORKDIR /app/src
