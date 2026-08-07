from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            "title",
            "description",
            "members",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # title
        self.fields["title"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter project title",
        })

        # description
        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter project description",
            "rows": 5,
        })

        # members
        self.fields["members"].widget.attrs.update({
            "class": "selectpicker",
            "data-live-search": "true",
            "data-width": "100%",
            "data-actions-box": "true",
            "data-selected-text-format": "count > 2",
            "title": "Select members",
        })
        self.fields["members"].required = True