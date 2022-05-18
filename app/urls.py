from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import  static
from django.contrib.auth import  views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, \
    MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    #path('', views.home),
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path("add-to-cart/", views.add_to_cart, name='add-to-cart'),
    #path("add-to-cartwu/", views.add_to_cartwu, name='add-to-cartwu'),
    path("cart/", views.show_cart, name='showcart'),
    path("pluscart", views.plus_cart, name='pluscart'),
    path("minuscart", views.minus_cart, name='minuscart'),
    path("removecart", views.remove_cart, name='removecart'),
    path('buy/', views.buy_now, name='buy_now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('orders1/', views.OrderView.as_view(), name='orders1'),
    #path('orders1/', views.orders1, name='orders1'),
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.
         as_view(template_name='app/passwordchangedone.html'),
         name='passwordchangedone'),
    path("password-reset/",auth_views.PasswordResetView.as_view(template_name
            ='app/password_reset.html',form_class=MyPasswordResetForm),
               name='password_reset'),
    path("password-reset/done/",auth_views.PasswordResetDoneView.
         as_view(template_name='app/password_reset_done.html'),
               name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.
         as_view(template_name='app/password_reset_confirm.html',form_class=
                 MySetPasswordForm),
               name='password_reset_confirm'),
    path("password-reset-complete/",auth_views.PasswordResetCompleteView.as_view(template_name
            ='app/password_reset_complete.html'),
               name='password_reset_complete'),
    #path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwear/',views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/',views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('electronics/', views.electronics, name='electronics'),
    path('laptop/', views.laptop, name='laptop'),
    path('accounts/login/' , auth_views.LoginView.as_view
    (template_name='app/login.html',authentication_form=LoginForm), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view
    (template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,
     success_url='/passwordchangedone/'),
         name='passworchange'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    #path('checkout1/', views.checkout1, name='checkout1'),
    path('checkout1/', views.CheckoutView.as_view(), name='checkout1'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_done1/', views.payment_done1, name='payment_done1'),
    path('search/', views.search, name = 'search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
