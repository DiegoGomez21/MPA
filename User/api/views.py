from django import forms
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy,reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from User.api.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from User.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.middleware.csrf import get_token
from django.conf import settings


class LoginView(TokenObtainPairView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            token = response.data['access']
            request.session['access_token'] = token
            return redirect('posts-list')
        return response

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def _add_csrf_cookie(self, request, response):
        if settings.CSRF_COOKIE_NAME not in response.cookies:
            csrf_token = get_token(request)
            response.set_cookie(settings.CSRF_COOKIE_NAME, csrf_token, max_age=settings.CSRF_COOKIE_AGE, domain=settings.CSRF_COOKIE_DOMAIN, secure=settings.CSRF_COOKIE_SECURE, httponly=settings.CSRF_COOKIE_HTTPONLY, samesite=settings.CSRF_COOKIE_SAMESITE)
        return response

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response = self._add_csrf_cookie(request, response)
        return response



#SE HACE NECESARIO ENCRIPTAR LA CONTRASEÑA
class RegisterView(APIView):

    template_name = 'user/register.html'
    form_class = AuthenticationForm

    def register_user(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect(reverse_lazy('login'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        return self.register_user(request)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'register_user': self.register_user})



class UserView(APIView):
    permission_classes = [IsAuthenticated] #Solo los usuarios autenticados podrán acceder
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        #request.user.id
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, request.data) #Aqui es donde vamos a actualizar los datos
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

