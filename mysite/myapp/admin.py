from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.


# Client model registered
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'city', 'get_categories']
    

admin.site.register(Client, ClientAdmin)


# Product model registered
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'stock' ]
    actions = ['update_products']
    
    def update_products(self, request, queryset):
        for product in queryset:
            product.stock = product.stock + 50
            product.save()
        self.message_user(request, "Successfully Updated product stock")
    update_products.short_description = "Update Product stock to 50 "


admin.site.register(Product, ProductAdmin)


# Order model registered
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_product_name', 'get_client_name', 'num_units', 'order_status', 'status_date'] 

    def get_product_name(self, obj):
        return '{}'.format(obj.product.name)

    get_product_name.short_description = 'Product Name'
    
    def get_client_name(self, obj):
        return '{} {}'.format(obj.client.first_name, obj.client.last_name)

    get_client_name.short_description = 'Client Name'


admin.site.register(Order, OrderAdmin)


# Category model registered
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'warehouse'] 


admin.site.register(Category, CategoryAdmin)
