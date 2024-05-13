from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ("kembangan", "kembangan"),
    ("Menteng", "Menteng"),
    ("Cakung", "Cakung"),
    ("Cengkareng", "Cengkareng"),
    ("Cilandak", "Cilandak"),
    ("Cilincing", "Cilincing"),
    ("Cipayung", "Cipayung"),
    ("Ciracas", "Ciracas"),
    ("Duren Sawit", "Duren Sawit"),
    ("Gambir", "Gambir"),
    ("Grogol Petamburan", "Grogol Petamburan"),
    ("Jagakarsa", "Jagakarsa"),
    ("Jatinegara", "Jatinegara"),
    ("Johar Baru", "Johar Baru"),
    ("Kalideres", "Kalideres"),
    ("Kebayoran Baru", "Kebayoran Baru"),
    ("Kebayoran Lama", "Kebayoran Lama"),
    ("Kebon Jeruk", "Kebon Jeruk"),
    ("Kelapa Gading", "Kelapa Gading"),
    ("Kemayoran", "Kemayoran"),
)

CATEGORY_CHOICES = (
    ("OS", "Oatside Series"),
    ("NB", "Non-Coffe Beverage"),
    ("LS", "Latte Series"),
    ("AS", "Aren Series"),
    ("BS", "Bakery Series"),
)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default="")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="product")
    prodapp = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name


STATE_CHOICES = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel"),
    ("Pending", "Pending"),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_id


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

