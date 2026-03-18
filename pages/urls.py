from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('cv/', views.cv_print, name='cv_print'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]
