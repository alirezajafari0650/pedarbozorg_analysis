from jafar_analyst.models import Order, SubOrder, Product, Customer, Category


def clean_models():
    Order.objects.all().delete()
    SubOrder.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    Category.objects.all().delete()
    print('All models cleaned')


def read_xlsx(file_path):
    import pandas as pd
    df = pd.read_excel(file_path)
    return df


columns = ['ردیف', 'نام شخص', 'فاکتور', 'تاریخ', 'کد', 'شرح', 'تعداد', 'فی خالص', 'جمع ردیف', 'فروشگاه', 'فروشنده', 'نوع', 'راس گیری']


def fill_customers(i, df):
    if '_' in str(df['نام شخص'][i]):
        name, phone = str(df['نام شخص'][i]).split('_')
        customer = Customer.objects.filter(phone=phone).first()
        if not customer:
            Customer.objects.create(name=name, phone=phone)
            print(f'Customer {name} created')


def fill_products(i, df):
    name = df['شرح'][i]
    price = float(df['فی خالص'][i])
    product_code = int(df['کد'][i])
    if str(name) != 'nan':
        if not Product.objects.filter(product_code=product_code).exists():
            Product.objects.create(name=name, price=price, product_code=product_code)
            print(f'Product {name} created')


def fill_orders_and_suborders(i, df):
    product_code = int(df['کد'][i])
    factor_number = df['فاکتور'][i]
    quantity = float(df['تعداد'][i])
    persian_date = df['تاریخ'][i]
    sub_order_price = float(df['جمع ردیف'][i])
    customer_phone = str(df['نام شخص'][i])
    if '_' in customer_phone:
        customer_phone = customer_phone.split('_')[1]
        product = Product.objects.filter(product_code=product_code).first()
        if not product:
            print(f'Product with code {product_code} not found')
        else:
            customer = Customer.objects.filter(phone=customer_phone).first()
            if not customer:
                print(f'Customer with phone {customer_phone} not found')
            else:
                sub_order = SubOrder.objects.create(customer=customer, product=product, quantity=quantity, persian_date=persian_date, sub_order_price=sub_order_price)
                order = Order.objects.filter(factor_number=factor_number).first()
                if not order:
                    order = Order.objects.create(factor_number=factor_number, persian_date=persian_date)
                order.sub_orders.add(sub_order)
                order.save()
                print(f'SubOrder {sub_order} added to Order {order}')


def fill_models(file_path):
    clean_models()
    df = read_xlsx(file_path)
    execeptions = []
    for i in range(len(df)):
        try:
            fill_customers(i, df)
            fill_products(i, df)
            fill_orders_and_suborders(i, df)
        except Exception as e:
            detail = f'Row {i}: {e}'
            execeptions.append(detail)
    print('All models filled')
    print('{} exceptions occured'.format(len(execeptions)))
    for e in execeptions:
        print(e)
        print('')
        print('-' * 50)


path = '/home/jafar/PycharmProjects/pedarbozorg_analysis/گزارش فروش کل.xlsx'
fill_models(path)
