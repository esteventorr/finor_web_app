from firebase_admin import auth

class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtén el token del encabezado de la solicitud
        token = request.META.get('HTTP_AUTHORIZATION')

        if token:
            try:
                # Verifica el token con Firebase
                decoded_token = auth.verify_id_token(token)
                request.user = auth.get_user(decoded_token['uid'])
            except:
                # Si el token no es válido, establece el usuario en None
                request.user = None

        response = self.get_response(request)

        return response