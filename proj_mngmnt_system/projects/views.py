from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from projects.forms import ProjectForm
from projects.models import Project


class ProjectListView(LoginRequiredMixin, View):

    def get(self, request):
        projects = Project.objects.filter(
            Q(owner=request.user) |
            Q(members=request.user)
        ).distinct()

        return render(
            request,
            "projects/project_list.html",
            {"projs": projects}
        )


class AddProjectView(LoginRequiredMixin, View):
    form_class = ProjectForm

    def get(self, request):
        form = self.form_class()

        return render(
            request,
            "projects/project_add.html",
            {"form": form}
        )

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = form.save(commit=False)

            project.owner = request.user
            project.save()

            # ذخیره ManyToMany یعنی members
            form.save_m2m()

            messages.success(
                request,
                "Your project was added successfully."
            )

            return redirect("projects:projects_list")

        return render(
            request,
            "projects/project_add.html",
            {"form": form}
        )


class ProjectDetailView(LoginRequiredMixin, View):

    def get(self, request, proj_id):

        projects = Project.objects.filter(
            Q(owner=request.user) |
            Q(members=request.user)
        ).distinct()

        project = get_object_or_404(
            projects,
            id=proj_id
        )

        return render(
            request,
            "projects/project_detail.html",
            {"project": project}
        )


class ProjectUpdateView(LoginRequiredMixin, View):
    form_class = ProjectForm

    def get_project(self, request, proj_id):
        return get_object_or_404(
            Project,
            id=proj_id,
            owner=request.user
        )

    def get(self, request, proj_id):
        project = self.get_project(request, proj_id)

        form = self.form_class(
            instance=project
        )

        return render(
            request,
            "projects/project_edit.html",
            {
                "project": project,
                "form": form,
            }
        )

    def post(self, request, proj_id):
        project = self.get_project(request, proj_id)

        form = self.form_class(
            request.POST,
            instance=project
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Project edited successfully."
            )

            return redirect(
                "projects:projects_detail",
                proj_id=project.id
            )

        return render(
            request,
            "projects/project_edit.html",
            {
                "project": project,
                "form": form,
            }
        )


class ProjectDeleteView(LoginRequiredMixin, View):

    def get_project(self, request, proj_id):
        return get_object_or_404(
            Project,
            id=proj_id,
            owner=request.user
        )

    def get(self, request, proj_id):
        project = self.get_project(request, proj_id)

        return render(
            request,
            "projects/project_delete.html",
            {"project": project}
        )

    def post(self, request, proj_id):
        project = self.get_project(request, proj_id)

        project.delete()

        messages.success(
            request,
            "Project deleted successfully."
        )

        return redirect("projects:projects_list")