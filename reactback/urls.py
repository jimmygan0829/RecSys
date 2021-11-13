"""reactback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
#from .views import CritViewSet,EffoViewSet,EffoUserSet,DDateViewSet,CritDoSet,AdminViewSet
from .views import MovieSet
router = routers.DefaultRouter()

router.register(r'movie', MovieSet,basename='ind')
# router.register(r'viewcrit', CritViewSet)
# router.register(r'adminview', AdminViewSet)
# router.register(r'docrit',CritDoSet)
# router.register(r'vieweffo',EffoViewSet)
# router.register(r'effouser',EffoUserSet)
# router.register(r'ddate',DDateViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('rest-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('',include('djoser.urls')),
    path('',include('djoser.urls.authtoken')),

]
