# Note
 ##Backend
 use postgres
 
 change
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_discount',
        'USER': 'postgres',
        'PASSWORD': '19001006',
        'HOST': '127.0.0.1',
        'PORT': '1808',
    }
}
1. Activate venv
  cd to venv/Scripts/activate
2. Migrate database
  python manage.py makemigrations
  python manage.py migrate
3. Create superuser
  python manage.py createsuperuser
4. Start Backend 
  python manage.py runserver
  
  ##Front End
 cd to folder frontend
  npm start
