from django.contrib import admin
from .models import Partner, ContactUs, Order, Blog, TruckType
from parler.admin import TranslatableAdmin

# Register your models here.

admin.site.register([ContactUs, Partner, Order])

class BlogAdmin(TranslatableAdmin):
    pass

admin.site.register(Blog, BlogAdmin)

class TruckTypeAdmin(TranslatableAdmin):
    pass

admin.site.register(TruckType, TruckTypeAdmin)