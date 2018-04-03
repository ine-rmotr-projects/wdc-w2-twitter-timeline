from django.contrib import admin

from .models import Tweet, Relationship, User

admin.site.register(Tweet)
admin.site.register(Relationship)
admin.site.register(User)
