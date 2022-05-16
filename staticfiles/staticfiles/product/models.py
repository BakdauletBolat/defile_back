from unicodedata import category
from django.db import models

from users.models import CustomUser



class Brand(models.Model):

    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='brand-p/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
    

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='category-p/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'

    def __str__(self):
        return self.name


class SubCategory(models.Model):

    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='category-p/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategorires')
    
    class Meta:
        verbose_name = 'Под категория'
        verbose_name_plural = 'Под категорий'

    def __str__(self):
        return f"""{self.category.name}: {self.name}"""


class Type(models.Model):

    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='type-p/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.BigIntegerField()
    price_stock = models.BigIntegerField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_stock = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='products')
    type = models.ForeignKey(Type,on_delete=models.CASCADE,related_name='products')
    owner = models.ForeignKey(CustomUser,null=True,blank=True,related_name='products',on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return f"""{self.brand.name}: {self.name}"""


class ProductFavorites(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='likes')
    session_id = models.CharField(max_length=255,null=True,blank=True)
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True,related_name='likes')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

class ProductImage(models.Model):

    name = models.CharField(max_length=255,null=True,blank=True)
    photo = models.ImageField(upload_to='product-images/')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    

    class Meta:
        verbose_name = 'Фотография продукта'
        verbose_name_plural = 'Фотографий продукта'
