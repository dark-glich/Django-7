from django.contrib import admin
from . import models


admin.site.site_header = "Ecommerce Admin Section"
admin.site.index_title = "Welcome to Ecommerce admin area"

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")
    
class OrderAdmin(admin.ModelAdmin):
     list_display = ("customer", "date_oredered", "complete", "cancel")
     list_filter = ("customer", )
     
     def cancelOrder(modelAdmin, request, queryset):
          queryset.update(is_cancel = 1)
     

admin.site.register(models.Customer)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAdress)