from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Idea

def authentication_check(user):
    return user.is_authenticated

def login(request):
    return render(request, 'storm/login.html')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def home(request):
    creator_name = request.user.get_full_name
    creator_email = request.user.email
    return render(request, 'storm/home.html', {"creator_email":creator_email, "creator_name":creator_name})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def logout_user(request):
    logout(request)
    return redirect('storm:login')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def idea_submit(request):
    if request.method =="POST":
        # Creator Details
        idea_creator_name = request.user.first_name
        idea_creator_mail = request.user.email

        # Idea Details
        idea_title = request.POST.get("idea_title")
        idea_description = request.POST.get("idea_description")
        idea_duration = request.POST.get("idea_duration")
        idea_file = request.FILES.get('idea_file')
        print(idea_creator_name)
        # Save Idea
        Idea.objects.create(idea_creator_name=idea_creator_name, 
                            idea_creator_mail=idea_creator_mail,
                            idea_title=idea_title, 
                            idea_description=idea_description, 
                            idea_duration=idea_duration, 
                            idea_file=idea_file,)
                        
        return redirect('storm:home')
    return redirect('storm:home')

