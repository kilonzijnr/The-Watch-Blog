from django.urls import path, include
from . import views

#urls below
urlpatterns = [
    path('', views.single_hood, name='hood'),
    path('register/', views.registerUser, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
]