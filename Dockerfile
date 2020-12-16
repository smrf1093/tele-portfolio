FROM python:alpine3.6

# Copy the script in
COPY . /
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install -r /requirements.txt


CMD ["flask", "-run"]
