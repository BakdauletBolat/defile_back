from ajax_select import register, LookupChannel
from .models import SubCategory,Category

@register('subcategory')
class SubCategoryLookup(LookupChannel):

    model = SubCategory

    def get_query(self, id, request):
        return self.model.objects.filter(id=id)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name

