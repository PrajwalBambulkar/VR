from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


STATE_CHOICES=(
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh ","Arunachal Pradesh "),
    ("Assam","Assam"),("Bihar","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),
    ("Jammu and Kashmir ","Jammu and Kashmir "),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Odisha","Odisha"),
    ("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),
    ("Telangana","Telangana"),
    ("Tripura","Tripura"),
    ("Uttar Pradesh","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),
    ("West Bengal","West Bengal"),
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Chandigarh","Chandigarh"),
    ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
    ("Daman and Diu","Daman and Diu"),
    ("Lakshadweep","Lakshadweep"),
    ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
    ("Puducherry","Puducherry")
)

# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,default=None, null=True, blank=True)
    mobile = models.CharField(max_length=15,default=None, null=True, blank=True)
    locality = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=5000)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICE = (
    ('TS',"Clothes"),
    ('AC','Accessories'),
    ('BK','Books'),
    ('PT','Painting'), 
)

class Product(models.Model):
    title = models.CharField(max_length=150)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICE,max_length=15)
    product_image = models.ImageField(upload_to='productimg',blank=True, null=True,default="")
    back_image = models.ImageField(upload_to='productimg', blank=True, null=True)
    left_image = models.ImageField(upload_to='productimg', blank=True, null=True,default="")
    right_image = models.ImageField(upload_to='productimg', blank=True, null=True,default="")
    product_video = models.FileField(upload_to='productvideos',default="", null=True, blank=True)
    prod_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,)
    anonymous_user_id = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,null=True, blank=True)
    size = models.CharField(max_length=15,default="S", null=True, blank=True)
    def __str__(self):
        return str(self.id)
    


STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed',"packed"),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)    

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_id = models.CharField(max_length=10,null=True, blank=True)
    Order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices = STATUS_CHOICE ,default ='Pending')


STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
  title =  models.CharField(max_length=200, unique=True)
  slug =   models.SlugField(max_length=200, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  content = models.TextField()
  status = models.IntegerField(choices=STATUS, default=0)
  blog_img=models.ImageField(upload_to='productimg/',blank=True, null=True)

  

  class Meta:
    ordering = ['-created_on']

  def __str__(self):
    return self.title

class Banner(models.Model):
    ban_name = models.CharField(max_length=250 ,default="banner1")
    ban_image1 = models.ImageField(upload_to='bannerimg',null=True,blank=True)
    ban_image2 = models.ImageField(upload_to='bannerimg',null=True,blank=True)
    ban_image3 = models.ImageField(upload_to='bannerimg',null=True,blank=True)


# class Poster(models.Model):
#     poster_name = models.CharField(max_length=250 ,default = 'poster1')
#     poster1 = models.ImageField(upload_to='posterimg',null=True,blank=True)
#     poster2 = models.ImageField(upload_to='posterimg',null=True,blank=True)
#     poster3 = models.ImageField(upload_to='posterimg',null=True,blank=True)


class Category(models.Model):
    image = models.ImageField(upload_to='categoryimg',null=True,blank=True)
    cat_name = models.CharField(max_length=150,null=True,blank=True)


class ContactUs(models.Model):
    f_name = models.CharField(max_length=250)
    l_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,default=None, null=True, blank=True)
    comment = models.CharField(max_length=1500)

class Poster(models.Model):
   poster_name = models.CharField(max_length = 250 , default='poster1')
   poster1 = models.ImageField(upload_to='posterimg', blank=True, null=True)
   poster2 = models.ImageField(upload_to='posterimg', blank=True, null=True)
   poster3 = models.ImageField(upload_to='posterimg', blank=True, null=True)



class Whishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
     

class CustProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default=None, null=True, blank=True)
    email = models.EmailField(max_length=250, default=None, null=True, blank=True)
    mobile = models.CharField(max_length=15, default=None, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    locality = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    pincode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=5000, null=True, blank=True)
    is_customer = models.BooleanField(default=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_google_login = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, null=True, blank=True)
    google_access_token = models.CharField(max_length=255, null=True, blank=True)



class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    is_seller= models.BooleanField(default=False)
    seller=models.BooleanField(default=False)
    company_address = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=15)  # Add mobile_no field to match the form

    def __str__(self):
        return self.company_name



from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your custom fields here, for example:
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username

    
     

 
class SellerProduct(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=150)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=15)
    product_image = models.ImageField(upload_to='productimg', blank=True, null=True, default="")
    back_image = models.ImageField(upload_to='productimg', blank=True, null=True)
    left_image = models.ImageField(upload_to='productimg', blank=True, null=True, default="")
    right_image = models.ImageField(upload_to='productimg', blank=True, null=True, default="")
    product_video = models.FileField(upload_to='productvideos', default="", null=True, blank=True)
    unapproved=models.BooleanField(default=True)
    approved_product = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class SellerApprovedProduct(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=150)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=15)
    product_image = models.ImageField(upload_to='approved_product_img', blank=True, null=True, default="")
    back_image = models.ImageField(upload_to='productimg', blank=True, null=True)
    left_image = models.ImageField(upload_to='productimg', blank=True, null=True, default="")
    right_image = models.ImageField(upload_to='productimg', blank=True, null=True, default="")
    product_video = models.FileField(upload_to='productvideos', default="", null=True, blank=True)
    approved = models.BooleanField(default=False)  # Add this field for approval status

    # Add other fields as needed

    def __str__(self):
        return str(self.id)



