from django.urls import path
from projects.views import *
app_name = 'projects'



urlpatterns = [
    path('',ProjectListView.as_view(), name='projects_list'),
    path('add-project',AddProjectView.as_view(), name='projects_add')
    
    
]