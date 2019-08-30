from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from core.views import homepage,cart,add_to_cart,remove_from_cart,productpage,handlerequest,payonline,SignUp,ownerproductpage,markdelivered,paylater,minus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',auth_views.LoginView.as_view(template_name = 'login.html'),name = 'login'),
    path('logout',auth_views.LogoutView.as_view(),name = 'logout'),
    path('signup',SignUp.as_view(),name = 'signup'),
    path('', homepage, name='homepage'),
    path('cart', cart, name='cart'),
    path('<int:myid>', productpage, name='productpage'),
    path('add-to-cart/<int:myid>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:myid>', remove_from_cart, name='remove-from-cart'),
    path('minus/<int:myid>', minus, name='minus'),
    path('payonline',payonline,name = 'payonline'),
    path('paylater',paylater,name = 'paylater'),
    path('handlerequest/',handlerequest,name = 'handlerequest'),
    url(r'^ownerproductpage/(?P<myorderid>[\w]{10})/$',ownerproductpage, name='ownerproductpage'),
    url(r'^markdelivered/(?P<myorderid>[\w]{10})/$',markdelivered, name='markdelivered')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
