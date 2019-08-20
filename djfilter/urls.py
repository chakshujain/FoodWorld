from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core.views import homepage,cart,add_to_cart,remove_from_cart,productpage,handlerequest,checkout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('cart', cart, name='cart'),
    path('<int:myid>', productpage, name='productpage'),
    path('add-to-cart/<int:myid>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:myid>', remove_from_cart, name='remove-from-cart'),
    path('checkout',checkout,name = 'checkout'),
    path('handlerequest/',handlerequest,name = 'handlerequest')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
