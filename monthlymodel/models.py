from django.db import models
from django.db import models


class MonthlyDataModel(models.Model):

    id = models.AutoField(primary_key = True)
    Stock_Symbol = models.TextField()
    LTP = models.FloatField(blank=True, null=True)
    LPT_Date = models.DateField(auto_now_add=True, blank=True)
    Sell_Initiate = models.FloatField()
    Sell_Target = models.FloatField()
    Buy_Initiate = models.FloatField()
    Buy_Target = models.FloatField()
    Market_Type = models.TextField(default='USA')
    
class StrategyModel(models.Model):

    id = models.AutoField(primary_key = True)
    Strategy_Name = models.TextField()
    Strategy_Owner = models.TextField()
    Date_Created = models.DateField(auto_now_add=True, blank=True, null=True)
    Strategy_Type = models.TextField(null=True)
    Mini_Capital = models.TextField()
    Expected_Returns = models.TextField()
    Fees = models.TextField()
    Cap_Lock_Period = models.TextField()
    
    
class BrokerModel(models.Model):

    id = models.AutoField(primary_key = True)
    Broker_name = models.TextField()
    Cust_Id = models.TextField()
    API_Key = models.TextField(null=True)
    API_Secret = models.TextField(null=True)
    Username = models.TextField(null=True)
    Password = models.TextField(null=True)
    Market_Types = models.TextField(null=True)
    
class DataStrategyMappingModel(models.Model):

    id = models.AutoField(primary_key = True)
    Month_Data_Model_id = models.TextField()
    Strategy_id = models.TextField()
    
class AlertDataModel(models.Model):

    id = models.AutoField(primary_key = True)
    Stock_Symbol = models.TextField()
    LPT_Date = models.DateField(auto_now_add=True, blank=True)
    Buy_Initiate = models.FloatField()
    Buy_Target = models.FloatField()
    Buy_Initiate_Flag = models.BooleanField(default=True)
    Buy_Target_Flag = models.BooleanField(default=False)

class PositionalDataModel(models.Model):

    id = models.AutoField(primary_key = True)
    Image = models.TextField()
    Market_Type = models.TextField()
    Header = models.TextField()
    Description = models.TextField()
    
class BlogPostDataModel(models.Model):

    id = models.AutoField(primary_key = True)
    Title = models.TextField()
    Body = models.TextField()
    URL_Slug = models.TextField()
    Date_Added = models.DateField(auto_now_add=True, blank=True)

class UserStrategySubscribeModel(models.Model):
    
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey("api_user.User", on_delete=models.CASCADE)
    Strategy_ID = models.ForeignKey("monthlymodel.StrategyModel",on_delete=models.CASCADE)
    Date_Added = models.DateField(auto_now_add=True, blank=True)
    