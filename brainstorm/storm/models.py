from django.db import models

class Judge(models.Model):
    judge_name = models.CharField(max_length=200, null=False, blank=False)
    judge_mail = models.EmailField(default=None, null=False, blank=False)

    def __str__(self):
        return self.judge_name

class Idea(models.Model):
    # Autofill Details
    idea_creator_name = models.CharField(max_length=200, null=True, blank=True)
    idea_creator_mail = models.EmailField(default=None, null=False, blank=False)
    idea_creation_date = models.DateTimeField(auto_now_add=True)

    # User Filled Details
    idea_title = models.CharField(max_length=200)
    idea_description = models.TextField(default=None, null=True, blank=True)
    idea_duration = models.IntegerField(default=0, null=True, blank=True)
    idea_file = models.FileField(upload_to='', blank=True)

    # Judge Selection
    idea_status = models.CharField(max_length=200, default='Pending', choices=[('Pending', 'Pending'), ('WIP', 'WIP'), ('Accepted', 'Accepted'), ('Completed', 'Completed')])

    def __str__(self):
        return self.idea_title

class Judgeselection(models.Model):
    idea_status = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.idea_status