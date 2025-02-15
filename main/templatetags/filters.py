from django import template
from django.utils.html import format_html
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='unbox_json')
def unbox_json(value, key):
    return value[key]

@register.simple_tag
def scissors(description, length):
    if description and len(description) > length:
        return format_html('{}...', description[:length])
    return description

@register.simple_tag
def translate_date(date_obj):
    utc = datetime.utcnow()
    date_obj = date_obj + timedelta(hours=3)
    month_names = {
        1: 'янв', 2: 'фев', 3: 'март', 4: 'апр', 5: 'май',
        6: 'июнь', 7: 'июль', 8: 'авг', 9: 'сент', 10: 'окт', 
        11: 'нояб', 12: 'дек'
    }

    return f"{date_obj.day} {month_names[date_obj.month]} {date_obj.year}"