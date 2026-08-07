from django.shortcuts import render, redirect
from django.views import View
from projects.forms import ProjectForm
from projects.models import Project
from django.contrib import messages

class ProjectListView(View):
    def get(self, request):
        projs = Project.objects.all()
        return render(request, 'projects/project_list.html', {'projs':projs})
    
    
class AddProjectView(View):
    form_class = ProjectForm
    def get(self, request):
        
        return render(request, 'projects/project_add.html', {'form':self.form_class})   
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            messages.success(request, 'your project added successfully...! ', 'success')
            return redirect('projects:projects_list')
        pass