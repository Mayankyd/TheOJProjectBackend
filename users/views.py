from django.http import JsonResponse

def login_user(request):
    return JsonResponse({'message': 'Login endpoint'})

def register_user(request):
    return JsonResponse({'message': 'Register endpoint'})
