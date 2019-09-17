from django.contrib import admin
from .models import *

# Register your models here.

#do this line multiple times for all models (maybe a loop -_o_-)
admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(Dish)
admin.site.register(Invoice)
admin.site.register(CreditCard)
admin.site.register(Comment)
admin.site.register(TypeDish)
admin.site.register(Content)
#admin.site.register(Allergen)
#admin.site.register(AllergenDish)
admin.site.register(Order)
admin.site.register(OrderStatus)

