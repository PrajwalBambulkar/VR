from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import random
import string
from django.contrib.auth.decorators import login_required
# Create your views here.

# def home(request):
#     return render(request,'front-end/flower-demo.html')


from .models import OrderPlaced
def ad_orders(request):
    # Retrieve all OrderPlaced objects from the database
    orders = OrderPlaced.objects.all().order_by('-Order_date')

    # Pass the orders to the template as a context variable
    context = {'orders': orders}
    return render(request, 'back-end/order-list.html', context)

class ProductView(View):
    def get(self,request):
        
        data = Product.objects.all().order_by('-prod_date')
        tshirt = Product.objects.filter(category = 'TS').order_by('-prod_date')
        acc = Product.objects.filter(category = 'AC').order_by('-prod_date')
        book = Product.objects.filter(category = 'BK').order_by('-prod_date')
        paint = Product.objects.filter(category = 'PT').order_by('-prod_date')
        posts = Post.objects.filter(status=1)
        poster=Poster.objects.all()
        banner = Banner.objects.all()
        cat = Category.objects.all()
        print('posts',posts)
        print('ttttttttttttt',request.user)
        context= {
            'data':data,
            'tshirt':tshirt,
            'acc':acc,
            'book':book,
            'paint':paint,
            'posts':posts,
            'banner':banner,
            'poster':poster,
            'cat':cat,
        }
        return render(request,'front-end/flower-demo.html',context)


#new product Details

def product_detail(request,pk):
    print()
    print(f'product details request.user---------{request.user}')

    product = Product.objects.get(pk = pk)

    data = Product.objects.all().order_by('?')
    
    #item_already_in_cart=False
    item_already_in_cart_an=False
    item_already_in_wish =False

    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        #item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        item_already_in_wish = Whishlist.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()    
    else: 
        item_already_in_cart_an = Cart.objects.filter(Q(product = product.id) & Q(anonymous_user_id = request.session.session_key))
    context= {
        'product':product,
        'totalitem':totalitem,
        'data':data,
        #'item_already_in_cart':item_already_in_cart,
        'item_already_in_wish':item_already_in_wish,
        'item_already_in_cart_an':item_already_in_cart_an,
    }
    return render(request,'front-end/product-left-sidebar.html',context)








#show all user

def all_users(request):
    users = User.objects.filter(is_superuser=False)  # Exclude superusers
    print('rammmmmmmmmmmm', users) 
    return render(request, 'back-end/all-users.html', {'users': users})   



# new login

# def customer_signup(request):
#     if request.method == 'POST':
#         form = CustomerRegistration(request.POST)
#         if form.is_valid():
#             print('Formmmmm',form.cleaned_data)
#             form.save()
#             return HttpResponseRedirect('/accounts/login/')
#     else:
#         form = CustomerRegistration()        
    
#     return render(request,'back-end/sign-up.html',{'form':form})
# orignal code **************************************************************************************************************
# def customer_signup(request):
#     if request.method == 'POST':
#         form = CustomerRegistration(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the user object
#             # Send registration confirmation email
#             subject = "Registration Confirmation"
#             message = f"Hello {user.username},\n\nThank you for registering on our website.\n\nBest regards,\nMahesh Talmale"
#             from_email = "zappkodesolutions@gmail.com"  # Replace this with your desired 'from' email address
#             recipient_list = [user.email]
#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#             return HttpResponseRedirect('/accounts/login/')
#     else:
#         form = CustomerRegistration()
    
#     return render(request, 'back-end/sign-up.html', {'form': form})


from django.contrib import messages

# def customer_signup(request):
#     if request.method == 'POST':
#         form = CustomerRegistration(request.POST)
#         if form.is_valid():
#             password1 = form.cleaned_data['password1']
#             password2 = form.cleaned_data['password2']
            
#             if password1 == password2:
#                 user = form.save()  # Save the user object
#                 # Send registration confirmation email
#                 subject = "Registration Confirmation"
#                 message = f"Hello {user.username},\n\nThank you for registering on our website.\n\nBest regards,\nMahesh Talmale"
#                 from_email = "zappkodesolutions@gmail.com"  # Replace this with your desired 'from' email address
#                 recipient_list = [user.email]
#                 send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
#                 # Add a success message for the user
#                 messages.success(request, 'Registration successful! Please login.')

#                 return HttpResponseRedirect('/accounts/login/')
            
#         else:
#             # Form is not valid, handle as needed
#             pass
#     else:
#         form = CustomerRegistration()
    
#     return render(request, 'back-end/sign-up.html', {'form': form})




from django.contrib import messages

def customer_signup(request):

	cart_items_transferred = False

	if request.method == 'POST':

		form = CustomerRegistration(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save() 
			print('Formmmmm',form.cleaned_data)
			CustProfile.objects.create(
				user=user,
				name=request.POST['username'],  # You can change this based on how you want to capture the name
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				# password = make_password(request.POST['password']),
				# conform_password = make_password(request.POST['confirm_password'])
				# Add more fields as needed, e.g., date_of_birth=request.POST['date_of_birth']
			)
			# Send registration confirmation email
			subject = "Registration Confirmation"
			message = f"Hello {user.username},\n\nThank you for registering on our website.\n\nBest regards,\nMahesh Talmale"
			from_email = "zappkodesolutions@gmail.com"  # Replace this with your desired 'from' email address
			recipient_list = [user.email]
			send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
			    # Add a success message for the user
			messages.success(request, 'Registration successful! Please login.')

			anonymous_user_id = request.session.get('anonymous_user_id')
			if anonymous_user_id:
				cart_items = Cart.objects.filter(anonymous_user_id=anonymous_user_id)

				for cart_item in cart_items:
                    
					cart_item.user = user
					cart_item.anonymous_user_id = None  
					cart_item.save()
				cart_items_transferred = True
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)
			if cart_items_transferred:
				return HttpResponseRedirect('/cart/')
			else:
				return HttpResponseRedirect('/')
			#return HttpResponseRedirect('/accounts/login/')

		else:
			messages.error(request, "Passwords do not match. Please enter matching passwords.")
			return render(request, 'back-end/sign-up.html', {'form': form} )
	else:
		form = CustomerRegistration()        
	return render(request,'back-end/sign-up.html',{'form':form})





# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         print('popopopop',username,password,user)
#         if user is not None:
#             login(request, user)
#             # Redirect to a success page or the desired URL
#             return redirect('')
#         else:
#             # Handle invalid login credentials here
#             pass


#     return render(request, 'back-end/login.html')


# def custom_login(request):
#     id = request.session.get('item_id')
#     cart_id = request.session.get('cart_id')
#     if id :
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             print('userrrrr',username,password)
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 product = get_object_or_404(Product, id=id)
#                 item_already_in_wish = Whishlist.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
#                 if item_already_in_wish:
#                     pass
#                 else:
#                     product = get_object_or_404(Product, id=id)
#                     wish = Whishlist(user = request.user,product=product)
#                     wish.save()
#                 # Redirect to a success page or the desired URL
#                 return redirect(f'/product_detail/{id}/')
            
#     elif cart_id : 
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 product = get_object_or_404(Product, id = cart_id)
#                 item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
#                 print(f'hai-{item_already_in_cart}')
#                 if item_already_in_cart:
#                     pass
#                 else:
#                     cart = Cart(user=request.user,product=product)
#                     cart.save()
#                 # Redirect to a success page or the desired URL
#                 return redirect(f'/product_detail/{cart_id}/')           
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             print('userrrrr',username,password)
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to a success page or the desired URL
#                 return redirect('/')  # Change the URL as needed
#             else:
#                 # Handle invalid login credentials here
#                 return render(request, 'back-end/login.html', {'error_message': 'Invalid credentials'})
#         return render(request, 'back-end/login.html')
#     return render(request, 'back-end/login.html')


def custom_login(request):
    id = request.session.get('item_id')
    slug = request.session.get('anonymous_user_id')     
    if id :
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print('userrrrr',username,password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                product = get_object_or_404(Product, id=id)
                item_already_in_wish = Whishlist.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
                if item_already_in_wish:
                    pass
                else:
                    product = get_object_or_404(Product, id=id)
                    wish = Whishlist(user = request.user,product=product)
                    wish.save()
                # Redirect to a success page or the desired URL
                return redirect(f'/product_detail/{id}/')
    elif slug:
        data = Cart.objects.filter(anonymous_user_id = slug)
        print(f'data--------{data}')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                data = Cart.objects.filter(anonymous_user_id = slug)

                print(f'loginnn ke time pe-{data}')

                for i in data:
                    product = get_object_or_404(Product, id=i.product.id)
                    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
                    if item_already_in_cart:
                        i.delete()
                        pass
                    else:
                        cart = Cart(user=request.user, product=i.product, quantity=i.quantity, size=i.size)
                        cart.save()
                        i.delete()
                return redirect('/cart/')  
                   
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print('userrrrr',username,password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or the desired URL
                return redirect('/')  # Change the URL as needed
            else:
                # Handle invalid login credentials here
                return render(request, 'back-end/login.html', {'error_message': 'Invalid credentials'})
        return render(request, 'back-end/login.html')
    return render(request, 'back-end/login.html')


def add_wish(request,id):
    request.session['item_id'] = id
    return redirect("/accounts/login/")

# def add_car(request,id):
#     request.session['cart_id'] = id
#     return redirect("/accounts/login/")

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         print()
#         print('ommmmm',user)
#         print()
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'back-end/login.html', {'error': 'Invalid login credentials'})
#     return render(request, 'back-end/login.html')


def cust_profile(request):
    if request.method == 'POST':
        user = request.user
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        data = Customer(user=user,name=fname,mobile=mobile,pincode=pincode,email=email,locality=locality,city=city,state=state)
        data.save()

    # add = Customer.objects.filter(user = request.user)
    # for i in add:
    #     print('oooooooooooo',i.name)
    # context={'add':add}
    return render(request,'back-end/profile-setting.html',)

# def cust_dash(request):
#     if request.method == 'POST':
#         user = request.user
#         fname = request.POST.get('fname')
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')
#         locality = request.POST.get('locality')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         pincode = request.POST.get('pincode')
#         data = Customer(user=user,name=fname,mobile=mobile,pincode=pincode,email=email,locality=locality,city=city,state=state)
#         data.save()
#     add = Customer.objects.filter(user = request.user)
#     context = {'add':add}
#     return render(request,'front-end/user-dashboard.html',context)

# def add_cart(request):
#     user = request.user
#     prod_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=prod_id)
#     #quantity = request.GET.get('quantity')
#     size = request.GET.get('size')
#     Cart(user=user,product=product,size=size).save()
    
#     print()
#     print('userrrrrrrrrrrrrrr',user,prod_id,size)
#     print(product)
#     return redirect('/product_detail/{}/'.format(prod_id))

def add_cart(request):
    user = request.user
    print()
    print(f'add cart request.user--------{user}')
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)
    quantity = request.GET.get('quantity')
    size = request.GET.get('size')

    # Check if the user is logged in or not
    if user.is_authenticated:
        Cart(user=user, product=product, quantity=quantity, size=size).save()
    else:
        # Generate a unique identifier for the anonymous user (e.g., session ID)
        anonymous_user_id = request.session.session_key
        print()
        print(f'anonymous_userrrrrrrr---------{anonymous_user_id}')
        if not anonymous_user_id:
            request.session.save()
            anonymous_user_id = request.session.session_key

        # Save the cart item associated with the anonymous user
        Cart(anonymous_user_id=anonymous_user_id, product=product, quantity=quantity, size=size).save()
    return redirect(f'/product_detail/{prod_id}/')



def show_cart(request):
    user = request.user
    anonymous_user_id = request.session.session_key
    # Check if the user is authenticated
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user)
    else:
        # Retrieve the anonymous user ID from the session
        anonymous_user_id = request.session.session_key

        data = Cart.objects.filter(anonymous_user_id = anonymous_user_id)
        for i in data: 
            print()
            print('data',i.id)
            print()
        
        # If there is no anonymous user ID, create one
        if not anonymous_user_id:
            request.session.save()
            anonymous_user_id = request.session.session_key
            
        # Retrieve cart items associated with the anonymous user

        print(f'userrrrrr-{anonymous_user_id}')

        cart = Cart.objects.filter(anonymous_user_id=anonymous_user_id)
    
    amount = 0.0
    delivery_chrg = 0.0
    cart_product = list(cart)  # Convert queryset to a list

    if cart_product:
        for c in cart_product:
            fare_amt = (c.quantity * c.product.discount_price)
            amount += fare_amt
            total_amt = amount + delivery_chrg
        context = {
            'cart': cart, 'total_amt': total_amt, 'amount': amount, 'fare_amt': fare_amt,'anonymous_user_id':anonymous_user_id,
        }
        return render(request, 'front-end/cart.html', context)
    else:
        return render(request, 'front-end/cart.html')



def sel_size(request,product_id):
    if request.method == 'POST':
        print(request.POST)
        new_size = request.POST.get('new_size')
        cart_item = Cart.objects.get(id=product_id)
        print()
        print(f'my size {new_size} cart id {cart_item}')
        print()
        cart_item.size = new_size
        cart_item.save()
        return redirect('cart')


def plus_cart(request,prod_id):
    print(f'pluse cart---------{request.session.session_key}')
    if request.method=='GET':
        # prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(id = prod_id) & Q(user = request.user)) 
        print()
        print('ccccccccccc',c)
        print()
        c.quantity+=1
        c.save()
        amount = 0.0
        delivery_chrg= 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            fare_amt = (p.quantity * p.product.discount_price)
            amount += fare_amt
            total_amt = amount + delivery_chrg
        data = {
                    'quantity':c.quantity, 'total_amt':total_amt, 'amount':amount, 
                }
        return redirect('/cart/')
    else:
        return HttpResponse("")


def plus_cart_an(request,prod_id):
    print(f'pluse cart---------{request.session.session_key}')
    if request.method=='GET':
        # prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(id = prod_id) & Q(anonymous_user_id = request.session.session_key))
        print()
        print('ccccccccccc',c)
        print()
        c.quantity+=1
        c.save()
        amount = 0.0
        delivery_chrg= 0.0
        cart_product = [p for p in Cart.objects.all() if p.anonymous_user_id == request.session.session_key]
        for p in cart_product:
            fare_amt = (p.quantity * p.product.discount_price)
            amount += fare_amt
            total_amt = amount + delivery_chrg
        data = {
                    'quantity':c.quantity, 'total_amt':total_amt, 'amount':amount, 
                }
        return redirect('/cart/')
    else:
        return HttpResponse("")




def minus_cart(request,id):
    print('iddiiiiidiidiidid',id)
    if request.method == 'GET':
		# prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(id=id) & Q(user=request.user)) 
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount= 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            if p.product.discount_price:
                tempamount = (p.quantity * p.product.discount_price)
            else:
                tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount 	
        data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
        return redirect('/cart/')
    else:
    	return HttpResponse("")


def minus_cart_an(request,id):
    print('iddiiiiidiidiidid',id)
    if request.method == 'GET':
		# prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(id = id) & Q(anonymous_user_id = request.session.session_key))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount= 0.0
        cart_product = [p for p in Cart.objects.all() if p.anonymous_user_id == request.session.session_key]
        for p in cart_product:
            if p.product.discount_price:
                tempamount = (p.quantity * p.product.discount_price)
            else:
                tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount 	
        data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
        return redirect('/cart/')
    else:
    	return HttpResponse("")

    	

from django.http import HttpResponse
def remove_cart(request, prod_id):
    if request.method == "GET":
        try:
            c = Cart.objects.get(Q(id=prod_id) & Q(user=request.user))
            c.delete()
            amount = 0.0
            shipping_amount = 50.0
            cart_products = Cart.objects.filter(user=request.user)
            
            for p in cart_products:
                if p.product.discount_price:
                    tempamount = (p.quantity * p.product.discount_price)
                else:
                    tempamount = (p.quantity * p.product.selling_price)
                
                amount += tempamount
            
            data = {
                'amount': amount,
                'totalamount': amount + shipping_amount,
            }
            
            return redirect('/cart/')
        except Cart.DoesNotExist:
            return HttpResponse("Product not found in the cart.")
    else:
        return HttpResponse("Invalid request method.")

def remove_cart_an(request, prod_id):
    if request.method == "GET":
        try:
            c = Cart.objects.get(Q(id = prod_id) & Q(anonymous_user_id = request.session.session_key))
            c.delete()
            amount = 0.0
            shipping_amount = 50.0
            cart_products = Cart.objects.filter(anonymous_user_id = request.session.session_key)
            
            for p in cart_products:
                if p.product.discount_price:
                    tempamount = (p.quantity * p.product.discount_price)
                else:
                    tempamount = (p.quantity * p.product.selling_price)
                
                amount += tempamount
            
            data = {
                'amount': amount,
                'totalamount': amount + shipping_amount,
            }
            
            return redirect('/cart/')
        except Cart.DoesNotExist:
            return HttpResponse("Product not found in the cart.")
    else:
        return HttpResponse("Invalid request method.")



@login_required
def checkout_log(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user = request.user) 
    amount = 0.0
    shipping_amount = 0.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            totalamount = amount+shipping_amount

    # cust = Customer.objects.get(id = address) 

    # if pay == 'cod':
    #     order = OrderPlaced(user = request.user,product=p.product.id)  
    #     order.save()  

    
    return render(request, 'front-end/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})


def checkout(request,slug):
    request.session['anonymous_user_id'] = slug
    print()
    print(f'vishwasssssssss---{slug}')
    print()
    return redirect("/accounts/login/")

#*****************************************************************************************************************************
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.shortcuts import render, redirect
# from .models import Customer, Cart, OrderPlaced

# def checkout(request):
#     user = request.user
#     add = Customer.objects.filter(user=user)
#     cart_items = Cart.objects.filter(user=request.user)
#     amount = 0.0
#     shipping_amount = 0.0
#     totalamount = 0.0
#     cart_product = [p for p in Cart.objects.all() if p.user == request.user]

#     if cart_product:
#         for p in cart_product:
#             tempamount = (p.quantity * p.product.discount_price)
#             amount += tempamount
#             totalamount = amount + shipping_amount

#     # Assuming you have code to place the order here
#     # Example:
#     # order = OrderPlaced(user=request.user, product=p.product.id)
#     # order.save()

#     # Send an email to the user
#     subject = 'Your Order Has Been Placed Successfully'
#     message = 'Thank you for your order. Your order has been placed successfully.'
#     from_email = 'zappkodesolutions@gmail.com'  # Replace with your email
#     recipient_list = [user.email]

#     # You can also create an HTML template for the email
#     # and render it using render_to_string
#     # email_html_message = render_to_string('email_template.html', {'user': user, 'order': order})

#     send_mail(subject, message, from_email, recipient_list)

#     # Redirect to a success page or display a success message
#     return render(request, 'front-end/checkout.html', {'add': add, 'cart_items': cart_items, 'totalcost': totalamount})


def custome_tshirt(request):
    return render(request,'front-end/customize-tshirt.html')

def custome_mug(request):
    return render(request,'front-end/customize-mug.html')

#mahesh
from django.contrib.auth.decorators import user_passes_test
    
@user_passes_test(lambda user: user.is_superuser)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/admin_dashboard/')
            # return render(request, 'back-end/admin-index.html')
        else:
            return render(request, 'back-end/admin_login.html', {'error': 'Invalid login credentials'})
    return render(request, 'back-end/admin_login.html')

def admin_dashboard(request):
    return render(request,'back-end/admin-index.html')

def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        selling_price = request.POST.get('selling_price')
        discount_price = request.POST.get('discount_price')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        product_image = request.FILES.get('myFile')  # Handle uploaded image file
        back_image = request.FILES.get('back_image')
        left_image = request.FILES.get('left_image')
        right_image = request.FILES.get('right_image')
        product_video = request.FILES.get('product_video')

        print('ppppp',title,selling_price,discount_price,description,brand,category)
        
        # Create a new Product instance and save it to the database
        product = Product(
            title=title,
            selling_price=selling_price,
            discount_price=discount_price,
            description=description,
            brand=brand,
            category=category,
            product_image=product_image,
            back_image=back_image,
            left_image=left_image,
            right_image=right_image,
            product_video=product_video,)
        
        product.save()
        print('mmmmmmmmmmmmm',product)
        
        # return redirect('success_page')  # Redirect to a success page
        
    return render(request, 'back-end/seller-add-products.html')

def t_shirt(request):
    data = Product.objects.filter(category = 'TS')
    context={'data':data}
    return render(request,'front-end/shop-top-filter.html',context)


def acccesories(request):
    data1 = Product.objects.filter(category = 'AC')
    context = {'data1':data1}
    return render(request,'front-end/shop-top-filter.html',context)

def books(request):
    data2 = Product.objects.filter(category = 'BK')
    context = {'data2':data2}
    return render(request,'front-end/shop-top-filter.html',context)

def painting(request):
    data3 = Product.objects.filter(category = 'PT')
    context = {'data3':data3}
    return render(request,'front-end/shop-top-filter.html',context)



def category(request,slug):
    if slug == 'FASHION':
        return redirect('/t_shirt/')
    elif slug == 'ACCESORIES':
         return redirect('/acccesories/')
    elif slug == 'BOOKS':
         return redirect('/books/')
    elif slug == 'PAINTINGS':
         return redirect('/painting/')
    else:
        return render(request,'front-end/404.html')



def admin_user(request):
    users = User.objects.filter(is_superuser=False)  
    print('rammmmmmmmmmmm', users) 
    return render(request, 'back-end/all-users.html', {'users': users})
	#return render(request,'back-end/all-users.html')

# def ad_orders(request):
# 	return render(request,'back-end/order-list.html')

def order_detail(request):
	return render(request,'back-end/order-detail.html')

def order_tracking(request):
	return render(request,'back-end/order-tracking.html')

def vendor_list(request):
    sellers = Seller.objects.filter(seller=True)  # Retrieve all Seller objects from the database
    for i in sellers:
        print(i.user)
    print('eeeeeeeeeeeeeeee',sellers)
    context = {
        'sellers': sellers,  # Pass the sellers queryset as context
    }
    return render(request, 'back-end/vendor-list.html', context)

def create_vendor(request):
	return render(request,'back-end/create-vendor.html')

def seller_base(request):
	return render(request,'back-end/seller-base.html')

def seller_dashboard(request):
    return render(request,'back-end/seller_dashboard.html')

# def seller_login(request):
# 	return render(request,'back-end/seller-login.html')

def seller_register(request):
	return render(request,'back-end/seller-register.html')

def seller_forgotpass(request):
	return render(request,'back-end/seller_forgotpass.html')

def contact_us(request):
	if request.method == "POST":
		f_name = request.POST.get('f_name')
		l_name = request.POST.get('l_name')
		email = request.POST.get('email')
		comment = request.POST.get('comment')
		ContactUs(f_name=f_name, l_name=l_name, email=email, comment=comment).save()
	return render(request, 'front-end/contact-us.html')

         	    

def about_us(request):
	return render(request,'front-end/about-us.html')

def our_product(request):
	item = Product.objects.all()
	return render(request,"front-end/flower-demo.html")

# def blog(request):
# 	return render(request,'front-end/blog-infinite-scroll.html')

# def blogdetails1(request):
#     posts = Post.objects.filter(status=1)
#     return render(request, 'front-end/blog-details1.html', {'posts': posts})
	

# def blogdetails2(request):
# 	return render(request,'front-end/blog-details2.html')

# def blogdetails3(request):
# 	return render(request,'front-end/blog-details3.html')

# def blogdetails4(request):
# 	return render(request,'front-end/blog-details4.html')

# def blogdetails5(request):
# 	return render(request,'front-end/blog-details5.htmll')

def blog(request):
	return render(request,'front-end/blog-infinite-scroll.html')

def blogdetails1(request):
    #posts = Post.objects.filter(status=1)
    return render(request, 'front-end/blog-details1.html',)
	

def blogdetails2(request):
	return render(request,'front-end/blog-details2.html')

def blogdetails3(request):
	return render(request,'front-end/blog-details3.html')

def blogdetails4(request):
	return render(request,'front-end/blog-details4.html')

def blogdetails5(request):
	return render(request,'front-end/blog-details5.html')

def blogdetails6(request):
	return render(request,'front-end/blog-details6.html')

def blogdetails7(request):
	return render(request,'front-end/blog-details7.html')

def blogdetails8(request):
	return render(request,'front-end/blog-details8.html')

def blogdetails9(request):
	return render(request,'front-end/blog-details9.html')

def blogdetails10(request):
	return render(request,'front-end/blog-details10.html')

def blogdetails11(request):
	return render(request,'front-end/blog-details11.html')

def blogdetails12(request):
	return render(request,'front-end/blog-details12.html')

def blogdetails13(request):
	return render(request,'front-end/blog-details13.html')

def blogdetails14(request):
	return render(request,'front-end/blog-details14.html')

def blogdetails15(request):
	return render(request,'front-end/blog-details15.html')

def blogdetails16(request):
	return render(request,'front-end/blog-details16.html')

def blogdetails17(request):
	return render(request,'front-end/blog-details17.html')

def blogdetails18(request):
	return render(request,'front-end/blog-details18.html')


def blog_details(request):
    return render(request,'front-end/blog-details.html')
#************************************************************original code*****************************
# def shop_category(request):
#     data = Product.objects.all().order_by('-prod_date')
    
#     for d in data:
#         print(d.title)
#     context = {
#         'data':data,
#     }
#     return render(request,"front-end/shop-left-sidebar.html",context)
#*************************************************************************************************

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import F
from .models import CATEGORY_CHOICE 

def shop_category(request):
    # Get all products
    data = Product.objects.all()

    # Filter by category
    category_filter = request.GET.get('category')  # Get the selected category from the request

    if category_filter:
        data = data.filter(category=category_filter)

    # Filter by price range
    price_range = request.GET.get('price_range')  # Get the selected price range from the request

    if price_range:
        if price_range == '100-500':
            data = data.filter(discount_price__range=(100, 500))
        elif price_range == '600-1000':
            data = data.filter(discount_price__range=(600, 1000))
        elif price_range == 'above_1000':
            data = data.filter(discount_price__gte=1000)

    # Sorting by price
    sort_by = request.GET.get('sort_by')  # Get the sorting parameter from the request

    if sort_by == 'high_to_low':
        data = data.order_by(F('discount_price').desc(nulls_last=True))
    elif sort_by == 'low_to_high':
        data = data.order_by(F('discount_price').asc(nulls_last=True))

    per_page = 10
    paginator = Paginator(data, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'sort_by': sort_by,  # Pass the sorting parameter to the template
        'category_filter': category_filter,  # Pass the category filter to the template
        'price_range': price_range,  # Pass the price range filter to the template
        'CATEGORY_CHOICE': CATEGORY_CHOICE, 
    }

    return render(request, "front-end/shop-left-sidebar.html", context)
def Terms_Conditions(request):
    return render(request,'front-end/Terms&Conditions.html')

def Refund_Return_Policy(request):
    return render(request,'front-end/return_refund_policy.html')

def Privacy_Policy(request):
    return render(request,'front-end/privacy_policy.html')

def all_posts(request):
    posts = Post.objects.filter(status=1)
    
    for post in posts:
        print('Title:', post.title)
        print('Slug:', post.slug)
        print('Author:', post.author)
        print('Blog Image:', post.blog_img)
    
    return render(request, 'front-end/blog-infinite-scroll.html', {'posts': posts})

# def blog_details(request,id):
#     data=Post.objects.get(id=id)
#     print()
#     print('bapuuuuuuuuuuuuuu',data.created_on)
#     print()
#     return render(request,'front-end/blog-details.html',{'data':data})




def new_order(request):
    return render(request,'back-end/new-order.html')

def can_order(request):
    return render(request,'back-end/cancelled-order.html')

def profile_setting(request):
    return render(request,'back-end/profile-setting.html')


def products(request):
    products = Product.objects.order_by('-id')
    # products = Product.objects.all()
    print('mmmmmmmmmmmm',products)
    return render(request, 'back-end/products.html', {'products': products})
    #return render(request,'back-end/products.html')





def coupon_list(request):
    return render(request,'back-end/coupon-list.html')

def create_coupon(request):
    return render(request,'back-end/create-coupon.html')
#***************************************************************original code **************************

# def create_order(request):
#     custid = request.GET.get('custid')
#     user = request.user
#     pay = request.GET.get('flexRadioDefault')
#     cust = Customer.objects.get(id = custid)
#     cart = Cart.objects.filter(user = cust.user)
    
#     characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
#     order_id = ''.join(random.choices(characters, k=6))
    
#     print('order iddddddddddd',order_id)

#     for i in cart:
#         order = OrderPlaced(user = user, customer = cust,product = i.product ,quantity = i.quantity,order_id=order_id )
#         order.save()
#         print('idddddddddd',i.product)
#         i.delete()     
#     data = OrderPlaced.objects.filter(user = user,order_id = order_id)
#     total = 0
#     j = 1
#     while j <= len(data):
#         for i in data:
#             total =float(i.product.discount_price)*(i.quantity) + float(total)
#             j = j+1
#     tax = (total*18)/100      #18% tax
#     ship = int(50)
#     grand_total = tax +ship+ total
#     print(len(data))    
#     print('ffffffffffffffffff',total)
#     print()

#     context = {
#         'grand_total':grand_total,
#         'tax':tax,
#         'total':total,
#         'data':data,
#         'cust':cust,
#         'order_id':order_id, 
#         'cart':cart,    
#     }
#     print('cart',cart)
#     print('custadreesssssssss',custid)
    
#     print(cust.user)
#     print('methodddddddd',pay)
#     print()
#     return render(request,"front-end/order-success.html",context)


import string
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render

from .models import Customer, Cart, OrderPlaced

def create_order(request):
    custid = request.GET.get('custid')
    user = request.user
    pay = request.GET.get('flexRadioDefault')
    cust = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=cust.user)
    
    characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
    order_id = ''.join(random.choices(characters, k=6))
    
    print('order iddddddddddd', order_id)

    for i in cart:
        order = OrderPlaced(user=user, customer=cust, product=i.product, quantity=i.quantity, order_id=order_id)
        order.save()
        print('idddddddddd', i.product)
        i.delete()
    
    data = OrderPlaced.objects.filter(user=user, order_id=order_id)
    total = 0
    j = 1
    while j <= len(data):
        for i in data:
            total = float(i.product.discount_price) * i.quantity + float(total)
            j = j + 1
    tax = (total * 18) / 100  # 18% tax
    ship = int(50)
    grand_total = tax + ship + total
    print(len(data))    
    print('ffffffffffffffffff', total)
    print()

    # Send an email to the user
    subject = 'Your Order Has Been Placed Successfully'
    from_email = 'zappkodesolutions@gmail.com'  # Replace with your email
    recipient_list = [cust.user.email]

    # Create a dictionary with order details to pass to the email template
    email_context = {
        'order_items': data,
        'order_total': total,
        'order_tax': tax,
        'order_shipping': ship,
        'order_grand_total': grand_total,
    }

    # Render the email template to HTML content
    email_html_message = render_to_string('back-end/order_email_template.html', email_context)

    # Send the email
    send_mail(subject, '', from_email, recipient_list, html_message=email_html_message)

    context = {
        'grand_total': grand_total,
        'tax': tax,
        'total': total,
        'data': data,
        'cust': cust,
        'order_id': order_id,
        'cart': cart,    
    }
    print('cart', cart)
    print('custadreesssssssss', custid)
    
    print(cust.user)
    print('methodddddddd', pay)
    print()
    return render(request, "front-end/order-success.html", context)



#*******************************************************************************************************

def cancel_order(request,id):
    data = OrderPlaced.objects.get(id=id)
    data.delete()
    return redirect('/cust_dash/')




from django.http import JsonResponse
from django.views.decorators.http import require_POST
from customer.models import User, Product, Whishlist

from django.shortcuts import get_object_or_404


def add_wishlist(request):
    if request.method == 'GET':
        user = request.user
        item_id  = request.GET.get('item_id')
        product = get_object_or_404(Product, id=item_id)
        print()
        print('itemmmmmmmmmmmmmm',user,'idddddddddd',product)
        wishlist = Whishlist(user=user, product=product)
        wishlist.save()
        return redirect("/product_detail/{}/".format(item_id))



def show_wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        data = Whishlist.objects.filter(user = user)
        context={
            'data':data,
        }
        return render(request,'front-end/wishlist.html',context)
    else:
        return redirect("/accounts/login/")


def remove_w(request,id):
    data = Whishlist.objects.get(id =id)
    data.delete()
    return redirect('/show_wishlist/')

def wish_to_cart(request,id):
    user = request.user
    print('userrrrrrrrrrrrr',user)
    wish = Whishlist.objects.get(id = id)
    print(wish.product)
    if request.user == wish.user:
        item = Cart(user=user,product=wish.product)
        item.save()
        wish.delete()
    return redirect('/show_wishlist/')


#customer Dashboard
@login_required
def cust_dash(request):
    user = CustProfile.objects.get(user = request.user)
    order = OrderPlaced.objects.filter(user = request.user).order_by('-Order_date')
    order_count = OrderPlaced.objects.filter(user = request.user).count()
    wishlist = Whishlist.objects.filter(user = request.user).count()
    order_pending = OrderPlaced.objects.filter(user=request.user,status = 'Pending').count()
    print('orderrrrrrr',order_count)
    add = Customer.objects.filter(user = request.user)
    context = {'add':add,'user':user,'order':order,'order_count':order_count,'order_pending':order_pending,'wishlist':wishlist}
    return render(request,'front-end/user-dashboard.html',context)

def save_customer(request):
    if request.method == 'POST':
        # Extract data from the POST request
        fname = request.POST.get('fname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        print('ooooooooooooooooooooooooooo',fname,mobile,email,locality,city,state,pincode)
        # Create a new Customer object and save it to the database
        customer = Customer(
            user=request.user,  # Assuming you have a logged-in user
            name=fname,
            email=email,
            mobile=mobile,
            locality=locality,
            city=city,
            state=state,
            pincode=pincode
        )
        customer.save()
    return redirect('/cust_dash/')


def save_customer1(request):
    if request.method == 'POST':
        # Extract data from the POST request
        fname = request.POST.get('fname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        print('ooooooooooooooooooooooooooo',fname,mobile,email,locality,city,state,pincode)
        # Create a new Customer object and save it to the database
        customer = Customer(
            user=request.user,  # Assuming you have a logged-in user
            name=fname,
            email=email,
            mobile=mobile,
            locality=locality,
            city=city,
            state=state,
            pincode=pincode)
        
        customer.save()
    return redirect('/checkout_log/')


def update_customer(request,id):
    data = CustProfile.objects.get(id=id)
    if request.method == 'POST':
        data.name = request.POST.get('name')
        data.email = request.POST.get('email')
        data.mobile = request.POST.get('mobile')
        data.date_of_birth = request.POST.get('date_of_birth')
        data.locality = request.POST.get('locality')
        data.city = request.POST.get('city')
        data.state = request.POST.get('state')
        data.pincode = request.POST.get('pincode')

        data.save()
        
    print()
    print('dataaaaaa==',data)
    print()
    return redirect('/cust_dash/')




def my_payment(request):
    return render(request,'back-end/payment.html')

def payment_history(request):
    return render(request,'back-end/payment_history.html')


from django.contrib.auth import login, get_user_model
from django.core.mail import send_mail
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import Seller
from .forms import SellerRegistration

def seller_registration(request):
    if request.method == 'POST':
        form = SellerRegistration(request.POST)

        if form.is_valid():
            user = form.save()

            # Create a Seller instance and populate the additional fields
            seller = Seller(
                user=user,
                company_name=form.cleaned_data['company_name'],
                company_address=form.cleaned_data['company_address'],
                mobile_no=form.cleaned_data['mobile_no'],
                seller=True
            )

            seller.save()

            # Send registration confirmation email
            subject = "Seller Registration Confirmation"
            message = f"Hello {user.username},\n\nThank you for registering as a seller on our website.\n\nBest regards,\nMahesh Talmale"
            from_email = "zappkodesolutions@gmail.com"  # Replace this with your desired 'from' email address
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Log the user in after registration
            user.backend = f"{get_user_model()._meta.app_label}.backends.CustomBackend"  # Replace 'CustomBackend' with your actual backend name
            login(request, user)

            # Redirect to the seller_login page
            return redirect('/seller_login/')
    else:
        form = SellerRegistration()

    return render(request, 'front-end/seller_registration.html', {'form': form})

# from django.contrib import messages

# def seller_registration(request):
#     if request.method == 'POST':
#         form = SellerRegistration(request.POST)

#         if form.is_valid():
#             user = form.save()

#             # Create a Seller instance and populate the additional fields
#             seller = Seller(
#                 user=user,
#                 company_name=form.cleaned_data['company_name'],
#                 company_address=form.cleaned_data['company_address'],
#                 mobile_no=form.cleaned_data['mobile_no'],
#                 seller=True
#             )

#             seller.save()

#             # Send registration confirmation email
#             subject = "Seller Registration Confirmation"
#             message = f"Hello {user.username},\n\nThank you for registering as a seller on our website.\n\nBest regards,\nMahesh Talmale"
#             from_email = "zappkodesolutions@gmail.com"  # Replace this with your desired 'from' email address
#             recipient_list = [user.email]
#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#             # Log the user in after registration
#             user.backend = f"{get_user_model()._meta.app_label}.backends.CustomBackend"  # Replace 'CustomBackend' with your actual backend name
#             login(request, user)

#             # Redirect to the seller_login page
#             return redirect('/seller_login/')

#         else:
#             messages.error(request, "Passwords do not match. Please enter matching passwords.")
#             return render(request, 'front-end/seller_registration.html', {'form': form, 'trigger_sweetalert': True})
#     else:
#         form = SellerRegistration()

#     return render(request, 'front-end/seller_registration.html', {'form': form})




from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SellerLoginForm  
from .models import Seller  

def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request, request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if the user is a seller
                try:
                    seller = Seller.objects.get(user=user)
                    if seller.is_seller:
                        # Log the user in
                        login(request, user)
                        
                        return redirect('/seller_dashboard/')  
                except Seller.DoesNotExist:
                    pass  

    else:
        form = SellerLoginForm()

    return render(request, 'front-end/seller_login.html', {'form': form})

#seller seaction

def cheack_seller(request, id):
    # Retrieve the seller instance based on the 'id' parameter
    seller = get_object_or_404(Seller, id=id)
    print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu',seller)

    # Set 'is_seller' to True and save the instance
    seller.is_seller = True
    seller.save()


def approve_seller(request, id):
    try:
        seller = Seller.objects.get(pk=id)
        seller.seller=False
        seller.is_seller = True
        seller.save()
        return redirect('/vendor_list/')  # Assuming 'vendor_list' is the name of your vendor list view
    except Seller.DoesNotExist:
        
        return redirect('/vendor_list/')  # Redirect to the vendor list view

def delete_seller(request,id):
    try:
        seller = Seller.objects.get(pk=id)
        seller.delete()
        # You can add a success message or redirect to a different page
        return redirect('/vendor_list/')  # Assuming 'vendor_list' is the name of your vendor list view
    except Seller.DoesNotExist:
        
        return redirect('/vendor_list/')  # Redirect to the vendor list view



from django.shortcuts import render, redirect
from .models import SellerProduct

def seller_add_product(request):
    if request.method == 'POST':
        user = request.user
        print('pijjjnhkjbjh',user)
        title = request.POST.get('title')
        selling_price = request.POST.get('selling_price')
        discount_price = request.POST.get('discount_price')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        product_image = request.FILES.get('product_image')
        back_image = request.FILES.get('back_image')
        left_image = request.FILES.get('left_image')
        right_image = request.FILES.get('right_image')
        product_video = request.FILES.get('product_video')

        # Fetch the logged-in user
        

        # Check if the user is a seller and has a Seller profile
        if hasattr(user, 'seller'):
            seller = user.seller
        else:
            
            return render(request, 'error.html', {'message': 'You are not a seller.'})

        # Create a new SellerProduct instance and save it to the database
        product = SellerProduct(
            seller=seller,
            title=title,
            selling_price=selling_price,
            discount_price=discount_price,
            description=description,
            brand=brand,
            category=category,
            product_image=product_image,
            back_image=back_image,
            left_image=left_image,
            right_image=right_image,
            product_video=product_video,
        )
        
        # Save the uploaded files to the appropriate directory
        product.save()

        return redirect('/seller_add_product/')

        # Redirect to a success page or seller dashboard
          # Adjust to the actual success page URL name

    return render(request, 'back-end/new-seller-add-product.html')



def seller_view_product(request):
    # Fetch the logged-in user
    user = request.user
    print('9999999999999999999999999999',user)
    # Check if the user is a seller and has a Seller profile
    if hasattr(user, 'seller'):
        seller = user.seller
        # Now you can use the 'seller' variable
        seller_products_view = SellerProduct.objects.filter(seller=seller,unapproved=True)
        print('yyyyyyyy', seller_products_view)

        return render(request, 'back-end/products.html', {'seller_products_view': seller_products_view})
    else:
        return render(request, 'error.html', {'message': 'You are not a seller.'})

#admin view product 
def admin_view_product(request):
    # Fetch the logged-in user
    user = request.user
    print('9999999999999999999999999999',user)
    # Check if the user is a seller and has a Seller profile
    if hasattr(user, 'seller'):
        seller = user.seller
        # Now you can use the 'seller' variable
        seller_products_view = SellerProduct.objects.filter(seller=seller,unapproved=True)
        print('yyyyyyyy', seller_products_view)

        return render(request, 'back-end/admin_product.html', {'seller_products_view': seller_products_view})
    else:
        return render(request, 'error.html', {'message': 'You are not a seller.'})


def approve_seller_product(request, product_id):
    try:
        product = get_object_or_404(SellerProduct, pk=product_id)
        
        if request.method == 'POST':
            # Check if the form was submitted (button clicked)
            product.unapproved = False
            product.approved_product = True
            product.save()
            return redirect('/seller_view_product/')  # Redirect to the seller product list view
        
        return render(request, 'approve_seller_product.html')
    
    except SellerProduct.DoesNotExist:
        return redirect('seller_product_list')


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Add logic to delete the product, e.g., calling product.delete()
    product.delete()
    return redirect('/product_list/')  # Redirect to the product list page


def view_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)
    return render(request, 'back-end/product_detail.html', {'product': product})



def approve_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)
    
    if request.method == 'POST':
        # Mark the product as approved (you can update any other fields as needed)
        product.approved_product = True
        product.save()
        
        # Redirect to the product detail page after approving
        return redirect('view_product', product_id=product_id)
    
    return render(request, 'back-end/product_detail.html', {'product': product})


from django.shortcuts import render
from .models import SellerProduct
from .forms import SellerFilterForm

def seller_show_product(request):
    if request.method == 'POST':
        form = SellerFilterForm(request.POST)
        if form.is_valid():
            selected_seller = form.cleaned_data.get('seller')
            approved_products = SellerProduct.objects.filter(approved_product=True)
            
            if selected_seller:
                approved_products = approved_products.filter(seller=selected_seller)
    else:
        form = SellerFilterForm()
        approved_products = SellerProduct.objects.filter(approved_product=True)

    context = {
        'my_products': approved_products,
        'form': form,
    }

    return render(request, 'back-end/approved_product.html', context)




from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomPasswordChangeForm

class CustomPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'back-end/password_change_form.html'
    success_url = '/password-change-done/'  # URL to redirect after a successful password change
    success_message = "Your password has been successfully changed."




def blogdetails11(request):
    return HttpResponse("This is blog details 11")

def blogdetails12(request):
    return HttpResponse("This is blog details 12")

def blogdetails13(request):
    return HttpResponse("This is blog details 13")

def blogdetails14(request):
    return HttpResponse("This is blog details 14")

def blogdetails15(request):
    return HttpResponse("This is blog details 15")

def blogdetails16(request):
    return HttpResponse("This is blog details 16")

def blogdetails17(request):
    return HttpResponse("This is blog details 17")

def blogdetails18(request):
    return HttpResponse("This is blog details 18")




from .models import Product

def custom_product_list(request):
    products = Product.objects.all()
    return render(request, 'back-end/product_list.html', {'products': products})


#edit
from django.shortcuts import render
from .models import Seller

def seller_profile(request):
    
    logged_in_user = request.user
    try:
        seller = Seller.objects.get(user=logged_in_user)
    except Seller.DoesNotExist:
        seller = None

    context = {
        'seller': seller,
    }

    return render(request, 'back-end/seller_profile.html', context)



from .models import Seller
from .forms import SellerProfileForm  # Create a form for editing seller profiles

def edit_seller_profile(request):
    logged_in_user = request.user
    try:
        seller = Seller.objects.get(user=logged_in_user)
    except Seller.DoesNotExist:
        seller = None

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            return redirect('/seller_dashboard/')

    else:
        form = SellerProfileForm(instance=seller)

    context = {
        'seller': seller,
        'form': form,
    }

    return render(request, 'back-end/edit_seller_profile.html', context)



from .models import Product

def custom_product_list(request):
    products = Product.objects.all()
    return render(request, 'back-end/product_list.html', {'products': products})


#seller able to seen their own product

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SellerProduct

@login_required
def seller_self_show_product(request):
    try:
        # Fetch all approved products associated with the logged-in seller
        approved_products = SellerProduct.objects.filter(seller=request.user, approved_product=True)
    except SellerProduct.DoesNotExist:
        approved_products = []

    context = {
        'my_products': approved_products,
    }

    return render(request, 'back-end/approved_product.html', context)



#test code ..................................

def my_seller_view_product(request):
    # Fetch the logged-in user
    user = request.user
    print('9999999999999999999999999999',user)
    # Check if the user is a seller and has a Seller profile
    if hasattr(user, 'seller'):
        seller = user.seller
        # Now you can use the 'seller' variable
        seller_products_view = SellerProduct.objects.filter(seller=seller,unapproved=True)
        print('yyyyyyyy', seller_products_view)

        return render(request, 'back-end/sproducts.html', {'seller_products_view': seller_products_view})
    else:
        return render(request, 'back-end/error.html', {'message': 'You are not a seller.'})


#edit product
from django.shortcuts import render, get_object_or_404, redirect
from .models import SellerProduct

def edit_product(request, product_id):
    product = get_object_or_404(SellerProduct, id=product_id)

    if request.method == 'POST':
        # Handle form submission and update the product here
        product.title = request.POST['title']
        product.selling_price = request.POST['selling_price']
        product.discount_price = request.POST['discount_price']
        product.description = request.POST['description']
        product.brand = request.POST['brand']
        product.category = request.POST['category']
        product.unapproved = bool(request.POST.get('unapproved'))
        product.approved_product = bool(request.POST.get('approved_product'))
        product.save()
        return redirect('/seller_dashboard/')  # Redirect to the product list page after editing
    else:
        context = {'product': product}
        return render(request, 'back-end/edit_product.html', context)




#customized T-shirt Views

def custome_tshirts(request):
    return render(request,"front-end/customize-tshirts.html")

# def custome_mug(request):
#     return HttpResponse(request,"front-end/")


def del_add(request,id):
    data = Customer.objects.get(id = id)
    data.delete()
    return redirect('/cust_dash/')