from .models import CartItem
from django.conf import settings

def default(request):
    cartcount = CartItem.objects.all().count()

    return {
            'cartcount' : cartcount
    }
