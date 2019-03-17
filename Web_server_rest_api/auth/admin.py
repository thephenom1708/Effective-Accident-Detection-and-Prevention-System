from django.contrib import admin
from .models import User, Organisation, AccidentLocation
# Register your models here.
admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(AccidentLocation)