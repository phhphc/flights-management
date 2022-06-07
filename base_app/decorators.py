from django.shortcuts import redirect


def employee_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_superuser or request.user.groups.filter(name='Employee').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')

    return wrapper_func
