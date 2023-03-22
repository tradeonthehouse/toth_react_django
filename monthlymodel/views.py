from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.files.storage import FileSystemStorage
from .serializers import MonthlyDataModelSerializer
import pandas as pd
import json

class UploadFileViewSet(viewsets.ModelViewSet):
    http_method_names = ["post"]
    permission_classes = (AllowAny,)
    serializer_class = MonthlyDataModelSerializer

    def create(self, request, *args, **kwargs):

        # excel_file = request.FILES.get("excel")
        # print(excel_file.file)
        # print(type(excel_file))

        myfile = request.FILES['excel']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)  
        print(filename)
        
        empexceldata = pd.read_excel(filename, skiprows=lambda x: x%2 == 0, usecols='B,C,E,F,H,I') 
        df = empexceldata.rename(columns={"LTP as on Dec 01":"LTP","STOCK SYMBOL":"Stock_Symbol","BUY INITIATE":"Buy_Initiate","SELL INITIATE":"Sell_Initiate","TARGET.1":"Sell_Target","TARGET":"Buy_Target"})     
        # print(empexceldata.to_dict('records'))
        json_excel_data = df.to_dict('records')
        json_excel_data_readable = json.dumps(json_excel_data,indent=4)
        #print(json_excel_data_readable)
        
        

        # read the data from the Excel file
        # df = pd.read_excel()

        # print(df)
        new_Data =   {
            "Stock_Symbol": "NMDC",
            "LTP_Date" : "2023-03-20",
            "Sell_Initiate": 98.7,
            "Sell_Target": 97.713,
            "Buy_Initiate": 119.9,
            "Buy_Target": 121.099,
            "LTP": 117.85
        }
        # serializer = self.get_serializer(data=new_Data)
        # serializer.is_valid(raise_exception=True)
        # filemodel = serializer.save()
        
        # print(type(new_Data))
        # print(type(json_excel_data))
        # print(type(df.to_dict('records')[0]))
        # serializer = self.get_serializer(data=json.dumps(df.to_dict('records'),indent=4))
        for each in json_excel_data:
            #each["LTP_Date"] = "2023-03-20"
            t = json.dumps(each)
            print(t)
            serializer = self.get_serializer(data=each)
            serializer.is_valid(raise_exception=True)
            filemodel = serializer.save()

        return Response(
            {
                "success": True,
                "filemodel" : filemodel.id,
                "msg": "File uploaded..",
            },
            status=status.HTTP_201_CREATED,
        )

