from django.contrib.auth import authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .models import *
from .tokens import account_activation_token
from .serializer import AccountRegisterSerializer
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework import views
# Create your views here.

class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request':request})
        if not serializer.is_valid():
            return Response({'user not found'})
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})


class AccountRegisterView(views.APIView):

    def get(self, *args, **kwargs):
        return Response({'data': {
            'name':'examplename',
            'username': 'exampleuser',
            'email': 'example@mail.ru',
            'last_name': 'last_name',
            'password': '2233',
            'password2':'2233'

        }})

    def post(self, request, *args, **kwargs):
        serializer = AccountRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'OGOGO team'
            message = render_to_string('register/activation.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),

            })
            to_email = serializer.data['email']
            email = EmailMessage(subject,message,to=[to_email,])
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')