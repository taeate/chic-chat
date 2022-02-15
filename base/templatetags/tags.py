from django.template.defaulttags import register

@register.filter
def namefilter(value,args):
    """
    user1user2|namefilter:request.user.username
    """
    return value.split(args)[0]
    return value
