# Teacher's Directory

> To setup the project follow the the instructions below


- optional setup venv if required
    - `pip install virtualenv`
    - `virtualenv venv`
- To activate venv in windows
    - `venv\script\activate` 
- To activate venv in linux
    - `source venv/bin/activate` 
    
# Clone the project
- `git clone https://github.com/doddahulugappa/directory_app.git`
- `cd directory_app`
    - `pip install -r requirements.txt`
    - `python manage.py makemigrations`
    - `python manage.py migrate`
    - `python manage.py createsuperuser` 
    - `python manage.py runserver <IP>:<PORT>`
# Usage Guide
- Open the url in any browser
    - Login with the created user creds and explore all the functionalities
- Use Import option for Bulk Import 
    - first import subjects.csv from data directory
    - second import teacher.csv from data directory
    - try to add subjects more than 5, will get an error
    - try to add duplicate email, will get an error
- Export options given for the export data
- Filter options for filtering data


# Docker Setup
- Create Dockerfile and save in the main directory
``` 
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
```

- Build Docker Image
```
docker build -t directory_app .
```

- Run Docker Image
```
docker run -it -p 8020:8020 directory_app
```

- Tag Docker Image
```
docker run -it -p 8020:8020 directory_app
```

- Push Docker Image
```
docker run -it -p 8020:8020 directory_app
```
