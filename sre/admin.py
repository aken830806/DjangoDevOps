from django.contrib import admin
from .models import GitServer, RepositoryNotify

admin.site.register(GitServer)
admin.site.register(RepositoryNotify)
