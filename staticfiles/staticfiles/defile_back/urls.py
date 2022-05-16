import uuid
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path,include
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from product.models import SubCategory


@login_required
def subcategory_list(request, category):
    subcategory = SubCategory.objects.filter(category_id=category)
    return JsonResponse({'data': [{'id': k.id, 'name': k.name} for k in subcategory]})

def index(request):
    return render(request,'index.html')

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('ajax/get_subcategory/<int:category>',subcategory_list),
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('', index),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
