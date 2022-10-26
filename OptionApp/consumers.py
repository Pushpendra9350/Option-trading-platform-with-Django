from turtle import pos
from typing import final
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json, random
from time import sleep
from OptionApp.models import *
from .utils_angelone import *
import numpy as np
import random
import time, sys
from django_redis import get_redis_connection
from django.core.cache import cache
redis_connection = get_redis_connection("default")

@sync_to_async
def get_data(counter):
    final_list = []
    # nifty_ltp,nifty_close_price = get_ltp_data_with_close_price(obj,'NSE','NIFTY','26000')
    # banknifty_ltp,banknifty_close_price  = get_ltp_data_with_close_price(obj,'NSE','BANKNIFTY','26009')
    # nifty_ltp,nifty_close_price,banknifty_ltp,banknifty_close_price = float(nifty_ltp),float(nifty_close_price),float(banknifty_ltp),float(banknifty_close_price)
    # percent_nifty_change = str(round(((nifty_ltp - nifty_close_price)/nifty_close_price)*100,2))
    # percent_banknifty_change = str(round(((banknifty_ltp - banknifty_close_price)/banknifty_close_price)*100,2))
    final_list.append(
        {
            'tk':'26000',
            'change':"+"+str(round(1+random.random(),2))+"%",
            'ltp':str(random.randint(15000,16500)),
        })
    final_list.append(
        {
            'tk':'26009',
            'change':"+"+str(round(1+random.random(),2))+"%",
            'ltp':str(random.randint(33500,35500)),
        }
    )
    token_list = redis_connection.hget("positions", "tokens").decode().split(" ")
    for token in token_list:
        price = redis_connection.lindex(token, counter)
        if price:
            price = price.decode()
        final_list.append(
            {
                'tk':str(token),
                'ltp':str(price),
            }
        )
    data = {'data': final_list, 'status': 'success'}
    return data

@sync_to_async
def get_data_new():
    for i in range(5):
        final_list = []
        final_list.append(
            {
                'tk':'26000',
                'change':"+"+str(round(1+random.random(),2))+"%",
                'ltp':str(random.randint(15000,16500)),
            })
        final_list.append(
            {
                'tk':'26009',
                'change':"+"+str(round(1+random.random(),2))+"%",
                'ltp':str(random.randint(33500,35500)),
            }
        )
        data = {'data': final_list, 'status': 'success'}
        return data

@sync_to_async
def get_prices(positions):
    mu = [0.001, 0.002, -0.001, -0.002 -0.00019, 0.0001, 0.00015, 0.00019, -0.0001, -0.00015]
    sigma = 0.01
    for position in positions:
        np.random.seed(0)
        mu_value = random.choice(mu)
        token = position.token
        if position.order_type == 'BUY -> SELL':
            price = float(position.buy_price)
        else:
            price = float(position.sell_price)
        returns = np.random.normal(loc=mu_value, scale=sigma, size=1000)
        price = price*(1+returns).cumprod()
        price = price.tolist()
        price = list(map(lambda a: round(a, 2), price))
        for i in price:
            redis_connection.rpush(token, i)
    return True

@sync_to_async
def make_cache_init(positions):
    if positions:
        final_positions_cache = {}
        tokens = ""
        for position in positions:
            tokens += position.token+" "
        final_positions_cache['tokens'] = tokens.strip()
        redis_connection.hmset("positions", final_positions_cache)

@sync_to_async
def check_empty_positions(positions):
    if positions.count() == 0:
        return False
    else:
        return positions

class AsyncAOCosumer(AsyncWebsocketConsumer):
    # Room: room is work like a open connection between two users to communicate seamlessly.
    # Group: group is a group of users that can communicate with each other(Used for broadcasting to multiple users).
    # Group: And jab hme view, model, and function ke ander se iss channel ko call karwana ho to group name use karte hain
    # In each connection we have give a room name and group name.

    # Call when anyone send request to this consumer/socket and send back to frontend.
    async def connect(self):
        await self.accept()
        try:
            positions = Position.objects.all()
            await make_cache_init(positions)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(e,' at line ',exc_tb.tb_lineno)
            positions = False
        if await check_empty_positions(positions):
            await get_prices(positions)
            for i in range(100):
                data = await get_data(i)
                await self.send(text_data=json.dumps(data))
                sleep(1)
        else:
            for i in range(100):
                data = await get_data_new()
                await self.send(text_data=json.dumps(data))
                sleep(1)

    # Call when any one disconnect from this consumer/socket
    async def disconnect(self,*args, **kwargs):
        print("Disconnected")
        raise StopConsumer()
    # Call when any one send message to this consumer/socket from frontend.
    async def receive(self, text_data):
        print(text_data)
        pass















# This is a Synchronous websocket consumer
"""
class AOCosumerIndex(WebsocketConsumer):
    # Room: room is work like a open connection between two users to communicate seamlessly.
    # Group: group is a group of users that can communicate with each other(Used for broadcasting to multiple users).
    # Group: And jab hme view, model, and function ke ander se iss channel ko call karwana ho to group name use karte hain
    # In each connection we have give a room name and group name.


    # Call when anyone send request to this consumer/socket at the time of handshaking.
    def connect(self):
        self.room_name = 'AO_room'
        self.room_group_name = 'AO_room_group'
        # Because of the differences between Channels and Django, we'll have to frequently switch between sync and async code execution
        # For example, the Django database needs to be accessed using synchronous code while the Channels channel layer needs to be accessed using asynchronous code.
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.room_group_name
            )
        # This will accept the connection from client(If we remove this then connection will disconnect)
        self.accept()
        #obj = get_api_object()
        try:
            positions = async_to_sync(Position.objects.all())
        except:
            positions = False
        if positions:
            for i in range(5):
                final_list = []
                # nifty_ltp,nifty_close_price = get_ltp_data_with_close_price(obj,'NSE','NIFTY','26000')
                # banknifty_ltp,banknifty_close_price  = get_ltp_data_with_close_price(obj,'NSE','BANKNIFTY','26009')
                # nifty_ltp,nifty_close_price,banknifty_ltp,banknifty_close_price = float(nifty_ltp),float(nifty_close_price),float(banknifty_ltp),float(banknifty_close_price)
                # percent_nifty_change = str(round(((nifty_ltp - nifty_close_price)/nifty_close_price)*100,2))
                # percent_banknifty_change = str(round(((banknifty_ltp - banknifty_close_price)/banknifty_close_price)*100,2))
                final_list.append(
                    {
                        'tk':'26000',
                        'change':'2.6',
                        'ltp':str(random.randint(15000,16500)),
                    })
                final_list.append(
                    {
                        'tk':'26009',
                        'change':'2.3',
                        'ltp':str(random.randint(33500,35500)),
                    }
                )
                for position in positions:
                    token = position.token
                    #ltp = get_ltp_data(obj,'NFO',position.symbol,token)
                    final_list.append(
                        {
                            'tk':token,
                            'ltp':str(random.randint(400,600)),
                        }
                    )
                data = {'data': final_list, 'status': 'success'}
                print(data)
                self.send(text_data=json.dumps(data))
                sleep(1)
        else:
            data = {'data': 'No positions', 'status': 'failure'}
            self.send(text_data=json.dumps(data))
            sleep(1)

    # Call when any one disconnect from this consumer/socket
    def disconnect(self,*args, **kwargs):
        print("Disconnected")
    
    # Call when any one send message to this consumer/socket from frontend.
    def receive(self, text_data):
        print(text_data)
        pass
"""