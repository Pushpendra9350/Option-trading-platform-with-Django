from unicodedata import name
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import random, json, requests, sys
from .models import *
from datetime import datetime
import pytz
from .utils_angelone import *
from time import sleep
from OptionApp import tasks
from django_redis import get_redis_connection
from django.core.cache import cache
redis_connection = get_redis_connection("default")

tz = pytz.timezone('Asia/Kolkata')
# Create your views here.

def get_date_time():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    dt_string = now.strftime("%y-%m-%d %I:%M:%S")
    dt_string = datetime.strptime(str(dt_string), "%y-%m-%d %I:%M:%S")
    return dt_string


def get_current_strike_list(request):
    try:
        if request.method == 'POST':
            data = request.POST.get('symbol')
            symbol = data
            if symbol == 'NIFTY':
                token = '26000'
            else:
                token = '26009'
            ltp = get_ltp_data('NSE',symbol,token)
            if token == '26000':
                final_strike = int(str(ltp)[:3]+'00')
                strike_list = []
                current_strike = final_strike
                for i in range(10):
                    strike_list.append(current_strike-50)
                    current_strike = current_strike-50
                strike_list = strike_list[::-1]
                strike_list.append(final_strike)
                current_strike = final_strike
                for i in range(10):
                    strike_list.append(current_strike+50)
                    current_strike = current_strike+50
            elif token == '26009':
                final_strike = int(str(ltp)[:3]+'00')
                current_strike = final_strike
                strike_list = []
                for i in range(10):
                    strike_list.append(current_strike-100)
                    current_strike = current_strike-100
                strike_list = strike_list[::-1]
                strike_list.append(final_strike)
                current_strike = final_strike
                for i in range(10):
                    strike_list.append(current_strike+100)
                    current_strike = current_strike+100
            return HttpResponse(json.dumps({'status':'success','strikes':strike_list}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')

def convert(date_time):
    format = '%b %d %Y %I:%M%p'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str.date()

def get_tokens_and_symbols():
    SymbolAndToken.objects.all().delete()
    ExpiryDate.objects.all().delete()
    data = requests.get('https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json')
    data = data.json()
    all_expiry = [] 
    for i in data:
        strike = i['strike']
        if strike == '-1.000000':
            strike = ''
        else:
            strike = strike.split('.')[0]
            strike = strike[:-2]
        if i['name'] in ['NIFTY', 'BANKNIFTY']:
            if i['expiry'][-2:] == '22':
                obj = SymbolAndToken.objects.create(
                    token= i['token'],
                    symbol = i['symbol'],
                    name = i['name'],
                    expiry = i['expiry'],
                    strike = strike,
                    lotsize = i['lotsize'],
                    instrumenttype = i['instrumenttype'],
                    exch_seg = i['exch_seg'],
                    tick_size = i['tick_size'])
                obj.save()
                # Saving a new expiry date if we get
                if i['expiry'] not in all_expiry:
                    all_expiry.append(i['expiry'])
    # Making objects for the expiry dates
    year_map = {"JAN":"01", "FEB":"02", "MAR": "03", "APR":"04", "MAY":"05", "JUN":"06", "JUL":"07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}
    for i in all_expiry:
        if i != '':
            date = str(i)[:2]
            month = str(i)[2:5]
            year = str(i)[-2:]
            input_value = date+month+year
            front_value = date + " " + month
            format_string = month + " " + date + " " + "20"+year + " 10:07AM"
            date_is = convert(format_string)
            obj = ExpiryDate.objects.create(expiry_date = i, input_value = input_value, front_value = front_value, date = date_is)
            obj.save()

def progress(request):
    result = tasks.process_task.delay()
    return render(request, "OptionApp/progress.html", context={'task_id': result.task_id})        

def index(request):
    try:
        file_token_date = open('static/token_date.txt','r').read()
        today_date = str(datetime.now(tz)).split(' ')[0]
        year = today_date.split('-')[0][2:]
        date_list = today_date.split('-')
        date_list[0] = year
        final_date = "-".join(date_list)
        date1 = datetime.strptime(file_token_date, "%y-%m-%d")
        date2 = datetime.strptime(final_date, "%y-%m-%d")
        if date1 != date2:
            token_date = open('static/token_date.txt','w')
            token_date.write(str(final_date))
            token_date.close()
            result = tasks.process_task.delay()
            return render(request, "OptionApp/progress.html", context={'task_id': result.task_id})
        expiry_dates = ExpiryDate.objects.all().order_by('date')[:5]
        first_expiry = expiry_dates[0]
        import json
        # if "newlst" in redis_connection:
        #     print(type(redis_connection.hget("newlst", "php").decode()))
        #     print(json.loads(redis_connection.hget("newlst", "python").decode()))
        #     print(json.loads(redis_connection.hget("newlst", "python").decode())['numpy'])
        # else:
        #     new_data = json.dumps({"numpy":"test"})
        #     frameworks = {'python':new_data,'php':'["zisd","askjdzfx","sjdn"]','java':'Spring'}
        #     redis_connection.hmset("newlst", frameworks)
        # if "newtes" in redis_connection:
        #     print(type(redis_connection.hget("newlst", "php").decode()))
        #     print(json.loads(redis_connection.hget("newlst", "python").decode()))
        #     print(json.loads(redis_connection.hget("newlst", "python").decode())['numpy'])
        # else:
        #     redis_connection.rpush("newtest", 12)
        #     print(redis_connection.lindex("newtest", 0))
        return render(request, 'OptionApp/index.html', {"first_expiry": first_expiry, "expiry_date": expiry_dates[1:]})
    except Exception as e:
        print(e)


def get_avg_price(old_price,new_price,old_quantity,new_quantity):
    one = old_price*old_quantity
    two = new_price*new_quantity
    avg_price = (one+two)/(old_quantity+new_quantity)
    return round(avg_price,2)


def exit_quantity(request):
    try:
        if request.method == 'POST':
            exit_quantity = request.POST.get('quantity')
            token = request.POST.get('token')
            price_now = request.POST.get('price')
            if str(token)[:2] == 'AB':
                token_val = str(token)[2:]
                order_type = 'BUY -> SELL'
                try:
                    pos = Position.objects.get(token=token_val,order_type=order_type)
                except:
                    pos = False
            elif str(token)[:2] == 'AS':
                token_val = str(token)[2:]
                order_type = 'SELL -> BUY'
                try:
                    pos = Position.objects.get(token=token_val,order_type=order_type)
                except:
                    pos = False
            if pos:
                symbol = pos.symbol

                #new_price = get_ltp_data('NFO', symbol, token_val)
                new_price = float(price_now)
                if pos.status == 'Active':
                    if pos.half_quantity == '':
                        if int(exit_quantity) == int(pos.quantity):
                            pos.fill_exit_quantity = str(exit_quantity)
                            if str(token)[:2] == 'AB':
                                pos.status = 'Close'
                                pos.sell_price = str(round(new_price,2))
                                pos.end_time = get_date_time()
                                pos.p_n_l = str(round(((float(new_price)-float(pos.buy_price))*int(exit_quantity)),2))
                                pos.save()
                            elif str(token)[:2] == 'AS':
                                pos.status = 'Close'
                                pos.buy_price = str(round(new_price,2))
                                pos.end_time = get_date_time()
                                pos.p_n_l = str(round(((float(pos.sell_price)-float(new_price))*int(exit_quantity)),2))
                                pos.save()
                        elif int(exit_quantity) < int(pos.quantity):
                            pos.half_quantity = str(exit_quantity)
                            pos.half_exit_price = str(round(new_price,2))
                            pos.half_exit_time = get_date_time()
                            pos.save() 
                        else:
                            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
                    else:
                        half_qty = pos.half_quantity
                        new_half_qty = int(half_qty)+int(exit_quantity)
                        if new_half_qty == int(pos.quantity):
                            pos.fill_exit_quantity = str(new_half_qty)
                            if str(token)[:2] == 'AB':
                                pos.status = 'Close'
                                pos.sell_price = str(round(new_price,2))
                                pos.end_time = get_date_time()
                                half_pnl = round(((float(pos.half_exit_price)-float(pos.buy_price))*int(pos.half_quantity)),2)
                                pos.p_n_l = str(half_pnl + round(((float(new_price)-float(pos.buy_price))*int(pos.quantity)),2))
                                pos.save()
                            elif str(token)[:2] == 'AS':
                                pos.status = 'Close'
                                pos.buy_price = str(round(new_price,2))
                                pos.end_time = get_date_time()
                                half_pnl = round(((float(pos.sell_price)-float(pos.half_exit_price))*int(pos.half_quantity)),2)
                                pos.p_n_l = str(half_pnl + round(((float(pos.sell_price)-float(new_price))*int(pos.quantity)),2))
                                pos.save()
                        elif new_half_qty < int(pos.quantity):
                            pos.half_quantity = str(new_half_qty)
                            pos.half_exit_price = str(round(new_price,2))
                            pos.half_exit_time = get_date_time()
                            pos.save()
                        else:
                            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
                    return HttpResponse(json.dumps({'status':'success'}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Views.py 209", e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')



def add_quantity(request):
    try:
        if request.method == 'POST':
            new_quantity = request.POST.get('quantity')
            token = request.POST.get('token')
            price_now = request.POST.get('price')
            print(price_now)
            if str(token)[:2] == 'AB':
                token_val = str(token)[2:]
                order_type = 'BUY -> SELL'
                try:
                    pos = Position.objects.get(token=token_val,order_type=order_type)
                except:
                    pos = False
            elif str(token)[:2] == 'AS':
                token_val = str(token)[2:]
                order_type = 'SELL -> BUY'
                try:
                    pos = Position.objects.get(token=token_val,order_type=order_type)
                except:
                    pos = False
            if pos:
                symbol = pos.symbol
                #new_price = get_ltp_data('NFO',symbol,token_val)
                new_price = float(price_now)
                if pos.status == 'Active':
                    old_quantity = pos.quantity
                    if str(token)[:2] == 'AB':
                        old_price = pos.buy_price
                        avg_price = get_avg_price(float(old_price),float(new_price),int(old_quantity),int(new_quantity))
                        pos.quantity = str(int(old_quantity)+int(new_quantity))
                        pos.buy_price = str(avg_price)
                    elif str(token)[:2] == 'AS':
                        old_price = pos.sell_price
                        avg_price = get_avg_price(float(old_price),float(new_price),int(old_quantity),int(new_quantity))
                        pos.quantity = str(int(old_quantity)+int(new_quantity))
                        pos.sell_price = str(avg_price)
                    pos.save()
                    return HttpResponse(json.dumps({'status':'success'}), content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')


def add_new_position_into_cache(token, buy_price = None, sell_price = None):
    import numpy as np
    mu = [0.001, 0.002, -0.001, -0.002 -0.00019, 0.0001, 0.00015, 0.00019, -0.0001, -0.00015]
    sigma = 0.01
    np.random.seed(0)
    mu_value = random.choice(mu)
    if buy_price == None:
        price = float(sell_price)
    elif sell_price == None:
        price = float(buy_price)
    returns = np.random.normal(loc=mu_value, scale=sigma, size=1000)
    price = price*(1+returns).cumprod()
    price = price.tolist()
    price = list(map(lambda a: round(a, 2), price))
    for i in price:
        redis_connection.rpush(token, i)
    token_string = redis_connection.hget("positions", "tokens").decode()
    token_string = str(token_string).strip()+" "+str(token)
    redis_connection.hmset("positions", {'tokens': token_string.strip()})
    return



def place_order(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            expiry = request.POST.get('expiry')
            stoploss = int(request.POST.get('stoploss'))
            target = int(request.POST.get('target'))
            side = request.POST.get('side')
            strike = request.POST.get('strike')
            quantity = request.POST.get('quantity')
            order_type = request.POST.get('type')
            symbol = str(name)+str(expiry)+str(strike)+str(side)
            token_by_symbol = SymbolAndToken.objects.get(symbol=symbol)
            token = token_by_symbol.token

            ltp = get_ltp_data('NFO', symbol, token)
            
            ltp = float(ltp)
            if stoploss == 0:
                stoploss = 'NA'
            if order_type == 'Buy':
                target_price = str(round(ltp + ((ltp*target)/100),2))
                final_type =  'BUY -> SELL'
                if stoploss == 'NA':
                    stoploss_price = 'NA'
                    trail_list = "NA"
                else:
                    stoploss_price = str(round(ltp - ((ltp*stoploss)/100),2))
                    trail_list = buy_trail_list(ltp,((stoploss)/100))
            elif order_type == 'Sell':
                target_price = str(round(ltp - ((ltp*target)/100),2))
                final_type = 'SELL -> BUY'
                if stoploss == 'NA':
                    stoploss_price = 'NA'
                    trail_list = "NA"
                else:
                    stoploss_price = str(round(ltp + ((ltp*stoploss)/100),2))
                    trail_list = sell_trail_list(ltp,((stoploss)/100))
            date_time = get_date_time()
            try:
                current_pos = Position.objects.get(symbol=symbol,order_type=final_type)
            except Position.DoesNotExist:
                current_pos = False
            if current_pos:
                if current_pos.status == "Active" and current_pos.order_type == final_type:
                    current_quant = int(current_pos.quantity)
                    if final_type == 'BUY -> SELL':
                        current_buy_price = float(current_pos.buy_price)
                        avg_price = get_avg_price(current_buy_price,ltp,current_quant,int(quantity))
                        current_pos.quantity = str(current_quant+int(quantity))
                        current_pos.buy_price = str(avg_price)
                    elif final_type == 'SELL -> BUY':
                        current_sell_price = float(current_pos.sell_price)
                        avg_price = get_avg_price(current_sell_price,ltp,current_quant,int(quantity))
                        current_pos.quantity = str(current_quant+int(quantity))
                        current_pos.sell_price = str(avg_price)
                    if current_pos.stoploss != "NA|NA":
                        sl_percentage = int(current_pos.stoploss.split('|')[1])
                        if order_type == 'Buy':
                            current_pos.stoploss = str(ltp - ((avg_price*sl_percentage)/100))+'|'+str(sl_percentage)
                            trail_list = buy_trail_list(int(float(avg_price)),sl_percentage/100)
                        elif order_type == 'Sell':
                            current_pos.stoploss = str(ltp + ((avg_price*sl_percentage)/100))+'|'+str(sl_percentage)
                            trail_list = sell_trail_list(int(float(avg_price)),sl_percentage/100)
                        current_pos.save()
                    else:
                        if current_pos.stoploss == "NA|NA" and stoploss == "NA":
                            current_pos.save()
                else:
                    if order_type == 'Buy':
                        Position.objects.create(
                            name = name,
                            symbol = symbol,
                            token = token,
                            order_type = final_type,
                            quantity = quantity,
                            buy_price = str(ltp),
                            stoploss = stoploss_price+'|'+str(stoploss),
                            target = target_price+'|'+str(target),
                            start_time = date_time,
                            status  = 'Active'
                        )
                        add_new_position_into_cache(token, buy_price = ltp)
                    elif order_type == 'Sell':
                        Position.objects.create(
                            name = name,
                            symbol = symbol,
                            token = token,
                            order_type = final_type,
                            quantity = quantity,
                            sell_price = str(ltp),
                            stoploss = stoploss_price+'|'+str(stoploss),
                            target = target_price+'|'+str(target),
                            start_time = date_time,
                            status  = 'Active'
                        )
                        add_new_position_into_cache(token, sell_price = ltp)
            else:
                if order_type == 'Buy':
                    Position.objects.create(
                        name = name,
                        symbol = symbol,
                        token = token,
                        order_type = final_type,
                        quantity = quantity,
                        buy_price = str(ltp),
                        stoploss = stoploss_price+'|'+str(stoploss),
                        target = target_price+'|'+str(target),
                        start_time = date_time,
                        status  = 'Active'
                    )
                    add_new_position_into_cache(token, buy_price = ltp)
                elif order_type == 'Sell':
                    Position.objects.create(
                        name = name,
                        symbol = symbol,
                        token = token,
                        order_type = final_type,
                        quantity = quantity,
                        sell_price = str(ltp),
                        stoploss = stoploss_price+'|'+str(stoploss),
                        target = target_price+'|'+str(target),
                        start_time = date_time,
                        status  = 'Active'
                    )
                    add_new_position_into_cache(token, sell_price = ltp)
            return HttpResponse(json.dumps({'status':'success','trail_data':trail_list}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')


def get_all_positions(request):
    try:
        if request.method == 'GET':
            positions = []
            #start_trailing()
            close_positions = []
            try:
                pos_obj = Position.objects.all().order_by('-start_time')
            except:
                pos_obj = False
            if pos_obj:
                for p in pos_obj:
                    if p.status == "Active":
                        if p.half_quantity == '':
                            positions.append({
                                'symbol':p.symbol,
                                'token':p.token,
                                'order_type':p.order_type,
                                'quantity':p.quantity,
                                'half_quantity':p.half_quantity,
                                'full_exit_quantity':p.fill_exit_quantity,
                                'buy_price':p.buy_price,
                                'half_exit_price':p.half_exit_price,
                                'sell_price':p.sell_price,
                                'stoploss':p.stoploss,
                                'target':p.target,
                                'start_time':str(p.start_time),
                                'half_exit_time':str(p.half_exit_time),
                                'end_time':str(p.end_time),
                                'status':p.status
                            })
                        else:
                            positions.append({
                                'symbol':p.symbol,
                                'token':p.token,
                                'order_type':p.order_type,
                                'quantity':p.quantity,
                                'half_quantity':p.half_quantity,
                                'full_exit_quantity':p.fill_exit_quantity,
                                'buy_price':p.buy_price,
                                'half_exit_price':p.half_exit_price,
                                'sell_price':p.sell_price,
                                'stoploss':p.stoploss,
                                'target':p.target,
                                'start_time':str(p.start_time),
                                'half_exit_time':str(p.half_exit_time),
                                'end_time':str(p.end_time),
                                'status':p.status
                            })
                            close_positions.append({
                                'symbol':p.symbol,
                                'token':p.token,
                                'order_type':p.order_type,
                                'quantity':p.quantity,
                                'half_quantity':p.half_quantity,
                                'full_exit_quantity':p.fill_exit_quantity,
                                'buy_price':p.buy_price,
                                'half_exit_price':p.half_exit_price,
                                'sell_price':p.sell_price,
                                'stoploss':p.stoploss,
                                'target':p.target,
                                'start_time':str(p.start_time),
                                'half_exit_time':str(p.half_exit_time),
                                'end_time':str(p.end_time),
                                'status':'Close'
                            })
                    elif p.status == "Close":
                        close_positions.append({
                            'symbol':p.symbol,
                            'token':p.token,
                            'order_type':p.order_type,
                            'quantity':p.quantity,
                            'half_quantity':p.half_quantity,
                            'full_exit_quantity':p.fill_exit_quantity,
                            'buy_price':p.buy_price,
                            'half_exit_price':p.half_exit_price,
                            'sell_price':p.sell_price,
                            'stoploss':p.stoploss,
                            'target':p.target,
                            'start_time':str(p.start_time),
                            'half_exit_time':str(p.half_exit_time),
                            'end_time':str(p.end_time),
                            'status':p.status
                        })
                positions.extend(close_positions)
                return HttpResponse(json.dumps({'status':'success','positions':json.dumps(positions)}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status':'Not found any active positions'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')



def complete_the_day(request):
    try:
        if request.method == 'GET':
            try:
                positions = Position.objects.all()
            except:
                positions = False
            buy_trades = 0
            sell_trades = 0
            buy_quanity = 0
            sell_quantity = 0
            buy_profit_trades = 0
            sell_profit_trades = 0
            buy_win_rate = ''
            sell_win_rate = ''
            buy_pnl = 0
            sell_pnl = 0
            if positions:
                for position in positions:
                    if position.status == "Close":
                        token_string = redis_connection.hget("positions", "tokens").decode()
                        token_string = str(token_string).strip().split(" ")
                        final_tokens = ""
                        for tokens in token_string:
                            if str(position.token) == str(tokens):
                                redis_connection.delete(position.token)
                            else:
                                final_tokens += tokens+" "
                        redis_connection.hmset("positions", {'tokens': final_tokens.strip()})
                        if position.order_type == "BUY -> SELL":
                            buy_trades += 1
                            buy_quanity += int(position.quantity)
                            buy_pnl += float(position.p_n_l)
                            if float(position.p_n_l) > 0:
                                buy_profit_trades += 1
                        elif position.order_type == "SELL -> BUY":
                            sell_trades += 1
                            sell_quantity += int(position.quantity)
                            sell_pnl += float(position.p_n_l)
                            if float(position.p_n_l) > 0:
                                sell_profit_trades += 1
                        TradeBook.objects.create(
                            name = position.name,
                            symbol = position.symbol,
                            token = position.token,
                            order_type = position.order_type,
                            quantity = position.quantity,
                            half_quantity = position.half_quantity,
                            fill_exit_quantity = position.fill_exit_quantity,
                            buy_price = position.buy_price,
                            half_exit_price = position.half_exit_price,
                            sell_price = position.sell_price,
                            stoploss = position.stoploss,
                            target = position.target,
                            start_time = position.start_time,
                            half_exit_time = position.half_exit_time,
                            end_time = position.end_time,
                            strategy = position.strategy,
                            p_n_l = position.p_n_l
                        )
                buy_win_rate = str(buy_profit_trades)+'/'+str(buy_trades)
                sell_win_rate = str(sell_profit_trades)+'/'+str(sell_trades)
                DaywiseSummery.objects.create(
                    date = get_date_time(),
                    total_buy_trades = str(buy_trades),
                    total_sell_trades = str(sell_trades),
                    total_buy_quantity = str(buy_quanity),
                    total_sell_quantity = str(sell_quantity),
                    win_buy_rate = buy_win_rate,
                    win_sell_rate = sell_win_rate,
                    buy_percentage = '0',
                    sell_percentage = '0',
                    buy_p_n_l = str(buy_pnl),
                    sell_p_n_l = str(sell_pnl),
                )
                for position in positions:
                    if position.status == 'Close':
                        position.delete()
                return HttpResponse(json.dumps({'status':'success'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')


def get_all_ltp(request):
    try:
        if request.method == 'GET':
            #obj = get_api_object()
            try:
                positions = Position.objects.all()
            except:
                positions = False
            if positions:
                final_list = []
                # nifty_ltp,nifty_close_price = get_ltp_data_with_close_price(obj,'NSE','NIFTY','26000')
                # banknifty_ltp,banknifty_close_price  = get_ltp_data_with_close_price(obj,'NSE','BANKNIFTY','26009')
                # nifty_ltp,nifty_close_price,banknifty_ltp,banknifty_close_price = float(nifty_ltp),float(nifty_close_price),float(banknifty_ltp),float(banknifty_close_price)
                # percent_nifty_change = str(round(((nifty_ltp - nifty_close_price)/nifty_close_price)*100,2))
                # percent_banknifty_change = str(round(((banknifty_ltp - banknifty_close_price)/banknifty_close_price)*100,2))
                final_list.append(
                    {
                        'tk':'26000',
                        'change':'3.4',
                        'ltp':str(random.randint(17000,18000)),
                    })
                final_list.append(
                    {
                        'tk':'26009',
                        'change':'2.4',
                        'ltp':str(random.randint(34000,36000)),
                    }
                )
                for position in positions:
                    token = position.token
                    #ltp = get_ltp_data(obj,'NFO',position.symbol,token)
                    final_list.append(
                        {
                            'tk':token,
                            'ltp':str(random.randint(300,600)),
                        }
                    )
                data = {'data': final_list}
                sleep(1)
                return HttpResponse(json.dumps({'status':'success','data':json.dumps(data)}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)
        return HttpResponse(json.dumps({'status':'failure'}), content_type='application/json')