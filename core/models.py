from django.db import models
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
    reviews = models.ManyToManyField(Reviews)
    def __str__(self):
        return self.name
#
# class Table(models.Model):
#     number = models.IntegerField(default = 1)
#     ads = models.CharField(max_length = 30)

class CartItem(models.Model):
    individualItem = models.ForeignKey(Dish,on_delete=models.CASCADE,blank = True,null = True)
    quantity = models.IntegerField(default = 0);
    subtotal = models.IntegerField(default = 0 )
class Cart(models.Model):
    # tableno = models.ForeignKey(Table,on_delete=models.CASCADE)
    name = models.CharField(max_length = 20,default = "abc")
    items = models.ManyToManyField(CartItem)
    total = models.IntegerField(default = 0)
