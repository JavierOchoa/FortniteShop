import requests

FNBR_API = ''
FNBR_ENDPOINT = 'https://fnbr.co/api'
HEADER = {'x-api-key': f'{FNBR_API}'}


class Shopper:
    def __init__(self):
        self.response = requests.get(f'{FNBR_ENDPOINT}/shop', headers=HEADER)
        self.shop_data = self.response.json()
        self.featured_data = self.shop_data['data']['featured']
        self.daily_data = self.shop_data['data']['daily']

    def get_featured(self):
        featured_dict = {}
        for item in self.featured_data:
            name = item["name"]
            values = []
            price = item["price"]
            image = item["images"]["featured"]
            if item["images"]["featured"] == False:
                image = item["images"]["icon"]
            rarity = item["rarity"]
            values.append('featured')
            values.append(rarity)
            values.append(price)
            values.append(image)
            featured_dict[name] = values
        return featured_dict

    def get_daily(self):
        daily_dict = {}
        for item in self.daily_data:
            name = item["name"]
            values = []
            price = item["price"]
            image = item["images"]["featured"]
            if item["images"]["featured"] == False:
                image = item["images"]["icon"]
            rarity = item["rarity"]
            values.append('daily')
            values.append(rarity)
            values.append(price)
            values.append(image)
            daily_dict[name] = values
        return daily_dict

    def get_num_items(self):
        num_of_items = 0
        featuredss = 0
        dayyy = 0
        for item in self.featured_data:
            featuredss += 1
            num_of_items += 1

        for item in self.daily_data:
            dayyy += 1
            num_of_items += 1

        print(featuredss)
        return num_of_items
