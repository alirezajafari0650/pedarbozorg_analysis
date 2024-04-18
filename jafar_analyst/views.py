from django.db.models import Q
from django.shortcuts import render
from jafar_analyst.models import Customer, Product, Order, SubOrder
from jafar_jalali import jalali


def dashboard(request):
    return render(request, 'dashboard.html')


def users_list(request):
    '''
    get start date and end date to filter count of shoping for each user
    this view show a table of users data + count of orders for each user in date range
    :param request:
    :return:
    '''
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    persian_start_date = start_date
    persian_end_date = end_date
    search = request.GET.get('search')
    minimum_orders_in_date_range = request.GET.get('minimum_orders_in_date_range')
    # Convert query parameters to Gregorian datetime objects
    if start_date:
        d, m, y = start_date.split('/')
        start_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
    if end_date:
        d, m, y = end_date.split('/')
        end_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
    # Filter transactions by date range
    customers = Customer.objects.all()
    if search:
        customers = customers.filter(Q(name__icontains=search) | Q(phone__icontains=search))
    for customer in customers:
        orders_count = Order.objects.filter(sub_orders__customer=customer)
        if start_date:
            orders_count = orders_count.filter(date__gte=start_date)
        if end_date:
            orders_count = orders_count.filter(date__lte=end_date)
        customer.orders_count = orders_count.distinct().count()
    if minimum_orders_in_date_range:
        customers = [customer for customer in customers if customer.orders_count >= int(minimum_orders_in_date_range)]
    # order customers by orders count
    customers = sorted(customers, key=lambda x: x.orders_count, reverse=True)
    data = {
        'customers': customers,
        'start_date': persian_start_date,
        'end_date': persian_end_date,
        'search': search,
        'minimum_orders_in_date_range': minimum_orders_in_date_range,
    }
    return render(request, 'users_list.html', data)


def user_detail(request, customer_id):
    '''
    show a table of sub orders that have this fields :
    product
    quantity
    persian_date
    sub_order_price
    and filter date with start date and end date
    :param request:
    :param customer_id:
    :return:
    '''
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    persian_start_date = start_date
    persian_end_date = end_date
    customer = Customer.objects.get(id=customer_id)
    sub_orders = SubOrder.objects.filter(customer=customer).order_by('-date')
    if start_date:
        d, m, y = start_date.split('/')
        start_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
        sub_orders = sub_orders.filter(date__gte=start_date)
    if end_date:
        d, m, y = end_date.split('/')
        end_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
        sub_orders = sub_orders.filter(date__lte=end_date)
    data = {
        'sub_orders': sub_orders,
        'customer': customer,
        'start_date': persian_start_date,
        'end_date': persian_end_date,
    }
    return render(request, 'user_detail.html', data)


def products_list(request):
    '''
    show a table of products data + count of orders for each product
    :param request:
    :return:
    '''
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')
    minimum_orders_in_date_range = request.GET.get('minimum_orders_in_date_range')
    products = Product.objects.all()
    persian_start_date = start_date
    persian_end_date = end_date
    if start_date:
        d, m, y = start_date.split('/')
        start_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
    if end_date:
        d, m, y = end_date.split('/')
        end_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
    for product in products:
        orders_count = SubOrder.objects.filter(product=product)
        if start_date:
            orders_count = orders_count.filter(date__gte=start_date)
        if end_date:
            orders_count = orders_count.filter(date__lte=end_date)
        product.orders_count = orders_count.distinct().count()
    if search:
        products = products.filter(name__icontains=search)
    if minimum_orders_in_date_range:
        products = [product for product in products if product.orders_count >= int(minimum_orders_in_date_range)]
    products = sorted(products, key=lambda x: x.orders_count, reverse=True)
    data = {
        'products': products,
        'start_date': persian_start_date,
        'end_date': persian_end_date,
        'search': search,
        'minimum_orders_in_date_range': minimum_orders_in_date_range,
    }
    return render(request, 'products_list.html', data)


def statistics(request):
    '''
    Statistics page (the busiest days of the week in a certain date range - graph of the number of orders in time - customers who made the most purchases in consecutive periods (interval and minimum purchase can be changed))
    :param request:
    :return:
    '''
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    persian_start_date = start_date
    persian_end_date = end_date
    if start_date:
        d, m, y = start_date.split('/')
        start_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
    if end_date:
        d, m, y = end_date.split('/')
        end_date = jalali.Persian(int(y), int(m), int(d)).gregorian_datetime()
    orders = Order.objects.all()
    if start_date:
        orders = orders.filter(date__gte=start_date)
    if end_date:
        orders = orders.filter(date__lte=end_date)
    days = {
        'SATURDAY': 0,
        'SUNDAY': 0,
        'MONDAY': 0,
        'TUESDAY': 0,
        'WEDNESDAY': 0,
        'THURSDAY': 0,
        'FRIDAY': 0,
    }
    for order in orders:
        days[order.weekday] += 1
    top_customers = Customer.objects.all()
    for customer in top_customers:
        orders_count = Order.objects.filter(sub_orders__customer=customer)
        if start_date:
            orders_count = orders_count.filter(date__gte=start_date)
        if end_date:
            orders_count = orders_count.filter(date__lte=end_date)
        customer.orders_count = orders_count.distinct().count()
    top_customers = sorted(top_customers, key=lambda x: x.orders_count, reverse=True)
    top_customers = top_customers[:10]
    orders_plot_data = {}
    for order in orders:
        if order.persian_date in orders_plot_data:
            orders_plot_data[order.persian_date] += 1
        else:
            orders_plot_data[order.persian_date] = 1
    sorted_orders_plot_data = sorted(orders_plot_data.items(), key=lambda x: x[0])
    #to dict
    orders_plot_data = {}
    for date, count in sorted_orders_plot_data:
        orders_plot_data[date] = count
    data = {
        'days': days,
        'start_date': persian_start_date,
        'end_date': persian_end_date,
        'orders_plot_data': orders_plot_data,
        'top_customers': top_customers,
    }
    return render(request, 'statistics.html', data)


