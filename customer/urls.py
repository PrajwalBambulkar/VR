from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import CustomPasswordChangeView 


urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    #path('',views.home,name='home'),
    path('product_detail/<int:pk>/',views.product_detail,name='product_detail'),
    path('customer_signup/',views.customer_signup,name='customer_signup'),
    path('cust_profile/',views.cust_profile,name='cust_profile'),
    # path('accounts/login/',auth_views.LoginView.as_view(template_name='back-end/login.html',authentication_form = LoginForm),name='customer_login'),
    path('accounts/login/', views.custom_login, name='customer_login'),
    path('all_users/',views.all_users,name="all_user"),



    path('logout/',auth_views.LogoutView.as_view(next_page = '/'),name='logout'),
    #path('login/', views.user_login, name='login'),
    path('cust_dash/',views.cust_dash,name='customer_signup'),
    path('save-customer/', views.save_customer, name='save_customer'),
    path('update_customer/<int:id>/', views.update_customer, name='update_customer'),



    path('add_cart/',views.add_cart,name='add_cart'),
    path('cart/',views.show_cart,name='cart'),
    path('pluscart/<int:prod_id>/',views.plus_cart),
    path('plus_cart_an/<int:prod_id>/',views.plus_cart_an),
    path('minuscart/<int:id>/',views.minus_cart),
    path('minus_cart_an/<int:id>/',views.minus_cart_an),
    path('removecart/<int:prod_id>/',views.remove_cart),
    path('remove_cart_an/<int:prod_id>/',views.remove_cart_an),
    path('custome_tshirt/',views.custome_tshirt,name='custome_tshirt'),
    path('add_wishlist/',views.add_wishlist,name='add_wishlist'),
    path('add_wish/<int:id>/',views.add_wish,name='add_wish'),
    #path('add_car/<int:id>/',views.add_car,name='add_car'),
    path('sel_size/<int:product_id>/', views.sel_size, name='sel_size'),

    path('t_shirt/',views.t_shirt,name='t_shirt'),
    path('acccesories/',views.acccesories,name='acccesories'),
    path('create_order/', views.create_order, name='create_order'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('books/',views.books,name='books'),
    path('painting/',views.painting,name='painting'),

    path('category/<slug:slug>/',views.category,name='category'),

    path('checkout/<slug:slug>/',views.checkout,name='checkout'),
    path('checkout_log/',views.checkout_log,name='checkout_log'),
    path('seller_base/',views.seller_base,name='seller_base'),
    path('show_wishlist/',views.show_wishlist,name='show_wishlist'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('about_us/',views.about_us,name='about_us'),
    # path('blog/',views.blog,name='blog'),
    # path('blog/',views.all_posts,name='blog'),
    # path('all_users/',views.all_users,name="all_user"),
    # path('blogdetails1/',views.blogdetails1,name="blogdetails1"),
    # path('blogdetails2/',views.blogdetails2,name="blogdetails2"),
    # path('blogdetails3/',views.blogdetails3,name="blogdetails3"),
    # path('blogdetails4/',views.blogdetails4,name="blogdetails4"),
    # path('blogdetails5/',views.blogdetails5,name="blogdetails5"),

    path('blog/',views.all_posts,name='blog'),
    # path('all_users/',views.all_users,name="all_user"),
    path('blogdetails1/',views.blogdetails1,name="blogdetails1"),
    path('blogdetails2/',views.blogdetails2,name="blogdetails2"),
    path('blogdetails3/',views.blogdetails3,name="blogdetails3"),
    path('blogdetails4/',views.blogdetails4,name="blogdetails4"),
    path('blogdetails5/',views.blogdetails5,name="blogdetails5"),
    path('blogdetails6/',views.blogdetails6,name="blogdetails6"),
    path('blogdetails7/',views.blogdetails7,name="blogdetails7"),
    path('blogdetails8/',views.blogdetails8,name="blogdetails8"),
    path('blogdetails9/',views.blogdetails9,name="blogdetails9"),
    path('blogdetails10/',views.blogdetails10,name="blogdetails10"),
    path('blogdetails11/', views.blogdetails11, name="blogdetails11"),
    path('blogdetails12/', views.blogdetails12, name="blogdetails12"),
    path('blogdetails13/', views.blogdetails13, name="blogdetails13"),
    path('blogdetails14/', views.blogdetails14, name="blogdetails14"),
    path('blogdetails15/', views.blogdetails15, name="blogdetails15"),
    path('blogdetails16/', views.blogdetails16, name="blogdetails16"),
    path('blogdetails17/', views.blogdetails17, name="blogdetails17"),
    path('blogdetails18/', views.blogdetails18, name="blogdetails18"),
    # path('customer_forgotpass/',views.customer_forgotpass,name="customer_forgotpass"),
    path('shop_category/', views.shop_category, name='shop_category'),
    path('Terms_Conditions/',views.Terms_Conditions,name="Terms_Conditions"),
    path('Refund_Return_Policy/',views.Refund_Return_Policy,name="Refund_Return_Policy"),
    path('Privacy_Policy/',views.Privacy_Policy,name="Privacy_Policy"),
    

    #admin
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('ad_orders/', views.ad_orders, name='ad_orders'), 
    path('order_detail/', views.order_detail, name='order_detail'),
    path('order_tracking/', views.order_tracking, name='order_tracking'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('create_vendor/', views.create_vendor, name='create_vendor'),
    path('create_coupon/', views.create_coupon, name='create_coupon'),
    
    
    #seller
    path('seller_login/', views.seller_login, name='seller_login'),
    path('seller_register/', views.seller_register, name='seller_register'),
    path('seller_forgotpass/',views.seller_forgotpass,name="seller_forgotpass"),

    # path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('reset/<str:uidb64>/token/<str:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # # path('reset_password_complet/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complet"),
    # path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('blog_details/',views.blog_details,name="blog_details"),
    path('new_order/',views.new_order,name="new_order"),
    #path('can_order/',views.can_order,name="can_order"),
    path('profile_setting/',views.profile_setting,name="profile_setting"),
    path('products/',views.products,name="products"),
    path('coupon_list/',views.coupon_list,name="coupon_list"),
    path('my_payment/',views.my_payment,name="my_payment"),
    path('payment_history/',views.payment_history,name="payment_history"),
    path('seller/login/', views.seller_login, name='seller_login'),
    path('seller_registration/', views.seller_registration, name='seller_registration'),
    path('save_customer1/', views.save_customer1, name='save_customer1'),

    path('wish_to_cart/<int:id>/', views.wish_to_cart, name='wish_to_cart'),
    path('remove_w/<int:id>/',views.remove_w,name='remove_w'),
    #seller seaction
    path('cheack_seller/<int:id>/', views.cheack_seller, name='cheack_seller'),
    path('approve-seller/<int:id>/', views.approve_seller, name='approve_seller'),
    path('delete-seller/<int:id>/', views.delete_seller, name='delete_seller'),
    path('seller_add_product/', views.seller_add_product, name='seller_add_product'),
    path('seller_view_product/', views.seller_view_product, name='seller_view_product'),
    path('admin_view_product/', views.admin_view_product, name='admin_view_product'),
    path('approve_seller_product/<int:product_id>/', views.approve_seller_product, name='approve_seller_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.view_product, name='view_product'),
    path('product/<int:product_id>/approve/', views.approve_product, name='approve_product'),
    path('seller_show_product/', views.seller_show_product, name='seller_show_product'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),
    #chnage pass
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='password_change_done'),
    path('custom-product-list/', views.custom_product_list, name='custom-product-list'),
    path('seller/profile/', views.seller_profile, name='seller_profile'),
    path('seller/profile/edit/', views.edit_seller_profile, name='edit_seller_profile'),
    path('custom-product-list/', views.custom_product_list, name='custom-product-list'),
    path('seller_self_show_product/', views.seller_self_show_product, name='seller_self_show_product'),   #seller seen their own product
    #test edit seller Product
    path('my_seller_view_product/', views.my_seller_view_product, name='my_seller_view_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'), 
    #customized T-shirts url
    path('custome_tshirts/',views.custome_tshirts,name="custome_tshirts"),
    path('del_add/<int:id>/', views.del_add, name='del_add'),

    # path('custome_mug/',views.custome_mug,name="custome_mug"),

    
    
    
    
    

    
    
    
    


    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
