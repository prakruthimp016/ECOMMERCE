from django.urls import path
from . import views

urlpatterns=[
    path('createuser/',views.create_user,name='register'),
    path('signin/',views.signin,name='signin'),
    path('home/',views.home,name='home'),
    path('signout',views.signout,name='signout'),
    path('updatepwd/',views.PasswordChange,name='updatepassword'),
    path('identify/',views.identifyview,name='identify'),
    path('resetpassword/<str:username>/',views.reset_password,name='resetpassword'),
    path('product/',views.product,name='product'),
    path('product_details/<slug>/',views.product_details,name='product_details'),
    # path('', views.home, name='home'),
    path('category/<slug>/', views.category_detail, name='category_detail'),
    path(' ',views.home,name='home'),
    path('addtocart/<productitemslug>/<sizeslug>/',views.add_to_cart,name='addtocart'),
    path('increment/<int:id>/',views.increment_quentity,name='increment'),
    path('decrement/<int:id>/',views.decrement_quentity,name='decrement'),
    path('removeorderitem/<int:id>/',views.remove_orderitem,name='removeorderitem'),
    path('checkout/',views.Checkout,name='checkout'),
    path('payment/',views.paymentview,name='payment'),
    path('header/',views.headerview,name='header')



    
]