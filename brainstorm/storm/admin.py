from django.contrib import admin

from .models import Judge, Idea

admin.site.site_header = 'Brainstorm Admin'
admin.site.site_title = 'Brainstorm Admin Area'
admin.site.index_title = 'Welcome to Brainstorm Admin Area'

admin.site.register(Judge)
admin.site.register(Idea)
