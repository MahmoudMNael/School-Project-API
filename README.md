<h1>Jujutsu School API</h1>

## Initialize the project

#### 1. Clone the repository with `git clone https://github.com/MahmoudMNael/School-Project-API.git`

#### 2. Initialize venv with `python -m venv .venv`

#### 3. Activate venv with `.venv/Scripts/activate`

#### 4. Run `pip install -r requirements.txt` in your terminal to install the required packages for this project

#### 5. Go to 'web_project' directory

#### 6. Run `python manage.py makemigrations`

#### 7. Run `python manage.py migrate`

#### 8. Run `python manage.py runserver` and you will be ready to go ❤

## Create new SuperUser (Django Admin)

#### 1. Open your terminal on the folder web_project to access the manage.py file

#### 2. Run `python manage.py shell`

#### 3. Run `from authentication.models import User`

#### 4. Run `user = User(email='example@mail.com', is_superuser=True, is_staff=True)`

#### 5. Run `user.set_password('examplepassword')`

#### 6. Run `user.save()`

#### 7. Run `exit()`

#### 8. Now you have a superuser account and ready to log in to the django admin app ❤
