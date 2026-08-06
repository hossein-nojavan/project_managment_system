from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

        placeholders = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "password1": "Password",
            "password2": "Repeat Password",
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control form-control-user",
                "placeholder": placeholders[field_name],
            })

        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email address already exists."
            )

        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-user", "placeholder":"Username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control form-control-user", "placeholder":"Password"}))