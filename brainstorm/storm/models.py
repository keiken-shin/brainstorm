from django.db import models

# Improvement Areas List for Idea
class Improvement_Area(models.Model):
    area_title = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.area_title 

# Impact 
class Impact(models.Model):
    impact = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.impact

# Judge Addition
class Judge(models.Model):
    judge_name = models.CharField(max_length=200, null=False, blank=False)
    judge_mail = models.EmailField(default=None, null=False, blank=False)

    def __str__(self):
        return self.judge_name

# Idea Submission
class Idea(models.Model):
    # Autofill Details
    idea_creator_name = models.CharField(max_length=200, null=True, blank=True)
    idea_creator_mail = models.EmailField(default=None, null=False, blank=False)
    idea_creation_date = models.DateTimeField(auto_now_add=True)

    # User Filled Details
    idea_improvement = models.CharField(default=None, max_length=200, null=False, blank=False)
    idea_title = models.CharField(default=None, max_length=200, null=False, blank=False)
    idea_description = models.TextField(default=None, null=True, blank=True)
    idea_impact = models.CharField(default=None, max_length=200, null=False, blank=False)
    idea_file = models.FileField(upload_to='', blank=True)

    # Judge Status
    idea_status = models.CharField(max_length=200, default=None, null=True, blank=True, choices=[('WIP', 'WIP'), ('Implemented', 'Implemented'), ('Hold', 'Hold'), ('Cancel', 'Cancel'), ('Close', 'Close')])

    def __str__(self):
        return self.idea_title

# QC Status for Idea
class Idea_QC(models.Model):
    # Same id as of idea
    idea_id = models.IntegerField(default=0, null=False, blank=False)
    
    # Autofill Details
    idea_qc_name = models.CharField(max_length=200, null=True, blank=True)
    idea_qc_mail = models.EmailField(default=None, null=False, blank=False)
    idea_qc_date = models.DateTimeField(auto_now_add=True)

    # QC Details
    idea_qc_remark = models.TextField(default=None, null=True, blank=True)
    idea_qc_status = models.CharField(max_length=200, default='Pending', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')])

    def __str__(self):
        return self.idea_id

# Comment Section
class Comment(models.Model):
    # Same id as of idea
    comment_id = models.IntegerField(default=0, null=False, blank=False)

    # Autofill Details
    commenter_name = models.CharField(max_length=200, null=True, blank=True)
    commenter_mail = models.EmailField(default=None, null=False, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)

    # Comment
    comment = models.TextField(default=None, null=False, blank=False)

    def __str__(self):
        return (self.comment_id, self.commenter_name)