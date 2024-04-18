from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام دسته بندی')

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    phone = models.CharField(max_length=11, verbose_name='تلفن', unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام محصول')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت برحسب ریال')
    sold_count = models.FloatField(verbose_name='تعداد فروخته شده', default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته بندی', null=True, blank=True)
    product_code = models.IntegerField(verbose_name='کد محصول', unique=True)

    def __str__(self):
        return self.name


class SubOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='مشتری')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.FloatField(verbose_name='تعداد')
    date = models.DateTimeField(verbose_name='تاریخ')
    persian_date = models.CharField(max_length=10, verbose_name='تاریخ شمسی')
    sub_order_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='قیمت کل')

    def __str__(self):
        return f"{self.customer} - {self.product} - {self.quantity}"

    def set_date(self):
        if not self.date and self.persian_date:
            from jafar_jalali.jalali import Persian
            y, m, d = [int(i) for i in self.persian_date.split('/')]
            self.date = Persian(y, m, d).gregorian_datetime()

    def save(self, *args, **kwargs):
        self.set_date()
        return super(SubOrder, self).save(*args, **kwargs)


class Order(models.Model):
    sub_orders = models.ManyToManyField(SubOrder, verbose_name='سفارشات')
    date = models.DateTimeField(verbose_name='تاریخ')
    persian_date = models.CharField(max_length=10, verbose_name='تاریخ شمسی')
    total_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='قیمت کل', null=True, blank=True)
    factor_number = models.CharField(max_length=255, verbose_name='شماره فاکتور', unique=True)
    total_quantity = models.FloatField(verbose_name='تعداد کل', null=True, blank=True)
    WEEKDAYS = [
        ('SATURDAY', 'شنبه'),
        ('SUNDAY', 'یکشنبه'),
        ('MONDAY', 'دوشنبه'),
        ('TUESDAY', 'سه شنبه'),
        ('WEDNESDAY', 'چهارشنبه'),
        ('THURSDAY', 'پنجشنبه'),
        ('FRIDAY', 'جمعه'),
    ]
    weekday = models.CharField(max_length=9, choices=WEEKDAYS, verbose_name='روز هفته')

    def __str__(self):
        return f"{self.date}"

    def set_total_quantity(self):
        if self.id:
            self.total_quantity = sum([sub_order.quantity for sub_order in self.sub_orders.all()])

    def set_total_price(self):
        if self.id:
            self.total_price = sum([sub_order.sub_order_price for sub_order in self.sub_orders.all()])

    def set_date(self):
        if not self.date and self.persian_date:
            from jafar_jalali.jalali import Persian
            y, m, d = [int(i) for i in self.persian_date.split('/')]
            self.date = Persian(y, m, d).gregorian_datetime()

    def set_weekday(self):
        if self.date:
            self.weekday = self.date.strftime('%A').upper()

    def save(self, *args, **kwargs):
        self.set_date()
        self.set_weekday()
        self.set_total_price()
        self.set_total_quantity()
        return super(Order, self).save(*args, **kwargs)
