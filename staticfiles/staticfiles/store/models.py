from tabnanny import verbose
from django.db import models
from product.models import Product
from users.models import CustomUser
# Create your models here.


class Order(models.Model):

    STATUS_CHOICES = [
        ('ожидает', 'ожидает'),
        ('принят', 'принят'),
        ('процессе', 'процессе'),
        ('выполнен', 'выполнен'),
    ]

    session_id = models.CharField(null=True,blank=True,max_length=255)
    owner = models.ForeignKey(CustomUser,null=True,blank=True,related_name='orders',on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,max_length=12,default='ожидает')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):

    product = models.ForeignKey(Product,related_name='orderitems',on_delete=models.CASCADE)
    order = models.ForeignKey(Order,related_name='orderitems', on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Под заказы'
        verbose_name_plural = 'Под заказы'