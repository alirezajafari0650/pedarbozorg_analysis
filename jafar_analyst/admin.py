from django.contrib import admin
from .models import Category, Customer, Product, SubOrder, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SubOrder)
admin.site.register(Order)


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['phone', 'name']

    # when a customer delete , delete all orders with empty suborders
    def delete_model(self, request, obj):
        orders = Order.objects.all()
        for order in orders:
            if not order.sub_orders.all():
                order.delete()
        obj.delete()


admin.site.register(Customer, CustomerAdmin)
