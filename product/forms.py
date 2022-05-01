from django import forms
from .models import Category, Product, SubCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        try:
            self.initial['category'] = kwargs['instance'].category.id
        except:
            pass
        category_list = [('', '---------')] + [(i.id, i.name) for i in Category.objects.all()]
       
        self.fields['category'].widget = forms.Select(
            attrs={
                'id': 'id_category',
                'onchange': 'getSubCategory(this.value)',
                'style': 'width:200px'
            },
            choices=category_list,
        )
     
      