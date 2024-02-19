from django.contrib import admin

# Register your models here.
from customer.models import *

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
