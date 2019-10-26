import requests
import time
from datetime import datetime


ETHEREUM_API_URL = 'https://api.coinmarketcap.com/v1/ticker/ethereum/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/jaMzeYnBLqDdAp2U4QqJkVsnRMH7DDs_CwEcuGwrtou'
ETHEREUM_PRICE_THRESHOLD = 179

def get_latest_ethereum_price():
    response = requests.get(ETHEREUM_API_URL)
    response_json = response.json()
    #Convert the price to a floating point number
    return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value):
    #the payload that will be sent to IFTTT service
    data = {'value1': value}
    #inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    #Sends a HTTP POST request to a webhook URL
    requests.post(ifttt_event_url, json=data)

def format_ethereum_history(ethereum_history):
    rows = []
    for ethereum_price in ethereum_history:
        date = ethereum_price['date'].strftime('%d.%m.%Y %H:%M')
        price = ethereum_price['price']
        row = '{}: $<br>{}</br>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)


def main():
    ethereum_history = []
    while True:
        price = get_latest_ethereum_price()
        date = datetime.now()
        ethereum_history.append({'date': date, 'price': price})

        if price < ETHEREUM_PRICE_THRESHOLD:
            post_ifttt_webhook('ether_price_emergency', price)

        if len(ethereum_history) == 5:
            post_ifttt_webhook('ether_price_update',
                                format_ethereum_history(ethereum_history))

            ethereum_history = []

        time.sleep(60)


if __name__ == '__main__':
    main()




