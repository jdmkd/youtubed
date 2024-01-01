from django import template

register = template.Library()

@register.filter()
def custom_duration_format(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    print(f"{minutes:02d}:{remaining_seconds:02d}")
    return f"{minutes:02d}:{remaining_seconds:02d}"
# <p>Duration : {{ yt.length|custom_duration_format }} minutes</p>
# This will format the duration as "04:61 minutes" without rounding. Please adapt the code as needed for your specific template system if you're not using Django templates.

@register.filter()
def split_float(value):
    # Split the floating-point number into its integer and decimal parts
    integer_part = int(value)
    decimal_part = int((value - integer_part) * 100)  # Multiply by 100 to get the two decimal digits

    # return integer_part, decimal_part
    return f"{integer_part:02d}:{decimal_part:02d}"




