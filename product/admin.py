from unicodedata import category
from django.contrib import admin

from product.forms import ProductForm
from .models import Product,Brand, ProductImage, SubCategory,Type,Category
# Register your models here.

from ajax_select.admin import AjaxSelectAdmin
from ajax_select import make_ajax_form
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField

class ProductImageTabularInline(admin.TabularInline):

    model = ProductImage
        



class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageTabularInline,)

    form = ProductForm

    class Media:
        js = (
            'js/main.js',
        )

   
admin.site.register(Product,ProductAdmin)
admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SubCategory,Category


@login_required
def category_list(request):
    category = Category.objects.all()
    return JsonResponse({'data': [{'id': p.id, 'name': p.name} for p in category]})





