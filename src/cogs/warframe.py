import json
import requests
import time

#from utils.logger import logger



class Warframe():
    def __init__(self):
        self.base_url = 'https://api.warframestat.us'
        self.market_base_url = 'https://api.warframe.market/v1'
        self.base_params = {'language': 'en'}
    
    def get_non_vaulted_prime(self):
        url = f'{self.base_url}/items/search/prime'
        params = self.base_params
        params['only'] = 'name,vaulted,category'

        response = requests.get(url, params=params)

        if response.status_code != 200:
            #logger.warning(f'Can\'t call {url}. Get response code {response.status_code}')
            pass
        
        nonVaulted = []
        for item in response.json():
            if 'vaulted' in item.keys():
                nonVaulted.append(item)
        
        return nonVaulted

    def get_market_cheapest_price(self, item_name):

        set_info_req = requests.get(f'{self.market_base_url}/items/{item_name}_set')

        if set_info_req.status_code != 200:
            print(f'An error occured on {set_info_req.url} and got HTTP code {set_info_req.status_code}')
            #logger.warning(f'Can\'t call {self.market_base_url}/items/{item_name}')
            return None
        
        items_in_set = set_info_req.json()

        if 'payload' not in items_in_set.keys():
            print(f'An error occured ine the response from {set_info_req.url}. Body only got {items_in_set.keys()}')
            #logger.warning(f'Can\'t call {self.market_base_url}/items/{item_name}')
            return None

        
        cheapest_prices_dict = {}
        for item in items_in_set['payload']['item']['items_in_set']:
            set_item_name = item['url_name']
            market_url = f'{self.market_base_url}/items/{set_item_name}/orders'
            headers = {'Platform': 'pc'}

            market_response = requests.get(market_url, headers=headers)

            if market_response.status_code == 200:
                market_response_json = market_response.json()
                print(market_url)
            else:
                print(f'An error occured on {market_url}')
                continue

            if 'error' in market_response_json.keys():
                cheapest_prices_dict[set_item_name] = 0
                print(market_response_json["error"])
                #logger.warning(f'An error happen while contacting Warframe Market API for the following item: {set_item_name}.\nError was: {market_response_json["error"]}')
                continue

            orders = market_response_json['payload']['orders']
            
            cheapest = 0
            for order in orders:
                if order['visible'] is False or 'buy' in order['order_type'] or 'offline' in order['user']['status']:
                    continue

                if order['platinum'] < cheapest or cheapest == 0:
                    cheapest = order['platinum']
            
            cheapest_prices_dict[set_item_name] = {}
            cheapest_prices_dict[set_item_name]['ducats'] = item['ducats']
            cheapest_prices_dict[set_item_name]['platinum'] = cheapest

        return cheapest_prices_dict

    def get_expensive_non_vaulted(self):
        non_vaulted_items = self.get_non_vaulted_prime()
        prime_and_value = {}

        for item in non_vaulted_items:
            item_name = item['name'].lower().replace(' ', '_')
            print(item_name)

            item_plat_value = self.get_market_cheapest_price(item_name)

            if item_plat_value is not None:
                prime_and_value[item_name] = item_plat_value
            else:
                #logger.warning(f'an error occured while trying to fetch information for {item_name}')
                continue

            #time.sleep(1)

    
        print(prime_and_value)

        # Specify the filename
        filename = "cheapest_prices.json"

        # Write dictionary to JSON file
        with open(filename, "w") as json_file:
            json.dump(prime_and_value, json_file, indent=4)

warframe = Warframe()
warframe.get_expensive_non_vaulted()