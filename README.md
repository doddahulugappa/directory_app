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
docker tag directory_app_v1 doddahulugappa/django:v2
```

- Push Docker Image
```
docker push doddahulugappa/django:v2
```
- Azure ACR

```
az login
az acr login --name myregistry
docker login myregistry.azurecr.io
docker tag directory_app myregistry.azurecr.io/huli/directory_app
docker push myregistry.azurecr.io/django/directoryapp
```


# Celery Integration
```
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dubai'
CELERY_RESULT_BACKEND = 'django-db'

```
- command to start celery worker and celery beat
```
celery -A directory_app.celery worker --pool=solo -l info
celery -A directory_app beat -l info
```
## Redis for windows
Download msi file from below and install
- https://github.com/tporadowski/redis/releases

## GraphQL integration
- settings.py
```
pip install graphene-django
INSTALLED_APPS = (
    # ...
    'graphene_django',
)

GRAPHENE = {
    'SCHEMA': 'app.schema.schema' # Where your Graphene schema lives
}
```
- urls.py

```
from django.conf.urls import url
from graphene_django.views import GraphQLView

urlpatterns = [
    # ...
    url(r'^graphql$', GraphQLView.as_view(graphiql=True)),
]
```

- schema.py
```
from graphene_django import DjangoObjectType
import graphene

class User(DjangoObjectType):
    class Meta:
        model = UserModel

class Query(graphene.ObjectType):
    users = graphene.List(User)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()

schema = graphene.Schema(query=Query)

query = '''
    query {
      users {
        name,
        lastName
      }
    }
'''
result = schema.execute(query)
```
- Sample Queries
```
{
  subjects {
    subjectName
  }
}

{
  mentors {
    firstName
    lastName
    phoneNumber
    roomNumber
    emailAddress
  }
}

{
  users {
    name
    lastName
  }
}
```


