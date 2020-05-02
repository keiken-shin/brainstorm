from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Idea, Judge, Impact, Improvement_Area, Idea_QC, Comment
from datetime import datetime

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
    new_ideas = [i.idea_id for i in Idea_QC.objects.all()]
    selected_ideas = [i.idea_id for i in Idea_QC.objects.filter(idea_qc_status='Accepted')]
    your_idea_mail = [i.idea_creator_mail for i in Idea.objects.all()]
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/home.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges, "new_ideas":new_ideas, "selected_ideas":selected_ideas, "your_idea_mail":your_idea_mail})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def idea(request, id):
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.filter(id__iexact = id)
    idea_qc_id = [i.idea_id for i in Idea_QC.objects.all()]
    idea_qc = [i for i in Idea_QC.objects.filter(idea_id=id)]
    comments = Comment.objects.filter(comment_id=id).order_by('-id')
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/idea.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges, "idea_qc_id":idea_qc_id, "idea_qc":idea_qc, "comments":comments})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def idea_form(request):
    user_name = request.user.first_name
    user_email = request.user.email
    creator_name = request.user.first_name
    creator_email = request.user.email
    impact = Impact.objects.all().order_by('id')
    improvement = Improvement_Area.objects.all().order_by('id')
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/form.html', {"user_email":user_email, "user_name":user_name, "creator_email":creator_email, "creator_name":creator_name, "impact":impact, "improvement":improvement, "judges":judges})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def idea_submit(request):
    if request.method =="POST":
        # Creator Details
        idea_creator_name = request.user.first_name
        idea_creator_mail = request.user.email

        # Idea Details
        idea_improvement = request.POST.get("idea_improvement")
        idea_title = request.POST.get("idea_title")
        idea_description = request.POST.get("idea_description")
        idea_impact = request.POST.get("idea_impact")
        idea_file_1 = request.FILES.get('idea_file_1')
        idea_file_2 = request.FILES.get('idea_file_2')
        idea_file_3 = request.FILES.get('idea_file_3')
        idea_file_4 = request.FILES.get('idea_file_4')
        idea_file_5 = request.FILES.get('idea_file_5')

        # Save Idea
        obj = Idea.objects.create(idea_creator_name=idea_creator_name,
                            idea_creator_mail=idea_creator_mail,
                            idea_improvement=idea_improvement,
                            idea_title=idea_title, 
                            idea_description=idea_description, 
                            idea_impact=idea_impact, 
                            idea_file_1=idea_file_1,
                            idea_file_2=idea_file_2,
                            idea_file_3=idea_file_3,
                            idea_file_4=idea_file_4,
                            idea_file_5=idea_file_5,
                            )
        # send_mail(f'Your ID is {obj.id}',
        #           'Hi,\n\nYour Idea is received.', settings.EMAIL_HOST_USER,[request.user.email])
                        
        return redirect('storm:home')
    return redirect('storm:home')

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def selection(request, id):
    if request.method =="POST":
        # Creator Detail
        idea_qc_name = request.user.first_name
        idea_qc_mail = request.user.email

        # Accept/Reject
        idea_id = id
        idea_qc_remark = request.POST.get("idea_qc_remark")
        idea_qc_status = request.POST.get("idea_qc_status")

        # Create QC status
        Idea_QC.objects.create(idea_id=idea_id,
                            idea_qc_name=idea_qc_name,
                            idea_qc_mail=idea_qc_mail,
                            idea_qc_remark=idea_qc_remark,
                            idea_qc_status=idea_qc_status
                            )
        # send_mail(f'Your Idea is {idea_status}',f'Hi,\n\nremarks on your idea is {idea_remark}.', settings.EMAIL_HOST_USER, [idea_creator_mail])
        
        return redirect('storm:idea', id=id)
    return redirect('storm:home')

# Comment Data
def comment(request, id):
    if request.method == 'POST':
        # Creator Detail
        commenter_name = request.user.first_name
        commenter_mail = request.user.email

        # Get Comment
        comment_id = id
        comment = request.POST.get("comment")

        # Create comment object
        Comment.objects.create(comment_id=comment_id,
                            commenter_name=commenter_name,
                            commenter_mail=commenter_mail,
                            comment=comment
                            )
        
        return HttpResponse('')
    return redirect('storm:idea', id=id)

# Update Idea Status
def status(request, id):
    if request.method == 'POST':
        idea_close_date = datetime.now()
        idea_status = request.POST.get('idea_status')

        # Update
        Idea.objects.filter(pk=id).update(idea_close_date=idea_close_date, idea_status=idea_status)
        return HttpResponse('')
    return redirect('storm:idea', id=id)

# Add Judge
def jury(request):
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.all()
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/jury.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges})

