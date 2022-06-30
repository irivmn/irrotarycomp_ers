from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(HCA_details)
admin.site.register(users)
admin.site.register(Registration_Approval)
admin.site.register(Reset_password_Approval)
admin.site.register(CD26_airend_data)
admin.site.register(CD26_airend_data_rated)