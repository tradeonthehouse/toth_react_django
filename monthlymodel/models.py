from django.db import models


class MonthlyDataModel(models.Model):

    id = models.AutoField(primary_key = True)
    Stock_Symbol = models.TextField()
    LTP = models.FloatField()
    LPT_Date = models.DateField(auto_now_add=True, blank=True)
    Sell_Initiate = models.FloatField()
    Sell_Target = models.FloatField()
    Buy_Initiate = models.FloatField()
    Buy_Target = models.FloatField()
    
    # class meta:
    #     db_table = "monthlydatamodel"
    #     ordering = ["Stock_Symbol", "LTP", "LPT_Date", "Sell_Initiate", "Sell_Target", "Buy_Initiate", "Buy_Target"]
    
