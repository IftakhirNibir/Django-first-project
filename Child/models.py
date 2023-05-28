from email.policy import default
from django.db import models
from django.contrib.auth.models import  User
from django.db.models.fields import DateTimeField
from sympy import true

# Create your models here.


class Customer(models.Model):
    profile_pic = models.ImageField(default="user.jpg",null=True, blank=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=13,null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
	    return str(self.username) if self.username else ''


class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name

class Help(models.Model):
    childname = models.CharField(max_length=122)
    address = models.CharField(max_length=122)
    contact = models.CharField(max_length=12)
    desc = models.TextField()
    account = models.CharField(max_length=20,null=True)

    def __str__(self) -> str:
        return self.childname

class Daycare(models.Model):
    organization_name =models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    service_time = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    approved = models.BooleanField('Approved',default=False)
    
class District(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return str(self.name)

class School(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)

	def __str__(self):
		return str(self.name)

class Schooldetails(models.Model):
    childname = models.CharField(max_length=122,null=True)
    district = models.ForeignKey(District, null=True, on_delete= models.SET_NULL)
    school = models.ForeignKey(School, null=True, on_delete= models.SET_NULL)
    contact_no = models.CharField(max_length=200)

class Product(models.Model):

	package_name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)

	def __str__(self):
		return self.package_name

class Order(models.Model):
    Payment = (
        ('Paid','paid'),
    )
    STATUS = (
			('pending', 'pending'),
			('delivered', 'delivered'),
			)

    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    payment_status = models.CharField(max_length=200, null=True, choices=Payment)
	
    def __str__(self):
	    return str(self.product.package_name) if self.product.package_name else ''

class DiscussionTopic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Discussion(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    more = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    participants =models.ManyToManyField(User, related_name="participants", blank=True)

    def __str__(self):
        return self.name

    class Meta:
       ordering = ['-updated', '-created']


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

class BkashPayment(models.Model):
	OPTION = (
			('Donation', 'Donation'),
			('Product Cost', 'Product Cost'),
			)

	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, blank=True)
	option = models.CharField(max_length=200, choices=OPTION)
	product_name_and_quentity = models.CharField(max_length=100, null=True, blank=True)
	bkashNumber = models.CharField(max_length=20)
	Transaction_ID = models.CharField(max_length=512)
	created_time = models.DateTimeField(auto_now_add=True,null=True)

class NagadPayment(models.Model):
	OPTION = (
			('Donation', 'Donation'),
			('Product Cost', 'Product Cost'),
			)

	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, blank=True)
	option = models.CharField(max_length=200, choices=OPTION)
	product_name_and_quentity = models.CharField(max_length=100, null=True, blank=True)
	nagadNumber = models.CharField(max_length=20)
	Transaction_ID = models.CharField(max_length=512)
	created_time = models.DateTimeField(auto_now_add=True,null=True)