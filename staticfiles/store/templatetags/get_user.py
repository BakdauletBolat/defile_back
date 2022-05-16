from django import template
from users.models import CustomUser
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def get_user_by_id(id):
    print(id)
    try:
        user = CustomUser.objects.get(id=id)
        return mark_safe(f"""<div class="form__user" style='padding: 20px 0px;'>
                                <div class='form_title'>Номер телефона заказчика: {user.phone}</div>
                                <div class='form_title'>ФИО заказчика: {user.fullname}</div>
                            </div>""")
    except:
    # print(user)
        return ''