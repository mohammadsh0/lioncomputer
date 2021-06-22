import requests
from bs4 import BeautifulSoup
import re
import sys

def num_of_pagss(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    mine = []
    for item in soup.select('div.pagination-wrapper ul li a'):
        mine.append(item.text)
    return(int(mine[-1]))

class lionComputer():
    def __init__(self):
        self.base_url = 'https://www.lioncomputer.com/category/'
        self.part_dict = {
            'case': ('7dy6b/computer-case12', '12'),
            'cpu': ('7e23b/processor15', '15'),
            'hdd': ('qe5ze/hard-disk-drive18', '18'),
            'power': ('dmq5e/power-supply27', '27'),
            'gpu': ('bp52d/graphic-card29', '29'),
            'ram': ('d4jkd/computer-memory63', '63'),
            'main': ('d65nb/motherboard88', '88'),
            'ssd': ('bw9qd/solid-state-drive110', '110')
}
        self.selected_parts = []
    def products(self, cat_url, cat_num):
        page_num = 1
        url_changer = lambda url_num: f'?sortBy=price&sortType=desc&page={page_num}&categories={url_num}&isAvailable=1&attributes=&q='
        num_of_pages = num_of_pagss(self.base_url + cat_url + url_changer(cat_num))
        self.part_list = []
        self.price_list = []

        while page_num <= num_of_pages:
            part = cat_url + url_changer(cat_num)
            page = requests.get(self.base_url + part)
            soup = BeautifulSoup(page.content, 'html.parser')

            page = soup.select('div.products_grid')

            for strong in soup.select('div.product__body strong'):
                strong = re.findall('[0-9]', strong.text)
                price = ''
                for digit in strong:
                    price += digit
                self.price_list.append(price)

            for h5 in soup.select('div.product__body h5'):
                h5 = re.findall('[A-Za-z].*', h5.text)
                self.part_list.append(str(h5[0]))

            page_num += 1

        i = 0
        while i < len(self.price_list):
            print(self.part_list[i] + "\t\t" + self.price_list[i])
            i += 1

    def selectProduct(self):
        for i, part in enumerate(self.part_dict.keys()):
            print(f'{[i+1]}: {part.upper()}')

        while True:
            try:
                value = int(input('Select the category of desired products to find their prices: '))
                break
            except ValueError:
                print('Not Valid. Try again...')

        for i, part in enumerate(self.part_dict.values()):
            if i == value - 1:
                self.products(part[0], part[1])
            if value > len(self.part_dict):
                total = 0
                for item in self.selected_parts:
                    total += int(item[1])
                    print(item[0] + ': ' + item[1])
                print(f"Total Price: ", str(total/1000))
                sys.exit()

    def search(self, txt):
        i = 1
        search_list = []
        for item in self.part_list:
            if txt.lower() in item.lower():
                index = self.part_list.index(item)
                # print(f'{[i]}: ' + item, self.price_list[index])
                search_list.append((item, self.price_list[index]))
        for item in search_list:
            print(f'{[i]}: ' + item[0], item[1])
            i += 1

        while True:
            try:
                value = int(input('Select product: '))
                break
            except ValueError:
                print('Not Valid. Try again...')
        print('The Selected part is:')
        print(search_list[value - 1][0], search_list[value - 1][1])
        self.selected_parts.append((search_list[value - 1][0], search_list[value - 1][1]))


pc = lionComputer()
while True:
    try:
        pc.selectProduct()
        search_item = input('Search: ')
        pc.search(search_item)
    except Exception:
        break