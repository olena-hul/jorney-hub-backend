from django.contrib import admin
from authentication.models import User, Role

admin.site.register(User, admin.ModelAdmin)
admin.site.register(Role, admin.ModelAdmin)
