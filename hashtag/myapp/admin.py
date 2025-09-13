from django.contrib import admin
from .models import dataTable
admin.site.register(dataTable)
# User, Hashtag, Usage
# Register your models here.
# admin.site.register(User)
# admin.site.register(Hashtag)
# admin.site.register(Usage)

from django.contrib import admin
from .models import ContactMessage

admin.site.register(ContactMessage)
