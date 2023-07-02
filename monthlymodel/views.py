import mimetypes
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.storage import FileSystemStorage
from .serializers import MonthlyDataModelSerializer
from .serializers import BrokerModelSerializer
from .serializers import DataStrategyMappingModelSerializer
from .serializers import StrategyModelSerializer,PositionalDataModelSerializer
from .models import StrategyModel as SM,PositionalDataModel as PM
from api.user.serializers import UserSerializer
from django.http import FileResponse, HttpResponse
from rest_framework import generics
from wsgiref.util import FileWrapper

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import random
import string

import pandas as pd
import json

cred = credentials.Certificate("toth-47f23-firebase-adminsdk-y8iji-4a0f8e77a6.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'toth-47f23.appspot.com'
})

class UploadFileViewSet(viewsets.ModelViewSet):
    http_method_names = ["post"]
    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)
    serializer_class = MonthlyDataModelSerializer

    def create(self, request, *args, **kwargs):
        print("upload strategy function running......")
        form_Data = request.POST
        market = form_Data.get('market').upper()
        print(market)
        myfile = request.FILES['excel']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        print(filename)
        
        empexceldata = pd.read_excel(filename, usecols='B,C,E,F,H,I') 
        df = empexceldata.rename(columns={"STOCK SYMBOL":"Stock_Symbol","BUY INITIATE":"Buy_Initiate","SELL INITIATE":"Sell_Initiate","TARGET.1":"Sell_Target","TARGET":"Buy_Target"})     

        json_excel_data = df.to_dict('records')
        # json_excel_data_readable = json.dumps(json_excel_data,indent=4)

        for each in json_excel_data:
            
            each['Market_Type'] = market;
            t = json.dumps(each)
            print(t)
            serializer = self.get_serializer(data=each)
            serializer.is_valid(raise_exception=True)
            # serializer2.is_valid(raise_exception=True)
            filemodel = serializer.save()     
            # serializer2 = DataStrategyMappingModelSerializer.get_serializer(data=each)
            
        return Response(
            {
                "success": True,
                "filemodel" : filemodel.id,
                "msg": "File uploaded..",
            },
            status=status.HTTP_201_CREATED,
        )


class BrokerModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["post"]
    permission_classes = (IsAuthenticated,)
    serializer_class = BrokerModelSerializer

    def create(self, request, *args, **kwargs):
        
        data = json.loads(request.body)
        
        broker_data_from_req = {
            "Broker_name" : data.get('Broker_name'),
            "Cust_Id" : data.get('Cust_Id'),
            "API_Key" : data.get('API_Key'),
            "API_Secret" : data.get('API_Secret'),
            "Username" : data.get('Username'),
            "Password" : data.get('Password'),
            "Market_Types" : data.get('Market_Types')
        }
        
        serializer = self.get_serializer(data=broker_data_from_req)
        serializer.is_valid(raise_exception=True)
        commit_response = serializer.save()
        
        return Response(
            {
                "success": True,
                "filemodel" : commit_response.id,
                "msg": "Broker Added To Your Account!",
            },
            status=status.HTTP_201_CREATED,
        )
        
        
class StrategyModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    permission_classes = (AllowAny,)
    serializer_class = StrategyModelSerializer

    def list(self, request, *args, **kwargs):

        queryset = SM.objects.all()
        print(queryset)
        serializer  = StrategyModelSerializer(queryset, many=True)
        print(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
class PositionalDataModelSet(viewsets.ModelViewSet):
    http_method_names = ["get","post"]
    permission_classes = (IsAuthenticated,)
    serializer_class = PositionalDataModelSerializer

    def list(self, request, *args, **kwargs):

        data = request.GET
        market = data.get('Market_Type')
        print(market)
        queryset = PM.objects.filter(Market_Type=market)
        # print(queryset)
        serializer  = PositionalDataModelSerializer(queryset, many=True)
        print(serializer)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
    def create(self, request, *args, **kwargs):
        
        # data = json.loads(request.body)
        data = request.POST
        
        imageFile = request.FILES['Image']
        # fs = FileSystemStorage(location='static/images/')
        # filename = fs.save(imageFile.name, imageFile)
        
        # print(imageFile)
        
        def generate_random_string(length):
            letters = string.ascii_letters + string.digits
            return ''.join(random.choice(letters) for _ in range(length))
        
        def upload_image(file_path, destination_path):
             # Initialize Firebase app
            bucket = storage.bucket()
            blob = bucket.blob(destination_path)
            # blob.upload_from_string(
            #     image_data,
            #     content_type='image/jpeg'
            # )
            blob.upload_from_file(file_path,content_type=imageFile.content_type)
           
            print("File uploaded successfully.")
            return blob.public_url
            
        image_name = generate_random_string(20)
        try:
            if "image" in str(imageFile.content_type):
                url = upload_image(imageFile,"positional-trade-images/"+image_name+"."+str(imageFile.content_type).replace('image/',''))
                print(url)
            else: 
                return Response(
                {
                    "success": False,
                    "msg": "Only Image files are allowed!",
                },
                status=status.HTTP_201_CREATED,)
        except Exception as e:
            print(e)
            return Response(
            {
                "success": False,
                "msg": "Positional Data Failed to Upload!",
            },
            status=status.HTTP_201_CREATED,)
            
        broker_data_from_req = {
            "Image" : url,
            "Market_Type" : data.get('Market_Type'),
            "Header" : data.get('Header'),
            "Description" : data.get('Description')
        }
        
        # print(broker_data_from_req)
        
        serializer = self.get_serializer(data=broker_data_from_req)
        serializer.is_valid(raise_exception=True)
        commit_response = serializer.save()
        
        return Response(
            {
                "success": True,
                # "filemodel" : commit_response.id,
                "filemodel" : commit_response.id,
                "msg": "Positional Data added Succesfully!",
            },
            status=status.HTTP_201_CREATED,
        )
        
class AuthMeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        
        serializer = UserSerializer(request.user)
        print(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
class PositionalImageDownload(generics.ListAPIView):
    http_method_names = ["get"]
    permission_classes = (AllowAny,)
    
    def get(self, request, id, format=None):
        queryset = PM.objects.get(id=id)
        file_handle = queryset.Image
        print(queryset.Image.name)
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.Image.name
        return response
        

