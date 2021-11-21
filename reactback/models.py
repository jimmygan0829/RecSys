# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)

    REQUIRED_FIELDS = ['email','first_name','last_name']
    #USERNAME_FIELD = 'username'
    def get_username(self):
        return self.username
    class Meta:
        db_table = 'auth_user'



class Movies(models.Model):
    movieid = models.PositiveIntegerField(primary_key=True)
    runtime = models.IntegerField()
    year = models.IntegerField()
    genre = models.CharField(max_length=125, blank=True, null=True)
    score = models.FloatField(null = True)
    storyline = models.CharField(max_length=5000, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'movies'


class Ratings(models.Model):
    rating = models.FloatField()
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.ForeignKey(Movies, models.DO_NOTHING, db_column='movieid')
    tstamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'


class Tags(models.Model):
    tag = models.CharField(max_length=125)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.ForeignKey(Movies, models.DO_NOTHING, db_column='movieid')
    tstamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'

class Comments(models.Model):
    commentid = models.PositiveIntegerField(primary_key = True)
    comment = models.CharField(max_length=1000)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.ForeignKey(Movies, models.DO_NOTHING, db_column='movieid')
    tstamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'

# class Crit(models.Model):
#     cri_id = models.AutoField(primary_key=True)
#     cri_att = models.CharField(max_length=400)
#     pts = models.IntegerField()

#     class Meta:
        
#         db_table = 'crit'


# class DDate(models.Model):
#     d_date = models.DateField()
#     d_id = models.AutoField(primary_key = True)

#     class Meta:
        
#         db_table = 'd_date'


# class ELog(models.Model):
#     log_id = models.AutoField(primary_key=True)
#     author = models.CharField(max_length=40)
#     submission_date = models.DateTimeField(auto_now=True)
#     content = models.CharField(max_length=2000, blank=True, null=True)

#     class Meta:
#         db_table = 'e_log'


# class Effo(models.Model):
#     eff_id = models.AutoField(primary_key=True)
#     submission_date = models.DateTimeField(auto_now=True)
#     author = models.CharField(max_length=40,null= True)
#     record_date = models.DateField()
#     tasks_done = models.CharField(max_length=800)
#     pts = models.IntegerField()
#     note = models.CharField(max_length=400)

#     class Meta:
        
#         db_table = 'effo'
