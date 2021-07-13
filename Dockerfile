# app/Dockerfile

# Get the python image
FROM python:3.8.6

# Set the working directory for the container
WORKDIR /directory_app

# Installing system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils

# Copy the requirements
COPY requirements.txt ./

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application files and directories
COPY . .

# Serve application
#CMD gunicorn --bind :8010 directory_app.wsgi --workers 1 --timeout 120
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "localhost:8000"]