from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Idea, Judge, Judgeselection

def authentication_check(user):
    return user.is_authenticated

def login(request):
    if request.user.is_authenticated:
        return redirect('storm:home')
    return render(request, 'storm/login.html')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def logout_user(request):
    logout(request)
    return redirect('storm:login')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def home(request):
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.all().order_by('-id')
    return render(request, 'storm/home.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def idea(request, id):
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.filter(id__iexact = id)
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/idea.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def idea_form(request):
    creator_name = request.user.first_name
    creator_email = request.user.email
    return render(request, 'storm/form.html', {"creator_email":creator_email, "creator_name":creator_name})

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

        # Save Idea
        obj = Idea.objects.create(idea_creator_name=idea_creator_name,
                            idea_creator_mail=idea_creator_mail,
                            idea_title=idea_title, 
                            idea_description=idea_description, 
                            idea_duration=idea_duration, 
                            idea_file=idea_file,)
        send_mail(f'Your ID is {obj.id}',
                  'Hi,\n\nYour Idea is received.', settings.EMAIL_HOST_USER,[request.user.email])
                        
        return redirect('storm:home')
    return redirect('storm:home')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def selection(request, id):
    if request.method =="POST":
        # Accept/Reject
        idea_remark = request.POST.get("idea_remark")
        idea_status = request.POST.get("idea_status")

        # Update Status and Remark
        Idea.objects.filter(pk=id).update(idea_remark=idea_remark, idea_status=idea_status)
        send_mail(f'Your Idea is {idea_status}',f'Hi,\n\nremarks on your idea is {idea_remark}.', settings.EMAIL_HOST_USER, [request.user.email])
        return redirect('storm:idea', id=id)
    return redirect('storm:home')


def jury(request):
    ideas = Idea.objects.all()
    return render(request, 'storm/jury.html', {'ideas':ideas})