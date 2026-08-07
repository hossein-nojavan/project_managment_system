from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "owner__username",
    )

    filter_horizontal = (
        "members",
    )