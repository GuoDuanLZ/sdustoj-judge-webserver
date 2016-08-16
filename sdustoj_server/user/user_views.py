from django.shortcuts import render


def render_with_user_info(request, template_name, context=None, **kwargs):
    user = request.user
    if user.is_authenticated():
        user_info = {'authenticated': True,
                     'username': user.username,
                     'group': user.groups,
                     'firstname':user.first_name,
                     'lastname':user.last_name,
                     'email':user.email
                        }
    else:
        user_info = {'authenticated': False}
    if context is None:
        context = dict()
    context['user_info'] = user_info
    return render(request, template_name, context, **kwargs)
