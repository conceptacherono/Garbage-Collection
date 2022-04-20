
from unicodedata import name
from django.urls import path,re_path,include
from.import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home,name='home'),
    path('events/',views.current_events,name='events'),
    path('attend/',views.attend_event,name='attend'),
    re_path(r'^service/',views.service,name = 'service'),
    re_path(r'^new-post/', views.new_post, name='new-post'),
    re_path(r'^posts/',views.posts,name = 'post'),
    re_path(r'^post/(\d+)',views.view_post,name ='view_project'),
    path("register/",views.register_user,name='register'),
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name='logout'),
    path('api/collect',views.event_list,name='collect'),
    re_path(r'^api/collect/(?P<pk>[0-9]+)$',views.event_details,name='details'),
    path('api/collect/published',views.event_list_published,name='published'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)