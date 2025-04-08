import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random
import json
import os

class MafengwoSpider:
    def __init__(self):
        self.ua = UserAgent()
        self.base_url = "https://www.mafengwo.cn"
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        
    def get_page(self, url):
        """获取页面内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_attractions(self, city_id):
        """解析景点信息"""
        attractions = []
        page = 1
        while True:
            url = f"{self.base_url}/poi/{city_id}.html"
            html = self.get_page(url)
            if not html:
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            attraction_items = soup.select('.poi-list .poi-item')
            
            if not attraction_items:
                break
                
            for item in attraction_items:
                try:
                    name = item.select_one('.title').text.strip()
                    rating = item.select_one('.rating')['title'] if item.select_one('.rating') else '暂无评分'
                    reviews = item.select_one('.review-num').text.strip() if item.select_one('.review-num') else '0'
                    address = item.select_one('.address').text.strip() if item.select_one('.address') else '暂无地址'
                    
                    attractions.append({
                        'name': name,
                        'rating': rating,
                        'reviews': reviews,
                        'address': address
                    })
                except Exception as e:
                    print(f"Error parsing attraction: {e}")
                    continue
            
            page += 1
            time.sleep(random.uniform(1, 3))  # 随机延迟
            
        return attractions

    def parse_hotels(self, city_id):
        """解析酒店信息"""
        hotels = []
        page = 1
        while True:
            url = f"{self.base_url}/hotel/{city_id}/"
            html = self.get_page(url)
            if not html:
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            hotel_items = soup.select('.hotel-item')
            
            if not hotel_items:
                break
                
            for item in hotel_items:
                try:
                    name = item.select_one('.title').text.strip()
                    price = item.select_one('.price').text.strip() if item.select_one('.price') else '暂无价格'
                    rating = item.select_one('.rating')['title'] if item.select_one('.rating') else '暂无评分'
                    address = item.select_one('.address').text.strip() if item.select_one('.address') else '暂无地址'
                    
                    hotels.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'address': address
                    })
                except Exception as e:
                    print(f"Error parsing hotel: {e}")
                    continue
            
            page += 1
            time.sleep(random.uniform(1, 3))  # 随机延迟
            
        return hotels

    def save_to_csv(self, data, filename):
        """保存数据到CSV文件"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到 {filename}")

def main():
    spider = MafengwoSpider()
    
    # 乌鲁木齐和伊犁的城市ID
    cities = {
        '乌鲁木齐': '10099',
        '伊犁': '10133'
    }
    
    # 创建保存数据的目录
    if not os.path.exists('data'):
        os.makedirs('data')
    
    for city_name, city_id in cities.items():
        print(f"开始爬取{city_name}的景点信息...")
        attractions = spider.parse_attractions(city_id)
        spider.save_to_csv(attractions, f'data/{city_name}_attractions.csv')
        
        print(f"开始爬取{city_name}的酒店信息...")
        hotels = spider.parse_hotels(city_id)
        spider.save_to_csv(hotels, f'data/{city_name}_hotels.csv')

if __name__ == "__main__":
    main() 