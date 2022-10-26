from celery import shared_task
from celery_progress.backend import ProgressRecorder
from time import sleep
from OptionApp.models import *
import requests
from datetime import datetime

def convert(date_time):
    format = '%b %d %Y %I:%M%p'
    datetime_str = datetime.strptime(date_time, format)
    return datetime_str.date()

@shared_task(bind = True)
def process_task(self):
    SymbolAndToken.objects.all().delete()
    ExpiryDate.objects.all().delete()
    data = requests.get('https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json')
    data = data.json()
    all_expiry = []
    length = len(data)
    print(length)
    counter = 1
    for i in data:
        progress = ProgressRecorder(self)
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
        progress.set_progress(counter+1, length)
        counter+=1
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
    return "Done"