from smartapi import SmartConnect
from smartapi import SmartWebSocket
import sys, pickle
from django.conf import settings
from django_redis import get_redis_connection
redis_connection = get_redis_connection("default")

def get_api_object():
    if "api_object" in redis_connection:
        pickelled_object = redis_connection.get("api_object")
        unpickelled_object = pickle.loads(pickelled_object)
        return unpickelled_object
    else:
        object=SmartConnect(api_key=settings.API_KEY)
        account_data = object.generateSession('user_id',settings.PASSWORD,'639899')
        pickelled_object = pickle.dumps(object)
        redis_connection.set("api_object", pickelled_object)
        return object

def get_ltp_data(exchange, symbol, token):
    try:
        obj = get_api_object()
        ltp = obj.ltpData(exchange,symbol,token)
        return ltp['data']['ltp']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e,' at line ',exc_tb.tb_lineno)

def get_ltp_data_with_close_price(exchange, symbol,token):
    obj = get_api_object()
    ltp = obj.ltpData(exchange,symbol,token)
    return (ltp['data']['ltp'],ltp['data']['close'])

def get_ltp_data_with_obj(obj, exchange, symbol,token):
    ltp = obj.ltpData(exchange,symbol,token)
    return ltp['data']['ltp']

# def get_ltp_data(obj,symbal,token):
#     response = {}
#     response['status'] = 500
#     response['message'] = 'Error: Get LTP Data Failed'
#     try:
#         ltp = obj.ltpData('NFO',symbal,token)
#         if ltp['status'] == True and ltp['errorcode'] == '':
#             response['status'] = 200
#             response['message'] = 'Get LTP Data Successfully'
#             response['ltp'] = ltp['data']['ltp']
#             return response
#         else:
#             response['message'] = 'Get LTP Data Failed'
#             return response
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         logger.error('GetLtpData: [AOTradeApp] %s at %s',str(e),str(exc_tb.tb_lineno))
#         #teleutils.sendMessageToTelegram('Error: Get LTP Data Failed')
#         return response