from django.contrib import admin
from planning.models import Destination, Attraction

admin.site.register(Destination, admin.ModelAdmin)
admin.site.register(Attraction, admin.ModelAdmin)
