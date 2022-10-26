from django.contrib import admin
from django.contrib.auth.models import Group
from OptionApp.models import *
# Register your models here.

class SymbolAndTokenAdmin(admin.ModelAdmin):
    list_display = ('name','strike','symbol','token',)

admin.site.register(SymbolAndToken, SymbolAndTokenAdmin)

class ExpiryDateAdmin(admin.ModelAdmin):
    list_display = ('expiry_date',)

admin.site.register(ExpiryDate, ExpiryDateAdmin)

class TradeBookAdmin(admin.ModelAdmin):
    list_display = ('name','symbol','order_type','quantity','buy_price','sell_price','p_n_l',)

admin.site.register(TradeBook, TradeBookAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name','symbol','order_type','quantity','buy_price','sell_price','status','p_n_l',)

admin.site.register(Position, PositionAdmin)


class DaywiseSummeryAdmin(admin.ModelAdmin):
    list_display = ('date','buy_p_n_l','sell_p_n_l',)

admin.site.register(DaywiseSummery, DaywiseSummeryAdmin)


class StoplossManagerAdmin(admin.ModelAdmin):
    list_display = ('token','order_type','current_stoploss','target_done',)

admin.site.register(StoplossManager, StoplossManagerAdmin)