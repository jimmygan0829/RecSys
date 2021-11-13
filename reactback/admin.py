from django.contrib import admin
from .models import *

admin.site.register(Tags)
admin.site.register(Movies)
admin.site.register(Ratings)
admin.site.register(User)