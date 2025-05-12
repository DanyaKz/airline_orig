import datetime
from django.utils.deprecation import MiddlewareMixin

class FirstVisitMiddleware(MiddlewareMixin):
    
    # проверяем визит
    def process_request(self, request):
        if not request.COOKIES.get('first_visit'):
            print("Новый пользователь обнаружен!")
            request.is_new_user = True
        else:
            request.is_new_user = False

    #  редачим кукис
    def process_response(self, request, response):
        if getattr(request, 'is_new_user', False):
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=365)
            response.set_cookie('first_visit', '1', expires=expires)
            print("+юзер")
        return response
