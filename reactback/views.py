from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .serializers import MoviesSerializer,RatingsSerializer,TagsSerializer,UserSer
from .models import Movies,Tags,Ratings, User
import datetime,time
import re,json
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests,random
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

# def date_converter(inp):
# 	input_list = inp.split("-")

# 	if len(input_list)!= 3:
# 		print(input_list)
# 		return False
# 	try:
		
# 		for idx,item in enumerate(input_list):
# 			#print(input_list)
# 			input_list[idx] = re.sub(r"\s+", "", item)
# 			temp = input_list[idx]
# 			if temp[0] == '0':
# 				temp = temp[1:]
# 				#print(temp,type(temp))
# 			#print(temp, type(temp))
# 			#print(input_list)
# 			input_list[idx] = int(temp)
# 		#print('this is output before going back {}'.format(output))
# 		output = datetime.date(input_list[0],input_list[1],input_list[2])
		
# 	except Exception as e:
# 		print('~~~~~~~~{}~~~~~~~'.format(e))
# 		return False
# 	return output


# class AdminViewSet (viewsets.ReadOnlyModelViewSet):
# 	queryset = User.objects.all()
# 	permission_classes = (IsAuthenticated,)
# 	serializer_class = UserSer
# 	def get_queryset(self):
# 		id_toCheck = self.request.user.id
# 		qs = User.objects.filter(id = id_toCheck)
# 		return qs
# 	# @action(detail= False, methods = ['get'],url_path='check-admin')
# 	# def admin_check(self,request,pk=None):
		
# 	# 	id_toCheck = request.user.id
		

# 	# 	qs = User.objects.filter(id = id_toCheck)
# 	# 	stuff = self.get_queryset()
# 	# 	print(stuff)
# 	# 	return JsonResponse({'stuff':'testing'})

def checkingInput(varId):
	pass

def getRec(curr_id):
	#testing phase
	l = list(Movies.objects.filter().values('movieid'))
	packet = {}
	url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{curr_id}.json'
	response = requests.get(url)
	packet['main'] = response.json()
	packet['recommendation'] = {}
	randomlist = random.sample(range(0, len(l)), 10)
	for idx in randomlist:
		mid = l[idx]['movieid']
		url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{mid}.json'
		response = requests.get(url)
		if response.status_code == 200:
			content = response.json()
			n = random.randint(1,100)
			imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{mid}.jpg'
			packet['recommendation'][str(mid)] = {'title':content['title'],'avg_rate':f'{n}%','img_link':imgUrl}
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
	randomlist = random.sample(range(0, len(l)), 20)
	for idx in randomlist:
		mid = l[idx]['movieid']
		url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{mid}.json'
		response = requests.get(url)
		if response.status_code == 200:
			content = response.json()
			n = random.randint(1,100)
			imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{mid}.jpg'
			packet['recommendation'][str(mid)] = {'title':content['title'],'avg_rate':f'{n}%','img_link':imgUrl}
	return packet

'''
params: user, default None
return: return global highly praised if None, else customized recommendation method
'''
def getFamFav(user = None):
	packet = {}
	packet['recommendation'] = {}
	randomlist = random.sample(range(0, len(l)), 20)
	for idx in randomlist:
		mid = l[idx]['movieid']
		url = f'https://inf551-4b646-default-rtdb.firebaseio.com/content/{mid}.json'
		response = requests.get(url)
		if response.status_code == 200:
			content = response.json()
			n = random.randint(1,100)
			imgUrl = f'https://filmimg.s3.us-west-2.amazonaws.com/{mid}.jpg'
			packet['recommendation'][str(mid)] = {'title':content['title'],'avg_rate':f'{n}%','img_link':imgUrl}
	return packet



class MovieSet(viewsets.ReadOnlyModelViewSet):
	# queryset = Effo.objects.all()
	serializer_class = MoviesSerializer
	# permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		#queryset = Movies.objects.all()
		movieid = self.request.query_params.get('id', None)
		
		if movieid is not None:
			queryset = Movies.objects.filter(movieid=int(movieid))
			return  queryset		

		return Movies.objects.filter(movieid=int(2))


	

	@action(detail= False, methods = ['get'],url_path='each')
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



# class DDateViewSet(viewsets.ModelViewSet):
# 	queryset = DDate.objects.all()
# 	permission_classes = (IsAuthenticated,)
# 	serializer_class = DDateSerializer
# 	def create (self,request):
# 		ser = DDateSerializer(data = request.data)
# 		if ser.is_valid():
# 			if request.user.username != 'GAN':
# 				return JsonResponse({'status':'Permission not allowed'})
# 			d = datetime.datetime.strptime(str(ser.data['d_date']), "%Y-%m-%d").date()
# 			DDate.objects.create(d_date = d)
# 			return JsonResponse({'status': 'set'})
# 	def destroy(self,request,pk=None):
# 		dd = self.get_object()
# 		ser = DDateSerializer(dd,many = False)

# 		if request.user.username != 'GAN':
# 			return JsonResponse({'status':'Permission not allowed'})
# 		else:
# 			dd.delete()
# 			return JsonResponse({'status':'set'})
# 	def update(self,request,pk=None):
# 		ser = DDateSerializer(data = request.data)
# 		if ser.is_valid():
# 			if request.user.username!='GAN':
# 				return JsonResponse({'status':'Permission not allowed'})
# 			d_up = self.get_object()
# 			my_own = DDateSerializer(d_up,many = False)
# 			d = datetime.datetime.strptime(str(ser.data['d_date']), "%Y-%m-%d").date()
# 			DDate.objects.filter(d_id = my_own.data['d_id']).update(d_date = d)
# 			return JsonResponse({'status':'set'})

# 	@action(detail= False, methods = ['get'],url_path='latest')
# 	def get_latest(self,request,pk=None):
# 		all_date = DDate.objects.all()
# 		ser = DDateSerializer(all_date,many = True)
# 		convert_list = []
# 		for item in ser.data:
# 			convert_list.append(dict(item))
# 		if is_empty(convert_list) == True:
# 			return JsonResponse({'status':'empty'})

# 		count_date_obj = DDate.objects.latest('d_date')
		
# 		d_ser = DDateSerializer(count_date_obj,many = False)

# 		count_date = d_ser.data['d_date']
# 		count_id = d_ser.data['d_id']
# 		return JsonResponse({'latest':str(count_date),'d_id':count_id})







# class CritViewSet(viewsets.ReadOnlyModelViewSet):
# 	permission_classes = (IsAuthenticated,)
# 	queryset = Crit.objects.all().order_by('cri_id')
# 	serializer_class = CritSerializer


	

# class CritDoSet(viewsets.ModelViewSet):
# 	permission_classes = (IsAdminUser,)
# 	queryset = Crit.objects.all().order_by('cri_id')
# 	serializer_class = CritSerializer


# class EffoViewSet (viewsets.ModelViewSet):
# 	permission_classes = (IsAuthenticated,)
# 	queryset = Effo.objects.all()
# 	serializer_class = EffoSerializer

# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(EffoViewSet, self).dispatch(request, *args, **kwargs)
# 	# this is for Logging create
# 	#@action(detail= False, methods = ['post'],url_path='log')


# 	def create(self,request):#,pk=None):
		
# 		ser = EffoSerializer(data = request.data)
# 		au = request.user.username
# 		if ser.is_valid():
# 			#print('~~~~{}~~~~~'.format(ser.data))
# 			cont_add = 'CREATE '+ser.data['note']+': '+str(ser.data['record_date']) +': '+ser.data['tasks_done']+': '+str(ser.data['pts'])
# 			ELog.objects.create(author = au,content=cont_add)
# 			#print()
# 			d = datetime.datetime.strptime(str(ser.data['record_date']), "%Y-%m-%d").date()
# 			b2 = Effo.objects.create(author = au,note=ser.data['note'],record_date=d,tasks_done=ser.data['tasks_done'],pts=int(ser.data['pts']))

# 			return JsonResponse({'status': 'set','effo_id':b2.eff_id,'author':request.user.username})
# 		else:
# 			return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)

# 	#@action(detail= True, methods = ['delete','get'],url_path='del-log')
# 	def destroy(self,request,pk=None):

# 		effo = self.get_object()
# 		ser = EffoSerializer(effo,many= False)
# 		if ser.data['author'] != request.user.username:
# 			return JsonResponse({'status':'Permission not allowed'})
# 		#print(temp.data)

# 		#effo.delete()

# 		#ser = EffoSerializer(data = request.data)
# 		print('~~~~DELETE \n {}~~~~~'.format(ser.data))
# 		cont_add = 'DEL '+ser.data['note']+': '+str(ser.data['record_date']) +': '+ser.data['tasks_done']+': '+str(ser.data['pts'])
# 		ELog.objects.create(author = ser.data['author'],content=cont_add)
# 		effo.delete()
# 		return JsonResponse({'status': 'set'})

# 	#@action(detail= True, methods = ['put'],url_path='edit-log')
# 	def update(self,request,pk=None):
# 		ser = EffoSerializer(data = request.data)
# 		s_obj = self.get_object()
# 		s_serial = EffoSerializer(s_obj,many = False)
# 		if ser.is_valid():
# 			#print(s_serial.data['author'],"THIS IS THE ONE FROM THE LEFT     ",request.user.username)
# 			if s_serial.data['author'] != request.user.username:
# 				return JsonResponse({'status':'Permission not allowed'})
# 			#print('~~~~{}~~~~~'.format(ser.data))
# 			cont_add = 'EDIT '+ser.data['note']+': '+str(ser.data['record_date']) +': '+ser.data['tasks_done']+': '+str(ser.data['pts'])
# 			ELog.objects.create(author = request.user.username,content=cont_add)
# 			#print()
# 			d = datetime.datetime.strptime(str(ser.data['record_date']), "%Y-%m-%d").date()
# 			effo_obj = self.get_object()
# 			my_own = EffoSerializer(effo_obj,many= False)

# 			Effo.objects.filter(eff_id =my_own.data['eff_id']).update(author = request.user.username,note=ser.data['note'],record_date=d,tasks_done=ser.data['tasks_done'],pts=int(ser.data['pts']))

# 			return JsonResponse({'status': 'set','effo_id':my_own.data['eff_id'],'author':request.user.username})
# 		else:
# 			return JsonResponse(ser.errors, status=status.HTTP_400_BAD_REQUEST)


		






# class EffoUserSet(viewsets.ReadOnlyModelViewSet):
# 	queryset = Effo.objects.all()
# 	serializer_class = EffoSerializer
# 	permission_classes = (IsAuthenticated,)

# 	def get_queryset(self):
# 		queryset = Effo.objects.all()
# 		username = self.request.query_params.get('author', None)
# 		check_date = self.request.query_params.get('record_date', None)
# 		#print('---------CHECKING THE DATE HERE :)-------',type(check_date),'  ',check_date)
# 		if username is not None:
# 			queryset = queryset.filter(author=username)
# 		if check_date is not None:
# 			temp = check_date
# 			t = datetime.datetime.strptime(check_date, "%Y-%m-%d").date()
# 			#print('-------------------------')
# 			#print(check_date,type(t))
# 			queryset = queryset.filter(record_date__gt=t)
		

# 		return queryset

# 	@action(detail= False, methods = ['get'],url_path='auto')
# 	def auto_pts(self,request,pk=None):
# 		params = request.query_params
# 		p_dict = params.dict()
# 		# General Idea: if there is a date, will add points based on date and username, if there is no input date
# 		# will add points based on username and dividend date in DB; if there is no dividend date in DB, will accumulate hitoric pts
# 		qs = self.get_queryset()
# 		ser = EffoSerializer(qs,many = True)
# 		convert_list = []
# 		for item in ser.data:
# 			convert_list.append(dict(item))
# 		if is_empty(convert_list) == True:
# 			#checking the if the list is empty, if so, will have to response null back
# 			return JsonResponse({'status':'nothing'})
# 		#print(convert_list)
# 		if "author" in p_dict and "record_date" not in p_dict:

			
# 			dCount = DDate.objects.all()
# 			#accumuulate all the data
# 			total_pts = 0
# 			if is_empty(list(dCount)) == True:
# 				for item in convert_list:
# 					total_pts += item['pts']
# 				return JsonResponse({p_dict["author"]:total_pts,"status":"valid"})
# 			else:
# 				count_date_obj = DDate.objects.latest('d_date')
# 				#print('-----------filter data----------')
# 				d_ser = DDateSerializer(count_date_obj,many = False)
# 				count_date = d_ser.data['d_date']
# 				#print(type(count_date))
# 				qs = qs.filter(record_date__gt = count_date)
# 				convert_list = []
# 				ser = EffoSerializer(qs,many = True)
# 				for item in ser.data:
# 					convert_list.append(dict(item))
# 				if is_empty(convert_list) == True:
# 					return JsonResponse({p_dict["author"]:total_pts,"status":"valid"})
# 				else:
# 					for item in convert_list:
# 						total_pts+=item['pts']
# 					return JsonResponse({p_dict["author"]:total_pts,"status":"valid"})
# 		elif "author" in p_dict and "record_date" in p_dict:
# 			total_pts = 0
# 			for item in convert_list:
# 				total_pts+=item['pts']
# 			return JsonResponse({p_dict["author"]:total_pts,"status":"valid"})
# 		elif "record_date" not in p_dict and "author" not in p_dict:
			
# 			if "hist" in p_dict:
				
# 				user_dic = {}
# 				for item in convert_list:
# 					if item["author"] not in user_dic:
# 						user_dic[item["author"]] = item["pts"] # initialize the whole thing
# 					else:
# 						user_dic[item["author"]]+=item["pts"]
# 				user_dic["status"] = "valid"

# 				return JsonResponse(user_dic)
# 			else:
# 				# if there is no dict in 
# 				dCount = DDate.objects.all()
# 				if is_empty(list(dCount)) == True:
# 					user_dic = {}
# 					for item in convert_list:
# 						if item["author"] not in user_dic:
# 							user_dic[item["author"]] = item["pts"]
# 						else:
# 							user_dic[item["author"]]+=item["pts"]

# 					user_dic["status"] = "valid"

# 					return JsonResponse(user_dic)
# 				else:
# 					count_date_obj = DDate.objects.latest('d_date')
# 					d_ser = DDateSerializer(count_date_obj,many = False)
# 					count_date = d_ser.data['d_date']
# 					rs = qs.filter(record_date__gt = count_date)
# 					rs_list = []
# 					rser = EffoSerializer(rs,many = True)
# 					for item in rser.data:
# 						rs_list.append(dict(item))
					
# 					#after dividend date, nobody did shit
# 					# init all the users first and then add pts for those who have pts after d_date
# 					user_dic = {}
# 					for item in convert_list:
# 						if item["author"] not in user_dic:
# 							user_dic[item["author"]] = 0
# 					if is_empty(rs_list) == True:
# 						user_dic["status"] = "valid"
# 						return JsonResponse(user_dic)
# 					else:
# 						#user_dic = {}
# 						for item in rs_list:
# 							if item["author"] not in user_dic:
# 								user_dic[item["author"]]=user_dic[item["pts"]]
# 							else:
# 								user_dic[item["author"]]+=item["pts"]
# 						user_dic["status"] = "valid"
# 						return JsonResponse(user_dic)












				



			














# 		return JsonResponse({"status":"invalid"})

		








