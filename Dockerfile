FROM python:alpine3.6

# Copy the script in
COPY . /app/src
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install -r /requirements.txt

<<<<<<< HEAD
CMD ["flask", "run", "--host", "0.0.0.0"]
=======
WORKDIR /app/src
>>>>>>> 0008b7b4a76f932fad0684279c8457566e87fca3
