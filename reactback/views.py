from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from .serializers import MoviesSerializer,RatingsSerializer,TagsSerializer,UserSer,CommentsSerializer
from .models import Movies,Tags,Ratings, User,Comments
import datetime,time
import re,json
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests,random
from django.db import connection
# def is_empty(any_structure):
#     if any_structure:
#         print('Structure is not empty.')
#         return False
#     else:
#         print('Structure is empty.')
#         return True


def advPrint(note,anything):
    print("\n\n\n")

    print(f"++++++++++++++++++++++++++START OF DEBUGGGG+++++++++++++++++++++++\n{note}\n\n{anything}\n++++++++++++++++++++++++++END OF DEBUGGGG+++++++++++++++++++++++")
    print("\n\n\n")



def checkingInput(varId):
	pass

def retrieveReviewCount(curr_id):
	cursor = connection.cursor()
	cursor.execute(f"""SELECT COUNT(*) FROM ratings WHERE movieid = {curr_id}""")
	row = cursor.fetchone()
	return row[0]

def retrieveUserHistory(uid):
	cursor = connection.cursor()
	cursor.execute(f"""SELECT COUNT(*) FROM ratings WHERE userId = {uid}""")
	row = cursor.fetchone()
	if row[0] == 0:
		return False
	return True


def watchagain(uid):
	cursor = connection.cursor()
	cursor.execute(f"""
		WITH tb1 AS(
SELECT movieid,rating FROM ratings WHERE userId = {uid}
ORDER BY rating DESC,tstamp LIMIT 10
)
SELECT movies.movieid,movies.title,movies.score 
FROM movies JOIN tb1 ON movies.movieid = tb1.movieid;""")
	rows = cursor.fetchall()
	rec = {"recommendation":{}}
	for eachObj in rows:
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{eachObj[0]}.jpg'
		rec["recommendation"][f"{eachObj[0]}"] = {"title":eachObj[1],"avg_rate":score100(eachObj[2]),"img_link":imgUrl}
	return rec



def recentRelease():
	cursor = connection.cursor()
	cursor.execute(f"""
		WITH tb1 AS(
SELECT movieid,COUNT(*) AS cnt from ratings 
GROUP BY movieid HAVING cnt >=50)
SELECT movies.movieid,movies.title,movies.score,tb1.cnt 
FROM tb1 JOIN movies ON tb1.movieid = movies.movieid
ORDER BY movies.year DESC,tb1.cnt DESC LIMIT 20;""")
	rows = cursor.fetchall()
	rec = {"recommendation":{}}
	for eachObj in rows:
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{eachObj[0]}.jpg'
		rec["recommendation"][f"{eachObj[0]}"] = {"title":eachObj[1],"avg_rate":score100(eachObj[2]),"img_link":imgUrl}
	return rec


def criticalAcclaim():
	cursor = connection.cursor()
	cursor.execute(f"""
		WITH tb1 AS(
SELECT movieid,COUNT(*) AS cnt from ratings 
GROUP BY movieid HAVING cnt >=50)
SELECT movies.movieid,movies.title,movies.score,tb1.cnt 
FROM tb1 JOIN movies ON tb1.movieid = movies.movieid
ORDER BY movies.score DESC,tb1.cnt DESC LIMIT 20;""")
	rows = cursor.fetchall()
	rec = {"recommendation":{}}
	for eachObj in rows:
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{eachObj[0]}.jpg'
		rec["recommendation"][f"{eachObj[0]}"] = {"title":eachObj[1],"avg_rate":score100(eachObj[2]),"img_link":imgUrl}
	return rec


def topinGenre(inpGenre):
	cursor = connection.cursor()
	cursor.execute(f"""
		WITH tb1 AS(
		SELECT movieid,COUNT(*) AS cnt from ratings GROUP BY movieid
		HAVING cnt >=50
			),
 		tb2 AS(
		SELECT * from movies WHERE genre LIKE '%{inpGenre}%'
			)
		SELECT tb2.movieid,tb2.title,tb2.score,tb1.cnt 
			FROM tb1 JOIN tb2 ON tb1.movieid = tb2.movieid
			ORDER BY tb2.score DESC,tb1.cnt DESC LIMIT 20;""")
	rows = cursor.fetchall()
	rec = {"recommendation":{}}
	for eachObj in rows:
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{eachObj[0]}.jpg'
		rec["recommendation"][f"{eachObj[0]}"] = {"title":eachObj[1],"avg_rate":score100(eachObj[2]),"img_link":imgUrl}
	return rec




def createOrUpdateComments(userid,movieid,comment):
	cursor = connection.cursor()
	try:
		cursor.execute(f"""
			SELECT * FROM comments WHERE movieid={movieid} AND userId = {userid}	
		""")
		row = cursor.fetchall()
		if len(row) != 0 :
			cursor.execute(f"""
			UPDATE comments SET comment = '{comment}' WHERE movieid={movieid} AND userId = {userid};
			""")
			connection.commit()
		else:
			advPrint("are you HERE BEFORE ENCOUNTER ERRRRRORRRR!!!?????",{})
			cursor.execute(f"""
			INSERT INTO comments (movieid, userId,comment) VALUES ({movieid},{userid},'{comment}');  
			""")
			connection.commit()

		advPrint("update/create comment completed",[])
		return True
	except Exception as e:
		print(e)
		return False

def getRatingByBothId(userid,movieid):
	cursor = connection.cursor()
	cursor.execute(f"""
			SELECT rating FROM ratings WHERE movieid={movieid} AND userId = {userid}	
		""")
	row = cursor.fetchall()
	if len(row)!=0:
		return row[0][0],True
	else:
		return None,False




def createOrUpdateRating(userid,movieid,rating):
	cursor = connection.cursor()
	try:
		cursor.execute(f"""
			SELECT * FROM ratings WHERE movieid={movieid} AND userId = {userid}	
		""")
		row = cursor.fetchall()
		if len(row) != 0 :
			cursor.execute(f"""
			UPDATE ratings SET rating = {rating} WHERE movieid={movieid} AND userId = {userid};
			""")
			connection.commit()
		else:
			advPrint("are you HERE BEFORE ENCOUNTER ERRRRRORRRR!!!?????",{})
			cursor.execute(f"""
			INSERT INTO ratings (movieid, userId,rating) VALUES ({movieid},{userid},{rating});  
			""")
			connection.commit()

		advPrint("update/create rating completed",[])
		return True
	except Exception as e:
		print(e.message)
		return False
def score100(sc):
	if sc is not None:
		return int(round(sc/5,2)*100)
	else:
		return "None"

def getRec(curr_id):
	#testing phase
	l = list(Movies.objects.filter().values('movieid'))
	packet = {}
	url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{curr_id}.json'
	response = requests.get(url)
	packet['main'] = response.json()
	packet['main']['score'] = score100(Movies.objects.get(movieid = curr_id).score)
	numU_score = retrieveReviewCount(curr_id)
	packet['main']['review_count'] = numU_score

	packet['recommendation'] = {}
	randomlist = random.sample(range(0, len(l)), 10)
	for idx in randomlist:
		mid = l[idx]['movieid']
		# url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{mid}.json'
		# response = requests.get(url)
		# if response.status_code == 200:
		# 	content = response.json()
		content={}
		content['title'] = Movies.objects.get(movieid = mid).title
		content['storyline'] = Movies.objects.get(movieid = mid).storyline
		n = Movies.objects.get(movieid = mid).score#random.randint(1,100)
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{mid}.jpg'
		packet['recommendation'][str(mid)] = {'title':content['title'],'avg_rate':score100(n),'img_link':imgUrl}
	return packet

	# print('----->',l[4]['movieid'],' ',len(l))#.movieid,' ',l[4].year)
	# return

'''
params: user, default None
return: return global trending if the user is None or cold start, else putout customized rec from one of the method
'''
def getTrendingNow(user = None):
	packet = {}
	packet['recommendation'] = {}
	l = list(Movies.objects.filter().values('movieid'))
	randomlist = random.sample(range(0, len(l)), 3)
	for idx in randomlist:
		mid = l[idx]['movieid']
		# url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{mid}.json'
		# response = requests.get(url)
		# if response.status_code == 200:
		# 	content = response.json()
		content={}
		content['title'] = Movies.objects.get(movieid = mid).title
		content['storyline'] = Movies.objects.get(movieid = mid).storyline
		n = Movies.objects.get(movieid = mid).score#random.randint(1,100)
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{mid}.jpg'
		packet['recommendation'][str(mid)] = {'title':content['title'],'avg_rate':score100(n),'img_link':imgUrl}
	return packet

'''
params: user, default None
return: return global highly praised if None, else customized recommendation method
'''
def getFamFav(user = None):
	packet = {}
	packet['recommendation'] = {}
	l = list(Movies.objects.filter().values('movieid'))
	randomlist = random.sample(range(0, len(l)), 3)
	for idx in randomlist:
		mid = l[idx]['movieid']
		# url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{mid}.json'
		# response = requests.get(url)
		# if response.status_code == 200:
		# 	content = response.json()
		content={}
		content['title'] = Movies.objects.get(movieid = mid).title
		content['storyline'] = Movies.objects.get(movieid = mid).storyline
		n = Movies.objects.get(movieid = mid).score#random.randint(1,100)
		imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{mid}.jpg'
		packet['recommendation'][str(mid)] = {'title':content['title'],'avg_rate':score100(n),'img_link':imgUrl}
	return packet

class CommentsHandler(viewsets.ModelViewSet):
	serializer_class = CommentsSerializer
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		movieid = self.request.query_params.get('movieid', None)
		if movieid is not None:
			queryset = Comments.objects.filter(movieid=int(movieid))
			return queryset
		return Comments.objects.filter(movieid=int(2))

	@action(detail= False, methods = ['post'],url_path='pushcom')
	def updateComment(self,request,pk= None):
		
		advPrint("request data is :::",dict(request.data))
		advPrint(f"{type(request.user)}requested user is ::::",request.user)
		data_dict = dict(request.data)
		movieid = int(data_dict['movieid'])
		userid = int(request.user.id)
		comment = str(data_dict['comment'])
		comment = comment.replace("'","\\'").replace('"','\\"')
		status=createOrUpdateComments(userid = userid,movieid = movieid,comment = comment)
		comObj = Comments.objects.get(userid= userid,movieid= movieid)
		print(f"status of the creation::::::",status)
		if status:
			return JsonResponse({'status':'valid','movieid':comObj.movieid.movieid,'userid':comObj.userid.id,'comment':comObj.comment})
		return JsonResponse({'status':'invalid'})


# testing purposes
class MovieScoreSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = MoviesSerializer
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		movieid = self.request.query_params.get('movieid', None)
		if movieid is not None:
			queryset = Movies.objects.filter(movieid=int(movieid))
			return queryset
		return Movies.objects.filter(movieid=int(2))

	

	@action(detail= False, methods = ['post'],url_path='scupdate')
	def updateScore(self,request,pk=None):
		advPrint("request data is :::",dict(request.data))
		advPrint(f"{type(request.user)}requested user is ::::",request.user)
		data_dict = dict(request.data)
		movieid = int(data_dict['movieid'])
		rate = float(data_dict['rating'])
		userid = int(request.user.id)
		status = createOrUpdateRating(userid = userid,movieid = movieid,rating = rate)
		if status:
			return JsonResponse({'status':'valid'})
		
		return JsonResponse({'status':'invalid'})

	@action(detail= False, methods = ['get'],url_path='each')
	def individualScore(self,request,pk=None):
		qs = self.get_queryset()
		if not qs:
			ret_dict['message'] = 'id not existed'
			ret_dict['status'] = 'invalid'

			return JsonResponse(ret_dict)
		else:
			target_movie=list(qs)[0]
			movieid = self.request.query_params.get('movieid', None)
			cursor = connection.cursor()
			cursor.execute(f"""SELECT COUNT(*) FROM ratings WHERE movieid = {movieid}""")
			row = cursor.fetchone()
			#for item in ct_review:
			print('what the hell::::::::: COUNT REVIEWS ',row)
			return JsonResponse({'score':target_movie.score,'status':'valid'})

class HomeSet(viewsets.ReadOnlyModelViewSet):
	# queryset = Effo.objects.all()
	serializer_class = MoviesSerializer
	permission_classes = (AllowAny,)

	def get_queryset(self):
		#queryset = Movies.objects.all()
		#movieid = self.request.query_params.get('id', None)
		#advPrint(f"{type(request.user)}requested user is ::::",request.user)
		# if movieid is not None:
		# 	queryset = Movies.objects.filter(movieid=int(movieid))
		# 	return  queryset
		#return JsonResponse(getTrendingNow())
		return Movies.objects.filter(movieid=int(2))


	

	@action(detail= False, methods = ['get'],url_path='home')
	def HomePage(self,request,pk=None):
		advPrint(f"{type(request.user)}requested user is ::::",request.user)
		from random import randrange
		#colduser = retrieveUserHistory()#randrange(10)%2
		ret_package = {}
		# will also add another condition to check if user has rating record or recommendations
		all_genre = ['Western', 'Film-Noir', 'Action', 'Fantasy', 
		'Documentary', 'IMAX', 'Horror', 'War', 'Mystery', 'Thriller', 'Crime',
		'Romance', 'Adventure', 'Musical', 'Sci-Fi', '(no genres listed)', 'Children']
		choice = random.choice(all_genre)

		if request.user.is_anonymous == False:
			if retrieveUserHistory(request.user.id) == True:
				recom = getFamFav()
				ret_package['watchagain']=watchagain(request.user.id)
				ret_package['FamFav']=recom
				ret_package['topAnime']=topinGenre('Animation')
				ret_package['topCome']=topinGenre('Comedy')
				ret_package['topDrama']=topinGenre('Drama')
				ret_package[choice]=topinGenre(choice)
				return JsonResponse(ret_package)

		ret_package['criticallyAcclaimed']=criticalAcclaim()
		ret_package['recentRelease']=recentRelease()
		ret_package['topAnime']=topinGenre('Animation')
		ret_package['topCome']=topinGenre('Comedy')
		ret_package['topDrama']=topinGenre('Drama')
		ret_package[choice]=topinGenre(choice)
		return JsonResponse(ret_package)
		


class MovieSet(viewsets.ReadOnlyModelViewSet):
	# queryset = Effo.objects.all()
	serializer_class = MoviesSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		#queryset = Movies.objects.all()
		movieid = self.request.query_params.get('id', None)
		
		if movieid is not None:
			queryset = Movies.objects.filter(movieid=int(movieid))
			return  queryset		

		return Movies.objects.filter(movieid=int(2))


	

	@action(detail= False, methods = ['get'],url_path='detail')
	def individualMovie(self,request,pk=None):
		params = request.query_params
		p_dict = params.dict()
		ret_dict = {}
		
		qs = self.get_queryset()
		if not qs:
			ret_dict['message'] = 'id not existed'
			ret_dict['status'] = 'invalid'
			return JsonResponse(ret_dict)
			
		else:
			target_movie = list(qs)[0]
			print(f"the whole object should be: {target_movie.runtime} {target_movie.movieid} {target_movie.genre} {target_movie.year}")
			ret_dict['message'] = 'LFG BRR'
			ret_dict['status'] = 'valid'

		print(' \n ')
		start = time.time()
		ret_packet = getRec(target_movie.movieid)
		movie_comment_qs = Comments.objects.filter(movieid = target_movie.movieid,userid = int(request.user.id))
		if movie_comment_qs:
			movie_comment = list(movie_comment_qs)[0].comment
		else:
			movie_comment = 'None'
		ind_rating,fetch_status = getRatingByBothId(userid=int(request.user.id),movieid=target_movie.movieid)
		if fetch_status:
			movie_rating = ind_rating
		else:
			movie_rating = 'None'
		ret_packet['main']['comment'] = movie_comment
		ret_packet['main']['user_score'] = movie_rating
		tmp = {'message':'LFG BRR','status':'valid'}

		advPrint('duration for getting the whole thing:::' , time.time()-start)
		ret_dict.update(ret_packet)
		#if val_status:
		#ser = MoviesSerializer(qs,many = False)
		# else:
		# 	ret_dict['message'] = 'invalid movie id, id not existed in the Database'
		# 	ret_dict['status'] = 'invalid'
		# 	return JsonResponse(ret_dict)
		advPrint('what are we looking at the return packet here:::::',ret_dict)
		#advPrint('before returnning, JSONREPONSE', JsonResponse(ret_dict,safe = False))
		
		return JsonResponse(ret_dict)



		








