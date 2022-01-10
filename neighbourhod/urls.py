from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

#urls below
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.hoods, name='hoods'),
    path('account/', include('django.contrib.auth.urls')),
    path('new-hood/', views.create_hood, name='new-hood'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/edit/', views.edit_profile, name='edit-profile'),
    path('join_hood/<id>', views.join_hood, name='join-hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave-hood'),
    path('single_hood/<hood_id>', views.single_hood, name='single-hood'),
    path('<hood_id>/new-post', views.create_post, name='post'),
    path('<hood_id>/members', views.hood_members, name='members'),
    path('search/', views.search_business, name='search'),
    path('create_business/', views.createBusiness, name='create_business')

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)