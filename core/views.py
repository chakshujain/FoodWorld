from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,HttpResponseRedirect,HttpResponse
from .models import Dish,DishOriginCategory,SpicynessCategory,VegginessCategory,StartersOrMaincourseCategory,Cart,CartItem,Order,OrderItem
from django.contrib.auth import get_user_model
from .forms import UserCreateForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
import random
import string
MERCHANT_KEY = '7KHtPzzx0RzUr!9w';



class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def is_valid_queryparam(param):
    return param != '' and param is not None

def ownerproductpage(request,myorderid):
    user = get_user_model()
    if request.user.is_superuser:
        particularorder = Order.objects.get(orderid = myorderid)
        print(particularorder.name)
        context = {
        'particularorder' : particularorder
        }
        return render(request,'ownerproductpage.html',context)

def markdelivered(request,myorderid):
    user = get_user_model()
    if request.user.is_superuser:
        particularorder = Order.objects.get(orderid = myorderid)
        particularorder.delivered = True
        particularorder.paid = True
        particularorder.save()
        return HttpResponseRedirect(reverse('homepage'))
def homepage(request):
    user = get_user_model()
    if request.user.is_superuser:
        activeorder = Order.objects.filter(delivered = False)
        completedorder = Order.objects.filter(delivered = True)
        context = {
            'activeorder' : activeorder,
            'completedorder' : completedorder,
        }
        return render(request,'owner.html',context)

    else:
        qs = Dish.objects.all()
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
            'startersOrMaincourse': startersOrMaincoursemodel
        }
        return render(request, "homepage.html", context)

def productpage(request,myid):
    qs = Dish.objects.get(id = myid )
    context = {
    'queryset' : qs
    }
    return render(request,"productpage.html",context)



@login_required
def add_to_cart(request,myid):
    if request.POST:
        qty = request.POST['qty']
        user = get_user_model()
        cartitem,created= CartItem.objects.get_or_create(
        individualItem = Dish.objects.get(id = myid),user = request.user)
        cartitem.quantity = qty
        cartitem.save()
    else:
            user = get_user_model()
            cartitem,created= CartItem.objects.get_or_create(
            individualItem = Dish.objects.get(id = myid),user = request.user)
            cartitem.quantity = cartitem.quantity + 1
            cartitem.save()
    return HttpResponseRedirect(reverse("cart"))

@login_required
def remove_from_cart(request,myid):
    cartitem = CartItem.objects.get(id=myid,user = request.user)
    cartitem.delete()
    # cartitem.save()
    return HttpResponseRedirect(reverse("cart"))

def minus(request,myid):
    print("heeeeee")
    cartitem = CartItem.objects.get(id=myid,user = request.user)
    print(cartitem)
    cartitem.quantity = cartitem.quantity - 1
    cartitem.save()
    return HttpResponseRedirect(reverse("cart"))

@login_required
def cart(request):
    user = get_user_model()
    cart,created = Cart.objects.get_or_create(user = request.user,name = "abc")
    cart.save()
    total = 0
    cartitem = CartItem.objects.filter(user = request.user)
    context = {
    'cartitems' : cartitem
    }
    for item in CartItem.objects.filter(user = request.user):
        subtotal = item.individualItem.price * item.quantity
        total = total + subtotal
        item.subtotal = subtotal
        item.save()
    cart.total = total
    cart.save()
    cartitemlist = list(cartitem)
    cart.items.add(*cartitemlist)
    context['cart'] = cart
    return render(request,"cart_page.html",context)

def paylater(request):
    user = get_user_model()
    cart,created = Cart.objects.get_or_create(name = "abc",user = request.user)
    orderid =  random_string_generator()
    cartitem = CartItem.objects.filter(user = request.user)
    for item in CartItem.objects.filter(user = request.user):
        orderitem = OrderItem()
        orderitem.orderid = orderid
        orderitem.individualItem = item.individualItem
        orderitem.user = request.user
        orderitem.quantity = item.quantity
        orderitem.subtotal = item.subtotal
        orderitem.save()
    orderitemlist = OrderItem.objects.filter(user = request.user,orderid = orderid)
    try:
        # if any previous order or not
        previousorder = Order.objects.get(user = request.user,delivered = False)
        previousid = previousorder.orderid
        order,created = Order.objects.get_or_create(orderid = previousid,user = request.user,delivered = False)
        for item in Cart.objects.filter(user = request.user):
            order.user = request.user
            order.name = item.name
            order.total = order.total +  item.total
        orderitemlist = list(orderitemlist)
        order.items.add(*orderitemlist)
        order.save()
        cart.delete()
        cartitem.delete()
        context = {}
        return render(request,"cashmodestatus.html",context)
    except:
        order,created = Order.objects.get_or_create(orderid = orderid,user = request.user,delivered = False)
        for item in Cart.objects.filter(user = request.user):
            order.user = request.user
            order.name = item.name
            order.total = item.total
        orderitemlist = list(orderitemlist)
        order.items.add(*orderitemlist)
        order.save()
        cart.delete()
        cartitem.delete()
        context = {}
        return render(request,"cashmodestatus.html",context)

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required
def payonline(request):
    user = get_user_model()
    cart,created = Cart.objects.get_or_create(name = "abc",user = request.user)
    orderid =  random_string_generator()
    if request.method == "POST":
        print("11122222222222222211111111111111111111111")
        param_dict = {
                'MID':'MJjWrZ23383299577319',
                'ORDER_ID':orderid,
                'TXN_AMOUNT':str(cart.total),
                'CUST_ID':str(request.user),
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
            print(response_dict)
            cartitem = CartItem.objects.filter(user = response_dict['CUST_ID'])
            for item in CartItem.objects.filter(user = response_dict['CUST_ID']):
                orderitem = OrderItem()
                orderitem.orderid = orderid
                orderitem.individualItem = item.individualItem
                orderitem.user = item.user
                orderitem.quantity = item.quantity
                orderitem.subtotal = item.subtotal
                orderitem.save()
            orderitemlist = OrderItem.objects.filter(user = response_dict['CUST_ID'],orderid = orderid)
            try:
                # if any previous order or not
                previousorder = Order.objects.get(user = response_dict['CUST_ID'],delivered = False)
                previousid = previousorder.orderid
                order,created = Order.objects.get_or_create(orderid = previousid,user = response_dict['CUST_ID'],delivered = False)
                for item in Cart.objects.filter(user = response_dict['CUST_ID']):
                    order.user = response_dict['CUST_ID']
                    order.name = item.name
                    order.total = order.total +  item.total
                orderitemlist = list(orderitemlist)
                order.items.add(*orderitemlist)
                order.save()
                cart.delete()
                cartitem.delete()
                context = {}
                return render(request,"cashmodestatus.html",context)
            except:
                order,created = Order.objects.get_or_create(orderid = orderid,user = response_dict['CUST_ID'],delivered = False)
                for item in Cart.objects.filter(user = response_dict['CUST_ID']):
                    order.user = response_dict['CUST_ID']
                    order.name = item.name
                    order.total = item.total
                orderitemlist = list(orderitemlist)
                order.items.add(*orderitemlist)
                order.save()
                cart.delete()
                cartitem.delete()
                context = {}
                return render(request,"cashmodestatus.html",context)

        else:
            print("order was not successful" + response_dict['RESPMSG'])

    return render(request,'paymentstatus.html',{'response':response_dict})
