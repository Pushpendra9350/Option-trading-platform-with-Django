from django.db import models
from datetime import datetime
from django.utils import timezone
# {"token":"8357","symbol":"725TN32-SG","name":"725TN32","expiry":"","strike":"-1.000000","lotsize":"100","instrumenttype":"","exch_seg":"NSE","tick_size":"1.000000"}
# Create your models here.

class SymbolAndToken(models.Model):
    token = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    expiry = models.CharField(max_length=100)
    strike = models.CharField(max_length=100)
    lotsize = models.CharField(max_length=100)
    instrumenttype = models.CharField(max_length=100)
    exch_seg = models.CharField(max_length=100)
    tick_size = models.CharField(max_length=100)

    def __str__(self):
        return str(self.symbol)


class ExpiryDate(models.Model):
    expiry_date = models.CharField(max_length=100, default='')
    input_value = models.CharField(max_length=100, default='')
    front_value = models.CharField(max_length=100, default='')
    date = models.DateField(default=timezone.now(), blank=True, null=True)
    def __str__(self):
        return str(self.expiry_date)


class TradeBook(models.Model):
    name = models.CharField(max_length=100,default='')
    symbol = models.CharField(max_length=100,default='')
    token = models.CharField(max_length=100,default='')
    order_type = models.CharField(max_length=100,default='')
    quantity = models.CharField(max_length=100,default='')
    half_quantity = models.CharField(max_length=100,default='')
    fill_exit_quantity = models.CharField(max_length=100,default='')
    buy_price = models.CharField(max_length=100,default='')
    half_exit_price = models.CharField(max_length=100,default='')
    sell_price = models.CharField(max_length=100,default='')
    stoploss = models.CharField(max_length=100,default='')
    target = models.CharField(max_length=100,default='')
    start_time = models.DateTimeField(default=timezone.now())
    half_exit_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now())
    strategy = models.CharField(max_length=100,default='')
    p_n_l  = models.CharField(max_length=100,default='')

    def __str__(self):
        return str(self.symbol)
    


class Position(models.Model):
    name = models.CharField(max_length=100, default='')
    symbol = models.CharField(max_length=100, default='')
    token = models.CharField(max_length=100,default='')
    order_type = models.CharField(max_length=100, default='')
    quantity = models.CharField(max_length=100, default='')
    half_quantity = models.CharField(max_length=100,default='')
    fill_exit_quantity = models.CharField(max_length=100,default='')
    buy_price = models.CharField(max_length=100, default='')
    half_exit_price = models.CharField(max_length=100,default='')
    sell_price = models.CharField(max_length=100,default='')
    stoploss = models.CharField(max_length=100, default='')
    target = models.CharField(max_length=100,default='')
    start_time = models.DateTimeField(default=timezone.now())
    half_exit_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now())
    strategy = models.CharField(max_length=100,default='')
    status  = models.CharField(max_length=100, default='')
    p_n_l  = models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.symbol)

class DaywiseSummery(models.Model):
    date = models.DateTimeField(default=timezone.now())
    total_buy_trades = models.CharField(max_length=100,default='')
    total_sell_trades = models.CharField(max_length=100,default='')
    total_buy_quantity = models.CharField(max_length=100,default='')
    total_sell_quantity = models.CharField(max_length=100,default='')
    win_buy_rate = models.CharField(max_length=100,default='')
    win_sell_rate = models.CharField(max_length=100,default='')
    buy_percentage = models.CharField(max_length=100,default='')
    sell_percentage = models.CharField(max_length=100,default='')
    buy_p_n_l  = models.CharField(max_length=100,default='')
    sell_p_n_l  = models.CharField(max_length=100,default='')

    def __str__(self):
        return str(self.date)


class StoplossManager(models.Model):
    token = models.CharField(max_length=100,default='')
    order_type = models.CharField(max_length=100, default='')
    current_stoploss = models.CharField(max_length=100, default='')
    target = models.CharField(max_length=100,default='')
    target_done = models.BooleanField(default=False)
    trail_list = models.TextField(default='')
    trail_dict = models.TextField(default='')
    
    def __str__(self):
        return str(self.token)

        
    
