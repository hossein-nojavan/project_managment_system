from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegisterForm, UserLoginForm

from django.contrib.auth import logout



class RegisterView(View):
    template_name = "account/register.html"

    def get(self, request):
        form = UserRegisterForm()

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data["password1"],
            )

            if authenticated_user is not None:
                login(request, authenticated_user)

                messages.success(
                    request,
                    "Your account was created successfully.",
                )

                return redirect("home:home")

            messages.error(
                request,
                "Your account was created, but automatic login failed.",
            )

        return render(
            request,
            self.template_name,
            {"form": form},
        )
        
class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    
    def setup(self,request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)       
    
    def dispatch(self,request, *args, **kwargs):
        if self.request.user.is_authenticated:
           return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)       
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name , {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password1'])
            if user is not None:
                login(request,user)

                messages.success(request,'You logged in successfully','success')
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            form.add_error(None,'username/password is wrong')
        return render(request, self.template_name , {'form':form})

        
        
class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.", 'success')
        return redirect("home:home")