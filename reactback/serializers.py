from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import Movies,Tags,Ratings,User,Comments

class MoviesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movies
        fields = ('movieid','runtime','year','genre','score','storyline','title')


class RatingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ratings
        fields = ('rating', 'userid','movieid','record_date','tstamp')


class TagsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tags
		fields = ('tag','userid','movieid','tstamp')

class CommentsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Comments
		fields = ('commentid','comment','userid','movieid','tstamp')


class UserSer(UserCreateSerializer):
	class Meta:
		model = User
		fields = ('id','username','password','first_name','last_name','email','is_staff')