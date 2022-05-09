from django import template
register = template.Library()
from users.models import CustomUser


@register.filter
def get_user_by_id(id):
    print(id)
    try:
        user = CustomUser.objects.get(id=id)
        return user.phone
    except:
    # print(user)
        return ''