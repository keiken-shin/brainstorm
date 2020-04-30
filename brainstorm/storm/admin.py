from django.contrib import admin

from .models import Improvement_Area, Impact, Judge, Idea, Comment

admin.site.site_header = 'Brainstorm Admin'
admin.site.site_title = 'Brainstorm Admin Area'
admin.site.index_title = 'Welcome to Brainstorm Admin Area'

admin.site.register(Improvement_Area)
admin.site.register(Impact)
admin.site.register(Judge)
admin.site.register(Idea)
admin.site.register(Comment)