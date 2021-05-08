from django.contrib import admin
from . import models
from django.contrib.auth.models import Group, User

admin.site.site_header = "Ecommerce Admin Section"
admin.site.index_title = "Welcome to Ecommerce admin area"

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (('name', 'price'), 'stock', 'image')
    list_editable = ['price', 'stock']
    list_display = ("name", "price", "stock")
    

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["name", "email"]
 
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "date_oredered", "complete", "cancel")
    list_display_links = ['customer','date_oredered']
    list_filter = ("date_oredered", )
    empty_value_display = '-empty-'
    search_fields = ["customer__name"]
    
    def cancelOrder(modelAdmin, request, queryset):
        queryset.update(is_cancel = 1)
        
class OrderitemAdmin(admin.ModelAdmin):
    list_display = ("order", "date" ,"product", "quantity")
    raw_id_fields = ("order",)


admin.site.unregister(Group)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderitemAdmin)
admin.site.register(models.ShippingAdress)