from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^check/$',views.index,name='check'),
    url(r'^login/$',views.login, name='login'),
    url(r'^addcar/$',views.addCar,name='addcar'),
    url(r'^register/$',views.register,name='register'),
]