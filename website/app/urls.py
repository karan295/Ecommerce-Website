from django.urls import path
from app import views
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

#from django.contrib.auth.views import password_reset

from .forms import *


urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),

    
    path('store/', views.store, name="store"),



    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/',views.show_cart,name='showcart'),

    path('pluscart/',views.plus_cart),

    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),


    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    #path('changepassword/', views.change_password, name='changepassword'),

    path('mobile/',views.mobile,name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('laptop/',views.laptop,name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),

    path('top_wear/',views.top_wear,name='top_wear'),
    path('top_wear/<slug:data>', views.top_wear, name='top_weardata'),

    path('bottom_wear/',views.bottom_wear,name='bottom_wear'),
    path('bottom_wear/<slug:data>',views.bottom_wear,name='bottom_weardata'),

    path('accounts/login/',auth_views.LoginView.as_view
    (template_name='app/login.html',
    authentication_form=LoginForm), name='login'),

    #path('accounts/login/',views.password_reset,name='password_reset'),
    
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),

    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
    form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),
    name='passwordchangedone'),



    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
   
   
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
   # path('accounts/login/',auth_views.LoginView.as_view(),{'template_name':'app/login.html'},name='login'),
    
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    
    path('search/',views.search,name='search'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)