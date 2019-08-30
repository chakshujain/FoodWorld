from django.contrib import admin

from .models import Dish,DishOriginCategory,VegginessCategory,SpicynessCategory,StartersOrMaincourseCategory,Cart,CartItem,Order,OrderItem

admin.site.register(Dish)
admin.site.register(DishOriginCategory)
admin.site.register(VegginessCategory)
admin.site.register(SpicynessCategory)
admin.site.register(StartersOrMaincourseCategory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
