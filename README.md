# Hybrid Movie Recommendation System Backend

## Set up
```
pip install -r requirements.txt 
```
modify settings.py databases setting for your local DB
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DBName',
        'USER':'UserLikeRoot',
        'PASSWORD':'pw',
        'HOST':'localhost',
        'PORT': '3306'
    }
}
```
## Import .sql to the DB
.sql file is located here: https://www.notion.so/Shared-Files-and-Repository-7de40876dbaa4031a236f8a703a75650

```
mysql -u username -p database_name < file.sql
```
or use mysql workbench to import the file

## run server
```
python3 manage.py runserver
```
