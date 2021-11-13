# Recommendation System Backend

## Set up
```
pip install -r requirements.txt 
```
modify settings.py databases setting for your local DB
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB Name',
        'USER':'User like root',
        'PASSWORD':'pw',
        'HOST':'localhost',
        'PORT': '3306'
    }
}
```
## run
python3 manage.py runserver
