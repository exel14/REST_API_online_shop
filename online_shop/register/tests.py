from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import *

class AccountTestCase(APITestCase):

    def setUp(self):
        self.create_url = reverse('create')
        Account.objects.create(name='lalal',
                               last_name='lalal123',
                               username='eXeL',
                               email='showmetheway220@gmail.com',
                               password='1234qwer')

    def test_account_create(self):
        data = {
            "name":"Danil",
            "last_name":"Atiakov",
            "email":"showmetheway22@gmail.com",
            "username":"eXeL123",
            "password":"1234qwer",
            "password2":"1234qwer"
        }
        self.response = self.client.post(self.create_url,data)
        self.assertEqual(self.response.status_code,status.HTTP_201_CREATED)
        print(self.response.data)

    def test_account_create_empty_username(self):
        data = {
            "name": "Danil",
            "last_name": "Atiakov",
            "email": "showmetheway220@gmail.com",
            "username": "",
            "password": "1234qwer",
            "password2": "1234qwer"
        }
        self.response = self.client.post(self.create_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        print(self.response.data)

    def test_account_empty_email(self):
        data = {
            "name": "Danil",
            "last_name": "Atiakov",
            "email": "",
            "username": "eXeL",
            "password": "1234qwer",
            "password2": "1234qwer"
        }
        self.response = self.client.post(self.create_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        print(self.response.data)

    def test_account_password_doesnt_much(self):
        data = {
            "name": "Danil",
            "last_name": "Atiakov",
            "email": "showmetheway220@gmail.com",
            "username": "eXeL",
            "password": "1234qwer",
            "password2": "1234qwer1"
        }
        self.response = self.client.post(self.create_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        print(self.response.data)

    def test_account_empty_name_last_name(self):
        data = {
            "name": "",
            "last_name": "",
            "email": "showmetheway220@gmail.com",
            "username": "eXeL",
            "password": "1234qwer",
            "password2": "1234qwer"
        }
        self.response = self.client.post(self.create_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        print(self.response.data)

    def test_account_create_username_duplicate(self):
        data = {
            "name":"Danil",
            "last_name":"Atiakov",
            "email":"showmetheway220@gmail.com",
            "username":"eXeL",
            "password":"1234qwer",
            "password2":"1234qwer"
        }
        self.response = self.client.post(self.create_url,data)
        self.assertEqual(self.response.status_code,status.HTTP_400_BAD_REQUEST)
        print(self.response.data)

    def test_account_create_email_duplicate(self):
        data = {
            "name": "Danil",
            "last_name": "Atiakov",
            "email": "showmetheway22@gmail.com",
            "username": "eXeL",
            "password": "1234qwer",
            "password2": "1234qwer"
            }
        self.response = self.client.post(self.create_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        print(self.response.data)

class AuthTestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')

    def account_test_sign_in(self):
        data = {
            "username": "eXeL123",
            "password": "1234qwer",
        }
        self.response = self.client.post(self.login_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
