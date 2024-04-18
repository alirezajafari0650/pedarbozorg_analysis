from jafar_analyst.views import users_list,user_detail,products_list,dashboard,statistics
from django.urls import path

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('users_list/', users_list, name='users_list'),
    path('user_detail/<int:customer_id>/', user_detail, name='user_detail'),
    path('products_list/', products_list, name='products_list'),
    path('statistics/', statistics, name='statistics'),
]