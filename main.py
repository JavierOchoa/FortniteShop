import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from shop_info import Shopper
from data_manager import Manager
from pprint import pprint

shopper = Shopper()
manager = Manager()

manager.create_bg()
featured = shopper.get_featured()
daily = shopper.get_daily()
manager.get_images(featured)
manager.get_images(daily)

