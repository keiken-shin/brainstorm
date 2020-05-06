from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Idea, Judge, Impact, Improvement_Area, Idea_QC, Comment
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

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
    try:
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master"', con=engine)
        df = df_aws[['Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting']]
        df.columns = ['email', 'dept', 'location', 'first_level', 'second_level']
    except:
        data = [['anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Sanjeev Rathore', 'Sanjeev Agarwal']]
        df = pd.DataFrame(data, columns = ['email', 'dept', 'location', 'first_level', 'second_level']) 
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.all().order_by('-id')
    new_ideas = [i.idea_id for i in Idea_QC.objects.all()]
    selected_ideas = [i.idea_id for i in Idea_QC.objects.filter(idea_qc_status='Accepted')]
    your_idea = Idea.objects.filter(idea_creator_mail=user_email)
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/home.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges, "new_ideas":new_ideas, "selected_ideas":selected_ideas, "your_idea":your_idea, "df":df})

@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def idea(request, id):
    try:
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master"', con=engine)
        df = df_aws[['Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting']]
        df.columns = ['email', 'dept', 'location', 'first_level', 'second_level']
    except:
        data = [['anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Sanjeev Rathore', 'Sanjeev Agarwal']]
        df = pd.DataFrame(data, columns = ['email', 'dept', 'location', 'first_level', 'second_level']) 
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.filter(pk = id)
    idea_qc_id = [i.idea_id for i in Idea_QC.objects.all()]
    idea_qc = [i for i in Idea_QC.objects.filter(idea_id=id)]
    comments = Comment.objects.filter(comment_id=id).order_by('-id')
    judges = [i.judge_mail for i in Judge.objects.all()]
    return render(request, 'storm/idea.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges, "idea_qc_id":idea_qc_id, "idea_qc":idea_qc, "comments":comments, "df":df})

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
        send_mail(f'Your ID is {obj.id}',
                  'Hi,\n\nYour Idea is received.', settings.EMAIL_HOST_USER,[request.user.email])
                        
        return redirect('storm:home')
    return redirect('storm:home')

# Accept or Reject IDEA_QC
@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def selection(request, id):
    if request.method =="POST":
        # Creator Detail
        idea_qc_name = request.user.first_name
        idea_qc_mail = request.user.email

        # Accept/Reject
        idea_id = id
        idea_join = Idea.objects.get(pk=id)
        idea_qc_remark = request.POST.get("idea_qc_remark")
        idea_qc_status = request.POST.get("idea_qc_status")

        # Create QC status
        Idea_QC.objects.create(idea_id=idea_id,
                            idea_qc_name=idea_qc_name,
                            idea_qc_mail=idea_qc_mail,
                            idea_join=idea_join,
                            idea_qc_remark=idea_qc_remark,
                            idea_qc_status=idea_qc_status
                            )
        send_mail(f'Your Idea is {idea_status}',f'Hi,\n\nremarks on your idea is {idea_remark}.', settings.EMAIL_HOST_USER, [idea_creator_mail])
        
        return redirect('storm:idea', id=id)
    return redirect('storm:home')

# Comment Data
@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def comment(request, id):
    if request.method == 'POST':
        # Creator Detail
        commenter_name = request.user.first_name
        commenter_mail = request.user.email

        # Get Comment
        comment_id = id
        comment = request.POST.get("comment")
        comment_join = Idea.objects.get(pk=id)

        # Create comment object
        Comment.objects.create(comment_id=comment_id,
                            commenter_name=commenter_name,
                            commenter_mail=commenter_mail,
                            comment_join=comment_join,
                            comment=comment
                            )
        
        return HttpResponse('')
    return redirect('storm:idea', id=id)

# Update Idea Status
@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def status(request, id):
    if request.method == 'POST':
        idea_close_date = datetime.now()
        idea_status = request.POST.get('idea_status')

        # Update
        Idea.objects.filter(pk=id).update(idea_close_date=idea_close_date, idea_status=idea_status)
        return HttpResponse('')
    return redirect('storm:idea', id=id)

# All Ideas
@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
def jury(request):
    try:
        engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
        df_aws = pd.read_sql_query('select * from "headcount_master"', con=engine)
        df = df_aws[['Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting']]
        df.columns = ['email', 'dept', 'location', 'first_level', 'second_level']
    except:
        data = [['anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Sanjeev Rathore', 'Sanjeev Agarwal']]
        df = pd.DataFrame(data, columns = ['email', 'dept', 'location', 'first_level', 'second_level']) 
    user_name = request.user.first_name
    user_email = request.user.email
    ideas = Idea.objects.all()
    judges = [i.judge_mail for i in Judge.objects.all()]
    all_ideas = Idea_QC.objects.all()
    return render(request, 'storm/jury.html', {"user_email":user_email, "user_name":user_name, "ideas":ideas, "judges":judges, "all_ideas":all_ideas, "df":df})


@user_passes_test(authentication_check, login_url='/', redirect_field_name=None)
@csrf_exempt
def filterdate(request):
    if request.method == 'POST':
        try:
            engine = create_engine('postgresql://analytics:analytics@123@ec2-34-246-108-106.eu-west-1.compute.amazonaws.com:5432/iadatabase')
            df_aws = pd.read_sql_query('select * from "headcount_master"', con=engine)
            df = df_aws[['Email Id', 'Sub-Department', 'DF Site', '1st Level Reporting', '2nd Level Reporting']]
            df.columns = ['email', 'dept', 'location', 'first_level', 'second_level']
        except:
            data = [['anubhav.kumar27@gmail.com', 'Analytics', 'Noida', 'Sanjeev Rathore', 'Sanjeev Agarwal']]
            df = pd.DataFrame(data, columns = ['email', 'dept', 'location', 'first_level', 'second_level']) 

        datepicker = request.POST.get('datepicker')
        datepicker = datepicker.split(' - ')
        date_from = datepicker[0].split('/')
        date_from = date_from[2] + '-' + date_from[0] + '-' + date_from[1]
        date_to = datepicker[1].split('/')
        date_to = date_to[2] + '-' + date_to[0] + '-' + date_to[1]
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')

        judges = [i.judge_mail for i in Judge.objects.all()]
        user_name = request.user.first_name
        user_email = request.user.email
        ideas = Idea.objects.filter(idea_creation_date__date__range=(date_from, date_to))
        all_ideas = Idea_QC.objects.all()
        print(all_ideas)
        return render(request, 'storm/jury.html', {"judges":judges, "user_name":user_name, "user_email":user_email, "ideas":ideas, "all_ideas":all_ideas, "df":df})
    return redirect('storm:jury')