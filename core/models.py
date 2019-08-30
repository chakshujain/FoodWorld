from django.db import models
from django.contrib.auth import get_user_model


# class User(auth.models.User,auth.models.PermissionsMixin):
#
#     def __str__(self):
#         return self.username

class DishOriginCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SpicynessCategory(models.Model):
    name = models.CharField(max_length = 10)
    def __str__(self):
        return self.name

class VegginessCategory(models.Model):
    name = models.CharField(max_length = 10)
    def __str__(self):
        return self.name

class StartersOrMaincourseCategory(models.Model):
    name = models.CharField(max_length = 20)
    def __str__(self):
        return self.name
class Reviews(models.Model):
    name = models.CharField(max_length = 50)
    review = models.CharField(max_length = 500)

class Dish(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length = 1000,default = "Description of the dish")
    dishOrigin = models.ForeignKey(DishOriginCategory, on_delete=models.CASCADE,blank = True,null = True)
    spicyness  = models.ForeignKey(SpicynessCategory, on_delete=models.CASCADE,blank = True,null = True)
    vegginess =  models.ForeignKey(VegginessCategory, on_delete=models.CASCADE,blank = True,null = True)
    startersOrMaincourse = models.ForeignKey(StartersOrMaincourseCategory, on_delete=models.CASCADE,blank = True,null = True)
    price = models.IntegerField()
    image = models.ImageField(upload_to = "images",default = "")
    delivery_time  = models.CharField(max_length = 10,default = "10 mins")
    reviews = models.ManyToManyField(Reviews,blank = True,null = True)
    def __str__(self):
        return self.name


class CartItem(models.Model):
    individualItem = models.ForeignKey(Dish,on_delete=models.CASCADE,blank = True,null = True)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,blank = True,null = True)
    quantity = models.IntegerField(default = 0);
    subtotal = models.IntegerField(default = 0 )
class Cart(models.Model):
    # tableno = models.ForeignKey(Table,on_delete=models.CASCADE,null = True, blank = True)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,blank = True,null = True)
    name = models.CharField(max_length = 20,default = "abc")
    items = models.ManyToManyField(CartItem)
    total = models.IntegerField(default = 0)

class OrderItem(models.Model):
    orderid = models.CharField(max_length = 50,default = "123")
    individualItem = models.ForeignKey(Dish,on_delete=models.CASCADE,blank = True,null = True)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,blank = True,null = True)
    quantity = models.IntegerField(default = 0);
    subtotal = models.IntegerField(default = 0 )
    created = models.DateTimeField(auto_now_add = True,blank = True,null = True)
    delivered =  models.BooleanField(default = False)
class Order(models.Model):
    orderid = models.CharField(max_length = 50,default = "123")
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,blank = True,null = True)
    name = models.CharField(max_length = 20,default = "abc")
    items = models.ManyToManyField(OrderItem)
    total = models.IntegerField(default = 0)
    created = models.DateTimeField(auto_now_add = True,blank = True,null = True)
    delivered_time = models.DateTimeField(blank = True,null = True)
    delivered =  models.BooleanField(default = False)
    paid = models.BooleanField(default = False)
    def __str__(self):
        return self.orderid
