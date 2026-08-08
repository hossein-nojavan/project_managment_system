from django.urls import path
from projects.views import *
app_name = 'projects'



urlpatterns = [
    path('',ProjectListView.as_view(), name='projects_list'),
    path('projects_add',AddProjectView.as_view(), name='projects_add'),
    path('projects_detail/<int:proj_id>',ProjectDetailView.as_view(), name='projects_detail'),
    path('delete/<int:proj_id>',ProjectDeleteView.as_view(), name='projects_delete'),
    path('update/<int:proj_id>',ProjectUpdateView.as_view(), name='projects_update'),
    
    
]