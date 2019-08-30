from .models import CartItem,Order
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# @login_required
def default(request):
    dict = {}
    user = get_user_model()
    if(request.user.is_authenticated):
        username = request.user.username
        cartcount = CartItem.objects.filter(user = request.user).count()
        order = Order.objects.filter(user = request.user,delivered = False)
        dict['username'] = username
        dict['cartcount'] = cartcount
        dict['order'] = order

    else:
        username = "Nobody"
        cartcount = 0
        dict['username'] = username
        dict['cartcount'] = cartcount
    return dict
