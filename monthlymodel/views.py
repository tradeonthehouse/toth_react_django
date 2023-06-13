from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.storage import FileSystemStorage
from .serializers import MonthlyDataModelSerializer
from .serializers import BrokerModelSerializer
from .serializers import DataStrategyMappingModelSerializer
from .serializers import StrategyModelSerializer
from .models import StrategyModel as SM
import pandas as pd
import json

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
