from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []  # Important: disable DRF authentication here
    permission_classes = []      # Important: disable DRF permissions here

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, first_name=name)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
