from django.contrib.auth.decorators import user_passes_test

def role_required(required_role):
    def decorator(view_func):
        return user_passes_test(
            lambda u: u.is_authenticated and u.role == required_role,
            login_url='/login/'
        )(view_func)
    return decorator
