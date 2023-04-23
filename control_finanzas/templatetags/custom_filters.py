from django import template 
import locale
register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='percentage')
def percentage(value, arg):
    return (value / arg) * 100
  
@register.filter(name='absolute')
def absolute(value):
    return abs(value)
  
@register.filter(name='to_float')
def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
      
@register.filter(name='get_value_by_key')
def get_value_by_key(dictionary, key):
    return dictionary.get(key, 0)
  
@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key, 0)

@register.filter(name='abs_value')
def abs_value(value):
    return abs(value)
  
def custom_number_format(number):
    number_str = f"{number:.2f}"
    int_part, decimal_part = number_str.split('.')
    int_parts = []
    count = 1
    while len(int_part) > 0:
        if count % 2 == 1:
            separator = ','
        else:
            separator = "'"
        int_parts.append(int_part[-3:])
        int_part = int_part[:-3]
        if len(int_part) > 0:
            int_parts.append(separator)
        count += 1
    formatted_number = "".join(reversed(int_parts)) + '.' + decimal_part
    return formatted_number

@register.filter(name='currency')
def currency(number, symbol='$', grouping=True): 

    # Redondear el número a dos decimales
    rounded_number = round(number, 2)

    # Aplicar el formato personalizado al número
    formatted_number = custom_number_format(rounded_number)

    # Agregar el símbolo de moneda y el código al principio y al final, respectivamente
    return f"{symbol} {formatted_number} COP"
  
@register.filter(name='to_float')
def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0