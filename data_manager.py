import requests
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from shop_info import Shopper
import math

shopper = Shopper()
SHOP_DATA = shopper.shop_data
ITEM_SUB_FONT = ImageFont.truetype("data/src/fortnite.otf", 100)
ITEM_NAME_FONT = ImageFont.truetype("data/src/fortnite.otf", 30) #35
ITEM_DESC_FONT = ImageFont.truetype("data/src/fortnite.otf", 25)

# TODO: fix long name (make double rows)

class Manager:
    def __init__(self):
        self.icon_width = 256
        self.icon_height = 256
        self.icon_frame = 8
        self.spacing = 4
        self.columns = 6
        self.bg_width = (self.icon_width * self.columns) + (self.columns * self.spacing)
        self.current_width = 0
        self.current_height = 0
        self.max_name_size = 240
        #TODO: Quitar esto comentario de crear bg?
        self.create_bg()

    def get_images(self, shop_sections):
        for key, value in shop_sections.items():
            folder_path = 'section'
            if value[0] == 'featured':
                folder_path = 'featured'
            elif value[0] == 'daily':
                folder_path = 'daily'

            image = value[3]

            filename = f"./data/icons/{folder_path}/{key}.png"
            r = requests.get(image, stream=True)

            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            img_file = Image.open(filename)
            resized_img = img_file.resize((self.icon_width - self.icon_frame, self.icon_height - self.icon_frame))
            img_rgba = resized_img.convert('RGBA')
            icon_file = self.paint(img_rgba, filename, key, value)
            icon_file.save(filename)
            # print('Image successfully Downloaded: ', filename)
        
            #AQUI se dibuja la tienda!!!!!!!
            self.draw_shop(filename, folder_path, key)

    def paint(self, image, path, name, info):
        rarity_info = info[1]
        price_info = info[2]
        width = image.width - self.icon_frame
        height = image.height - self.icon_frame
        color = (0, 0, 0)
        frame_color = (0, 0, 0)
        if rarity_info == 'legendary':
            color = (234, 141, 35)
            frame_color = (120, 55, 29)
        elif rarity_info == 'epic':
            color = (195, 89, 255)
            frame_color = (75, 36, 131)
        elif rarity_info == 'rare':
            color = (44, 193, 255)
            frame_color = (20, 57, 119)
        elif rarity_info == 'uncommon':
            color = (105, 187, 30)
            frame_color = (23, 81, 23)
        elif rarity_info == 'common':
            color = (190, 190, 190)
            frame_color = (100, 100, 100)
        elif rarity_info == 'dark':
            color = (251, 34, 223)
            frame_color = (82, 12, 111)
        elif rarity_info == 'dc':
            color = (84, 117, 199)
            frame_color = (36, 52, 97)
        elif rarity_info == 'marvel':
            color = (197, 51, 52)
            frame_color = (118, 27, 27)
        elif rarity_info == 'lava':
            color = (217, 94, 37)
            frame_color = (106, 10, 49)
        elif rarity_info == 'frozen':
            color = (148, 223, 255)
            frame_color = (38, 158, 214)
        elif rarity_info == 'slurp':
            color = (41, 241, 163)
            frame_color = (18, 169, 164)
        elif rarity_info == 'icon_series':
            color = (0, 255, 255)
            frame_color = (18, 169, 164)
        elif rarity_info == 'shadow':
            color = (64, 64, 64)
            frame_color = (25, 25, 25)
        elif rarity_info == 'star_wars':
            color = (27, 54, 110)
            frame_color = (8, 23, 55)
        elif rarity_info == 'gaming_legends':
            color = (47, 12, 50)
            frame_color = (22, 6, 24)

        # Change frame?
        icon_frame = Image.new(mode="RGB", size=(self.icon_width, self.icon_height), color=frame_color)
        icon_bg = Image.new(mode="RGB", size=(width, height), color=color)
        icon_frame.paste(icon_bg, box=(self.icon_frame, self.icon_frame))

        icon_frame.paste(image, image)

        tint_w = self.icon_width - (self.icon_frame * 2)
        tint_h = round(self.icon_height / 3)

        black_tint = Image.new(mode="RGBA", size=(tint_w, tint_h - self.icon_frame), color=(0, 0, 0, 80))
        off_y = round((self.icon_height / 3) * 2)
        offset = self.icon_frame, off_y
        icon_frame.paste(black_tint, mask=black_tint, box=offset)
        icon_frame.save(path)

        icon = Image.open(path)
        vbuck_icon = Image.open('data/src/vbuck.png')
        # TODO: find formula for vbuck icon resize
        vbuck_resized = vbuck_icon.resize((23, 23))
        vbuck = vbuck_resized.convert('RGBA')
        draw = ImageDraw.Draw(icon)
        item_name_size = ITEM_NAME_FONT.getsize(name)
        # Resize name if bigger than 240 [242 for actual border]
        # Created a new self.max_name_size so it's easy
        # muestra nombre + tamano en la consola
        # print(f'{name.split()}: {item_name_size}')
        # #
        # if item_name_size[0] > self.max_name_size:
        #     item_name_size = (self.max_name_size/2, item_name_size[1])

        item_price_size = ITEM_DESC_FONT.getsize(price_info)
        item_price_x = (icon.size[0] - item_price_size[0]) // 2
        item_price_y = ((self.icon_height / 4) * 3) + ((self.icon_height / 4) / 2)
        item_name_x = (icon.size[0] - item_name_size[0]) // 2 ##Cambuar a 2
        item_name_y = (self.icon_height / 4) * 3
        draw.text(xy=(item_name_x, item_name_y - 13), text=name, fill=(255, 255, 255), font=ITEM_NAME_FONT)
        draw.text(xy=(item_price_x + 5, item_price_y - 4), text=price_info, fill=(255, 255, 255), font=ITEM_DESC_FONT)
        icon.paste(vbuck, mask=vbuck, box=(round(item_price_x - (25 - 5)), round(item_price_y - 6)))

        icon.save(path)

        return icon

    def draw_shop(self, item_file, section, name):
        bg = Image.open('data/shop/shop.png')
        featured_items = shopper.featured_data
        n_featured_items = 0
        for item in featured_items:
            n_featured_items += 1
        
        featured = shopper.get_featured()
        last_featured_item = list(featured.keys())[-1]
        
        if section == "featured":
            if self.current_width == 0:
                # TODO: REVISAR CALCULOS (quitar 155)
                self.current_height += self.spacing + 155
            elif self.current_width == self.bg_width:
                self.current_height += self.icon_height + self.spacing

            if self.current_width >= self.bg_width:
                self.current_width = self.spacing
            else:
                self.current_width += self.spacing

            position = (self.current_width, self.current_height)
            print(f"name:{name}")
                
        elif section == "daily":
            print(f"start of daily width: {self.current_width}")
            if self.current_width == 0:
                # TODO: REVISAR CALCULOS (quitar 250)
                self.current_height = round(self.icon_height*(n_featured_items/6)) + (self.icon_height+250)
            elif self.current_width == self.bg_width:
                self.current_height += self.icon_height + self.spacing

            if self.current_width >= self.bg_width:
                self.current_width = self.spacing
            else:
                self.current_width += self.spacing
            
        position = (self.current_width, self.current_height)
        
        item = Image.open(item_file)
        bg.paste(item, position)
        bg.save(f'data/shop/shop.png')

        self.current_width += self.icon_width
        
        # print(f"width: {self.current_width}")
        # print(f"height: {self.current_height}")
        
        if name == last_featured_item:
            self.current_width = 0

    def create_bg(self):
        featured_items = shopper.featured_data
        n_featured_items = 0
        for item in featured_items:
            n_featured_items += 1
        print(n_featured_items)
        
        daily_items = shopper.daily_data
        n_daily_items = 0
        for item in daily_items:
            n_daily_items += 1
        print(n_daily_items)
        
        num_of_items = n_featured_items + n_daily_items
        width = self.bg_width + self.spacing
        n_rows = num_of_items / 6
        rows = math.ceil(n_rows)
        # TODO: QUITAR EL 164*2
        height = (self.icon_height * rows) + (rows * self.spacing + self.spacing) + (self.icon_height*2) + round(self.icon_height/2)

        fn = Image.open('data/src/fn_bg.jpg')
        fn_bg = fn.rotate(90, expand=True)
        img_bg = Image.new(mode="RGB", size=(width, height), color=(209, 123, 193))
        fn_bg_w = int(fn_bg.width / 2)
        fn_bg_h = int(fn_bg.height / 2)
        center_img_bg_w = int(img_bg.width / 2)
        center_img_bg_h = int(img_bg.height / 2)
        img_bg.paste(fn_bg, box=((center_img_bg_w - fn_bg_w), (center_img_bg_h - fn_bg_h)))
        draw = ImageDraw.Draw(img_bg)
        draw.text(xy=(self.spacing*4, self.icon_height/4), text="Featured", fill=(255, 255, 255), font=ITEM_SUB_FONT)
        draw.text(xy=(self.spacing*4, (self.icon_height*(n_featured_items/6))+(self.icon_height)+145), text="Daily", fill=(255, 255, 255), font=ITEM_SUB_FONT)
        draw.text(xy=(self.bg_width - (self.icon_width*2) + (self.icon_width/4), self.icon_height/8), text="Item Shop", fill=(255, 255, 255), font=ITEM_SUB_FONT)
        img_bg.save(f'data/shop/shop.png')
        print('Background successfully created at data/shop/shop.png')
