from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('place_order/', views.place_order, name='PlaceOrder'),
    path('get_strikes/', views.get_current_strike_list, name='GetStrikes'),
    path('add_quantity/', views.add_quantity, name='AddQuantity'),
    path('all_positions/', views.get_all_positions, name='AllPositions'),
    path('exit_quantity/', views.exit_quantity, name='exitQuantity'),
    path('complete/', views.complete_the_day, name='complete'),
    path('get_all_ltp/', views.get_all_ltp, name='getAllLtp'),
    path('loading/', views.progress, name='loading'),
]


