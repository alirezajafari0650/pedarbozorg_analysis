from jafar_analyst.models import *

customer_count = Customer.objects.count()
product_count = Product.objects.count()
category_count = Category.objects.count()
order_count = Order.objects.count()
sub_order_count = SubOrder.objects.count()
print(f'Customers: {customer_count}')
print(f'Products: {product_count}')
print(f'Categories: {category_count}')
print(f'Orders: {order_count}')
print(f'SubOrders: {sub_order_count}')
