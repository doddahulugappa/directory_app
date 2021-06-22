# Teacher's Directory

> To setup the project follow the the instructions below

- `git clone https://github.com/doddahulugappa/directory_app.git`
- `cd directory_app`
    - `pip install -r requirements.txt`
    - `python manage.py makemigrations`
    - `python manage.py migrate`
    - `python manage.py createsuperuser` 
    - `python manage.py runserver <IP>:<PORT>`
- Open the url in any browser
    - Login with the created user creds and explore all the functionalities
- Use Import option for Bulk Import 
    - first import subjects.csv from data directory
    - second import teacher.csv from data directory
    - try to add subjects more than 5, will get an error
    - try to add duplicate email, will get an error
- Export options given for the export data
- Filter options for filtering data

