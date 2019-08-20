from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404,HttpResponseRedirect,HttpResponse
from .models import Dish,DishOriginCategory,SpicynessCategory,VegginessCategory,StartersOrMaincourseCategory,Cart,CartItem
from django.urls import reverse
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
import random
import string
MERCHANT_KEY = '7KHtPzzx0RzUr!9w';

def is_valid_queryparam(param):
    return param != '' and param is not None


def homepage(request):
    qs = Dish.objects.all()
    cartcount = CartItem.objects.all().count()
    dishOriginmodel = DishOriginCategory.objects.all()
    spicynessmodel = SpicynessCategory.objects.all()
    vegginessmodel = VegginessCategory.objects.all()
    startersOrMaincoursemodel = StartersOrMaincourseCategory.objects.all()
    vegginess = request.GET.get('vegginess')
    budget = request.GET.get('budget')
    dishOrigin = request.GET.get('dishOrigin')
    startersOrMaincourse = request.GET.get('startersOrMaincourse')
    spicyness = request.GET.get('spicyness')
    particular_thing  = request.GET.get('particular_thing')



    if is_valid_queryparam(vegginess) and vegginess != 'Choose...':
        qs = qs.filter(vegginess__name=vegginess)

    if is_valid_queryparam(spicyness) and spicyness != 'Choose...':
        qs = qs.filter(spicyness__name=spicyness)

    if is_valid_queryparam(startersOrMaincourse) and startersOrMaincourse != 'Choose...':
        qs = qs.filter(startersOrMaincourse__name=startersOrMaincourse)

    if is_valid_queryparam(dishOrigin) and dishOrigin != 'Choose...':
        qs = qs.filter(dishOrigin__name=dishOrigin)

    if is_valid_queryparam(budget):
        qs = qs.filter(price__lt=budget)

    if is_valid_queryparam(particular_thing):
        qs = qs.filter(name__icontains = particular_thing)

    context = {
        'queryset': qs,
        'dishOrigin': dishOriginmodel,
        'spicyness': spicynessmodel,
        'vegginess': vegginessmodel,
        'startersOrMaincourse': startersOrMaincoursemodel,
        'cartcount' : cartcount

    }
    return render(request, "homepage.html", context)

def productpage(request,myid):
    qs = Dish.objects.get(id = myid )
    context = {
    'queryset' : qs
    }
    return render(request,"productpage.html",context)




def add_to_cart(request,myid):
    if request.POST:
        qty = request.POST['qty']
        cartitem,created= CartItem.objects.get_or_create(
        individualItem = Dish.objects.get(id = myid))
        print(created)
        cartitem.quantity = qty
        cartitem.save()
    return HttpResponseRedirect(reverse("homepage"))

def remove_from_cart(request,myid):
    # cartitem = CartItem(
    # individualItem = Dish.objects.get(id = myid))
    cartitem = CartItem.objects.get(id=myid)
    print(cartitem)
    cartitem.delete()
    # cartitem.save()
    return HttpResponseRedirect(reverse("cart"))

def cart(request):

    total = 0
    cartitem = CartItem.objects.all()

    context = {
    'cartitems' : cartitem
    }
    for item in CartItem.objects.all():
        subtotal = item.individualItem.price * item.quantity
        total = total + subtotal
        item.subtotal = subtotal
        item.save()
    cartitemlist = list(cartitem)
    cart,created = Cart.objects.get_or_create(name = "abc")
    cart.total = total
    print(created)
    cart.save()
    cart.items.add(*cartitemlist)
    context['cart'] = cart
    return render(request,"cart_page.html",context)

def checkout(request):
    def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    cart,created = Cart.objects.get_or_create(name = "abc")
    orderid =  random_string_generator()
    print(orderid)
    if request.method == "POST":
        param_dict = {
                'MID':'MJjWrZ23383299577319',
                'ORDER_ID':orderid,
                'TXN_AMOUNT':str(cart.total),
                'CUST_ID':'abc@gmail.com',
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE':'WEBSTAGING',
                'CHANNEL_ID':'WEB',
    	        'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
            }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict': param_dict})



@csrf_exempt
def handlerequest(request):
    # paytm will send post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i=='CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print("order was not successful" + response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response':response_dict})
