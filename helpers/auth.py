from django.shortcuts import redirect

# Esto es un "decorador", que es una función de orden superior que toma una vista y devuelve una nueva vista
def require_auth(view_func):
    # Esta es la nueva vista que se devuelve
    def _wrapped_view_func(request, *args, **kwargs):
        try:
            request.session['user_display_name']
        except KeyError:
            # Las claves 'user_display_name' y/o 'user_uid' no existen en la sesión, redirige al usuario a la página de inicio de sesión
            return redirect('loginpage')

        # Si el usuario está autenticado, ejecuta la vista original
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view_func