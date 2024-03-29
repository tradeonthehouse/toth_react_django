import mimetypes
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.storage import FileSystemStorage
import typing
from .serializers import MonthlyDataModelSerializer, UserStrategySubscribeSerializer
from .serializers import BrokerModelSerializer
from .serializers import DataStrategyMappingModelSerializer
from .serializers import StrategyModelSerializer,PositionalDataModelSerializer, BlogPostDataModelSerializer
from .models import BlogPostDataModel as BM, PositionalDataModel as PM, StrategyModel as SM,UserStrategySubscribeModel as USSM, MonthlyDataModel as MM
from api.user.serializers import UserSerializer
from django.http import FileResponse, HttpResponse
from rest_framework import generics
from wsgiref.util import FileWrapper

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import random
import string
from datetime import datetime as dt, timedelta, time
import pandas as pd
import json

cred = credentials.Certificate("toth-47f23-firebase-adminsdk-y8iji-4a0f8e77a6.json")
firebase_admin.initialize_app(cred,{"databaseURL": "https://toth-47f23-default-rtdb.asia-southeast1.firebasedatabase.app/"})


Day = dt.now().day
Month = dt.now().strftime('%b')
Year = dt.now().year

class UploadFileViewSet(viewsets.ModelViewSet):
    http_method_names = ["post","get"]
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
        
                
        buy_fb_path = market+"-Buy-"+str(Month)+"-"+str(Year)
        sell_fb_path = market+"-Sell-"+str(Month)+"-"+str(Year)
        
        alerts_list_buy = db.reference(buy_fb_path).get()
        if alerts_list_buy is None:
            alerts_list_buy = []
        alerts_list_sell = db.reference(sell_fb_path).get()
        if alerts_list_sell is None:
            alerts_list_sell = []

        for each in json_excel_data:
            
            each['Market_Type'] = market
            t = json.dumps(each)
            print(t)
            
            if any(each_dict['Stock_Symbol'].strip() == each['Stock_Symbol'].strip() for each_dict in alerts_list_buy):
                print(each['Stock_Symbol'].strip(),' This already exists')
            else:
                alert_data = {'Stock_Symbol' : each['Stock_Symbol'].strip(), 'Buy_Initiate' : round(each['Buy_Initiate'],2) ,\
                    'Buy_Target' : round(each['Buy_Target'],2), 'Buy_Initiate_Flag' : False, \
                    'Buy_Target_Flag' : False, 'Buy_Initiate_Timestamp' : '','Buy_Target_Timestamp': ''}
                alerts_list_buy.append(alert_data)
                
            if any(each_dict['Stock_Symbol'].strip() == each['Stock_Symbol'].strip() for each_dict in alerts_list_sell):
                print(each['Stock_Symbol'].strip(),' This already exists')
            else:
                alert_data = {'Stock_Symbol' : each['Stock_Symbol'].strip(), 'Sell_Initiate' : round(each['Sell_Initiate'],2) ,\
                    'Sell_Target' : round(each['Sell_Target'],2), 'Sell_Initiate_Flag' : False, \
                    'Sell_Target_Flag' : False, 'Sell_Initiate_Timestamp' : '','Sell_Target_Timestamp':''}
                alerts_list_sell.append(alert_data)
            
            serializer = self.get_serializer(data=each)
            serializer.is_valid(raise_exception=True)
            # serializer2.is_valid(raise_exception=True)
            filemodel = serializer.save()     
            # serializer2 = DataStrategyMappingModelSerializer.get_serializer(data=each)
            

            
        db.reference(buy_fb_path).set(alerts_list_buy)
        db.reference(sell_fb_path).set(alerts_list_sell)
            
        return Response(
            {
                "success": True,
                "filemodel" : filemodel.id,
                "msg": "File uploaded..",
            },
            status=status.HTTP_201_CREATED,
        )
        
    def list(self, request, *args, **kwargs):
        data = request.GET
        month = data.get('Month')
        call_type = data.get('Type')
        market_type = data.get('Market_Type')
        #print(month, market_type)
        
        queryset = MM.objects.filter(Market_Type=market_type)

        serializer  = MonthlyDataModelSerializer(queryset, many=True)
        if call_type.lower() == 'buy':
            for each in serializer.data:
                each.pop('id',None)
                each.pop('LTP',None)
                each.pop('LPT_Date',None)
                each.pop('Sell_Initiate',None)
                each.pop('Sell_Target',None)
                each.pop('Market_Type',None)
                each['Buy_Initiate_Flag'] = False
                each['Buy_Initiate_Timestamp'] = None
                each['Buy_Target_Flag'] = False
                each['Buy_Target_Timestamp'] = None
        else:
            for each in serializer.data:
                each.pop('id',None)
                each.pop('LTP',None)
                each.pop('LPT_Date',None)
                each.pop('Buy_Initiate',None)
                each.pop('Buy_Target',None)
                each.pop('Market_Type',None)
                each['Sell_Initiate_Timestamp'] = None
                each['Sell_Target_Flag'] = False
                each['Sell_Target_Timestamp'] = None
                each['Sell_Initiate_Flag'] = False
            
        #print(serializer.data)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
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
            bucket = storage.bucket('toth-47f23.appspot.com')
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
                status=status.HTTP_400_BAD_REQUEST,)
        except Exception as e:
            print(e)
            return Response(
            {
                "success": False,
                "msg": "Positional Data Failed to Upload!",
            },
            status=status.HTTP_400_BAD_REQUEST,)
            
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
        

class StockSymbolImagesDownload(generics.ListAPIView):
    
    http_method_names = ["get"]
    permission_classes = (AllowAny,)
    
    def get(self, request, stocksymbol, format=None):
        bucket = storage.bucket('toth-47f23.appspot.com')
        blobs = list(bucket.list_blobs(prefix='Company_Stock_Symbol/'+stocksymbol.upper()+'/'))
        # print(blobs)
        url = []
        for each in blobs:
            print(each.public_url)
            sub_strings = ['.D-','_BIG']
            if all(sub not in each.name for sub in sub_strings):
            #     # print(each.public_url)
                url.append(each.public_url)
                
        
        # ref = db.reference('/Company_Stock_Symbol/'+stocksymbol)
        # data = ref.get()
        # print(data)
        # url = []
        # images = data['images']
        # for each  in images:
        #     sub_strings = ['.D-','_BIG']
        #     if all(sub not in each for sub in sub_strings):
        #         url.append(each.split('?')[0])
                
        print(url)
        msg =  None
        for each in url:
            if '.png' in each:
                msg = each
                break
            elif '.svg' in each:
                msg = each
        if msg is None:                
            return Response(
            'Image Not Found',
            status=status.HTTP_404_NOT_FOUND,
        )
        return Response(
            msg,
            status=status.HTTP_200_OK,
        )
        
class PerformanceDataViewSet(generics.ListAPIView):
    http_method_names = ["get"]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        data = request.GET
        Month = data.get('month')
        Year = data.get('year')

        Month = dt.now().strftime('%b') if Month is None else Month
        Year = dt.now().year if Year is None else Year
        
        Paths = ["USA-Buy-" + str(Month)+"-"+str(Year),
            "USA-Sell-" + str(Month)+"-"+str(Year),
            "INDIA-Sell-" + str(Month)+"-"+str(Year),
            "INDIA-Buy-" + str(Month)+"-"+str(Year)]
        
        total_calls = 0
        exited_calls = 0
        time_list = []
        
        def get_delta_time(string1,string2):
            date_format = "%Y-%m-%d %H:%M:%S"
            # Convert the strings into datetime objects
            datetime1 = dt.strptime(string1, date_format)
            datetime2 = dt.strptime(string2, date_format)

            # Calculate the difference
            time_difference = datetime2 - datetime1

            time_list.append(time_difference)
            return time_difference
        
        for each in Paths:
            ref = db.reference(each)
            node_data = ref.get()
            
            if node_data is not None:
                for one in node_data:
                    #print(one)
                    if "Buy" in each:
                        if (one['Buy_Target_Flag'] is True):
                            exited_calls = exited_calls + 1
                            get_delta_time(one['Buy_Initiate_Timestamp'].split('.')[0], one['Buy_Target_Timestamp'].split('.')[0])
                    else:
                        if (one['Sell_Target_Flag'] is True):
                            exited_calls = exited_calls + 1
                            get_delta_time(one['Sell_Initiate_Timestamp'].split('.')[0], one['Sell_Target_Timestamp'].split('.')[0])
                            
                    if one.get('Sell_Initiate_Flag') is True or one.get('Buy_Initiate_Flag') is True:
                        total_calls = total_calls + 1
            

        # Calculate the sum of the time deltas
        total_time = sum(time_list, timedelta())

        # Calculate the average
        avg_time = total_time / len(time_list)
            
        return_data = {'Total_Signals': total_calls, 'Target_Hit': exited_calls, 'Avg_Duration': str(avg_time).split('.')[0]}
        
        return Response(
            return_data,
            status=status.HTTP_200_OK,
        )
        
        
class BlogPostModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get","post"]
    permission_classes = (AllowAny,)
    serializer_class = BlogPostDataModelSerializer

    def list(self, request, Title, *args, **kwargs):
        
        queryset = BM.objects.get(URL_Slug__iexact=Title.lower())
        #print(queryset)
        serializer  = BlogPostDataModelSerializer(queryset)
        #print(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
    def list_all(self, request, *args, **kwargs):
        
        queryset = BM.objects.all()
        #print(queryset)
        serializer  = BlogPostDataModelSerializer(queryset, many=True)
        #print(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
        
    def create(self, request, *args, **kwargs):
        
        # data = json.loads(request.body)
        data = request.POST
        
        post_data = {
            'Title' : data['title'],
            'Body' : data['contents'],
            'URL_Slug' : data['title'].lower().replace(' ','-')
        }
        
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        commit_response = serializer.save()
        
        return Response(
            {
                "success": True,
                # "filemodel" : commit_response.id,
                "filemodel" : commit_response.id,
                "msg": "BlogPost Data added Succesfully!",
            },
            status=status.HTTP_201_CREATED,
        )
        
class UserStrategySubscribeViewSet(viewsets.ModelViewSet):
    http_method_names = ["post","get","delete"]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserStrategySubscribeSerializer

    def create(self, request, *args, **kwargs):
        
        # data = json.loads(request.body)
        data = request.POST
        
        print(data)
        
        post_data = {
            'Strategy_ID' : data['Strategy_ID'],
            'user' : request.user.id
        }
        
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        commit_response = serializer.save()
        
        return Response(
            {
                "success": True,
                # "filemodel" : commit_response.id,
                "filemodel" : commit_response.id,
                "msg": "Strategy Subscribed Succesfully!",
            },
            status=status.HTTP_201_CREATED,
        )
    
    def list(self, request, *args, **kwargs):

        # data = request.GET
        user = None
        if request.user:
            userserializer = UserSerializer(request.user)
            user =  userserializer.data
            
            queryset = USSM.objects.filter(user=user['id'])
            
            serializer  = UserStrategySubscribeSerializer(queryset, many=True)
            value = []
            for each in json.loads(json.dumps(serializer.data)):
                value.append(each.get('Strategy_ID'))
            return Response(
                value,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                [],
                status=status.HTTP_200_OK,
            )
        
        # market = data.get('Market_Type')
        # print(market)
        
    def delete(self, request, *args, **kwargs):

        userserializer = UserSerializer(request.user)
        user =  userserializer.data
        user_id = user['id']
        
        Strategy_Id = request.data.get('Strategy_ID')
        
        try:
            queryset = USSM.objects.filter(user=user_id).get(Strategy_ID_id=Strategy_Id)
            queryset.delete()
        except:
            return Response(
            {
                "success": False,
                "msg": "Strategy Delete Failed!!",
            },
            status=status.HTTP_200_OK,
        )
            
        return Response(
            {
                "success": True,
                "Deleted_Strategy_ID" : Strategy_Id,
                "msg": "Strategy Deleted Succesfully!",
            },
            status=status.HTTP_200_OK,
        )