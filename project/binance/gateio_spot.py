from __future__ import print_function

import time

import gate_api
from gate_api.exceptions import ApiException, GateApiException
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取配置文件中的数据
api_key = config.get('GATE', 'api_key')
api_secret = config.get('GATE', 'api_secret')

# Configure APIv4 key authorization
configuration = gate_api.Configuration(
    host="https://api.gateio.ws/api/v4",
    key=api_key,
    secret=api_secret
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.FlashSwapApi(api_client)


def preview_request():
    sell_currency = "BTC"
    sell_amount = "0.01"
    buy_currency = "USDT"
    flash_swap_preview_request = gate_api.FlashSwapPreviewRequest(sell_currency=sell_currency, sell_amount=sell_amount,
                                                                  buy_currency=buy_currency)
    # Initiate a flash swap order preview
    api_response = api_instance.preview_flash_swap_order(flash_swap_preview_request)
    # print(api_response)
    return api_response


if __name__ == '__main__':
    for i in range(20):
        api_response = preview_request()
        print(api_response.price)
        time.sleep(1)
