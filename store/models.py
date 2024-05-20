from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Manzil (mo'ljal)")
    city = models.CharField(max_length=150, verbose_name="Shaxar")
    state = models.CharField(max_length=150, verbose_name="Viloyat")

    def __str__(self):
        return self.locality

    class Meta:
        verbose_name = "Katalog"
        verbose_name_plural = "Kataloglar"


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Katalog nomi")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Katalog uchun ta'rif")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Katalog uchun rasm")
    is_active = models.BooleanField(verbose_name="Yaroqlimi ?")
    is_featured = models.BooleanField(verbose_name="Tanlangnami ?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    class Meta:
        verbose_name_plural = 'Kataloglar'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Maxsulot nomi")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="(SKU)")
    short_description = models.TextField(verbose_name="Qisqacha tavsif")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Ko'proq ma'lumot")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Maxsulot rasmi")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Maxsulot turi", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Faolmi ?")
    is_featured = models.BooleanField(verbose_name="Tanlanganmi ?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name_plural = 'Maxsulotlar'
        verbose_name = 'Maxsulot'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Maxsulot", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma qilingan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    def __str__(self):
        return str(self.user)
    
    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Yetkazib berish manzili", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Mahsulot", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Miqdor")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma sanasi")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
