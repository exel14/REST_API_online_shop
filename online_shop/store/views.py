from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['price','name']

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class UPDOrderView(APIView):

    def put(self,request,*args,**kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        serializers = OrderSerializer(order,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'data':'seccess'})

    def delete(self,request,*args,**kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.delete()
        return Response({'data':'seccess'})

class ProductToOrderView(APIView):

    def get(self,request,*args,**kwargs):
        orders = ProductToOrder.objects.all()
        serializers = ProductToOrderSerializer(orders,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializers = ProductToOrderSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
