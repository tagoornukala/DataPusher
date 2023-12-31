from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import requests
# Create your views here.
@api_view(['GET','POST'])
def account_list(request):
    if request.method == 'GET':
        account = Account.objects.all()
        serializer = AccountSerializer(account,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# payload
# {
# "email" : "tagoor@gmail.com",
# "account_name" : "ajay"
# }

@api_view(['GET','PUT','DELETE'])
def account_details(requst,account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if requst.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
    elif requst.method == 'PUT':
        serializer = AccountSerializer(account,data=requst.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif requst.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET','POST'])
def destination_list(request):
    if request.method == 'GET':
        destination = Destination.objects.all()
        serializer = DestinationSerializer(destination,many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# {
# "account" : 2,
# "url" : "https://www.tridotstech.com/career#career-job-application",
# "http_method" : "GET",
# "headers": {
# "APP_ID": "1234APPID1234",
# "APP_SECTET": "enwdj3bshwer43bjhjs9ereuinkjcnsiurew8s",
# "ACTION": "user.update",
# "Content-Type": "application/json",
# "Accept": "*"
# }
# }


@api_view(['GET','PUT','DELETE'])
def destination_details(request,id):
    try:
        destination = Destination.objects.get(id=id)
    except Destination.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DestinationSerializer(destination)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = DestinationSerializer(destination,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        destination.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def account_destinations(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    destinations = Destination.objects.filter(account=account)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def incoming_data(request):
    if request.method == 'POST':
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return Response({'error':'Unauthenticated'},status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        if not isinstance(data,dict):
            return Response({'error':"Inavalid Data"},status=status.HTTP_400_BAD_REQUEST)
        
        account = get_object_or_404(Account,app_secret_token=app_secret_token)
        destinations = Destination.objects.filter(account=account)

        for destination in destinations:
            url = destination.url
            http_method = destination.http_method
            headers = destination.headers

            if http_method == 'GET':
                params = {'data':data}
                response = request.get(url,params=params,headers = headers)
            else:
                response = requests.request(http_method,url,json=data,headers=headers)

            return response(status=status.HTTP_200_OK)
        
