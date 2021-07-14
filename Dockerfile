# Use the official Python image from the Docker Hub
FROM python:3.8.2

# Make a new directory to put our code in.
RUN mkdir /directory_app

# Change the working directory.
WORKDIR /directory_app

# Copy to code folder
COPY . /directory_app/

# Install the requirements.
RUN pip install -r requirements.txt

# Run the application:
CMD python manage.py runserver 0.0.0.0:8000