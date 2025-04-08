import re
import time
import random
from bs4 import BeautifulSoup
from config import Config

class Utils:
    @staticmethod
    def parse_attraction_page(html, city_name):
        soup = BeautifulSoup(html, 'lxml')
        
        # 景点名称
        name = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
        
        # 位置信息
        location_div = soup.find('div', class_='mhd')
        location = location_div.find('p', class_='sub').get_text(strip=True) if location_div else None
        
        # 地址
        address_item = soup.find('li', class_='item-address')
        address = address_item.find('div', class_='content').get_text(strip=True) if address_item else None
        
        # 门票价格
        ticket_price = None
        student_price = None
        ticket_div = soup.find('div', class_='mod mod-detail')
        if ticket_div:
            tickets = ticket_div.find_all('tr')
            for ticket in tickets:
                cols = ticket.find_all('td')
                if len(cols) >= 2:
                    ticket_type = cols[0].get_text(strip=True)
                    price = cols[1].get_text(strip=True)
                    if '学生' in ticket_type or '学生' in price:
                        student_price = price
                    else:
                        ticket_price = price
        
        # 开放时间
        open_time_item = soup.find('li', class_='item-time')
        open_time = open_time_item.find('div', class_='content').get_text(strip=True) if open_time_item else None
        
        # 描述
        desc_div = soup.find('div', class_='summary')
        description = desc_div.get_text(strip=True) if desc_div else None
        
        # 评分
        rating_span = soup.find('span', class_='score')
        rating = float(rating_span.get_text(strip=True)) if rating_span else None
        
        # 图片
        image_url = None
        image_div = soup.find('div', class_='cover')
        if image_div and image_div.find('img'):
            image_url = image_div.find('img')['src']
        
        return {
            'city': city_name,
            'name': name,
            'location': location,
            'address': address,
            'ticket_price': ticket_price,
            'student_price': student_price,
            'open_time': open_time,
            'description': description,
            'rating': rating,
            'image_url': image_url
        }
    
    @staticmethod
    def parse_hotel_page(html, city_name):
        soup = BeautifulSoup(html, 'lxml')
        
        # 酒店名称
        name = soup.find('h1', class_='hotel-name').get_text(strip=True) if soup.find('h1', class_='hotel-name') else None
        
        # 位置信息
        location_div = soup.find('div', class_='location-info')
        location = location_div.get_text(strip=True) if location_div else None
        
        # 地址
        address_div = soup.find('div', class_='address')
        address = address_div.get_text(strip=True) if address_div else None
        
        # 价格范围
        price_span = soup.find('span', class_='price')
        price_range = price_span.get_text(strip=True) if price_span else None
        
        # 评分
        rating_span = soup.find('span', class_='score')
        rating = float(rating_span.get_text(strip=True)) if rating_span else None
        
        # 设施
        facilities = []
        facilities_div = soup.find('div', class_='facilities')
        if facilities_div:
            facilities = [f.get_text(strip=True) for f in facilities_div.find_all('li')]
        
        # 评论
        reviews = []
        review_divs = soup.find_all('div', class_='review-item')
        for div in review_divs:
            review = div.find('p', class_='content').get_text(strip=True) if div.find('p', class_='content') else None
            if review:
                reviews.append(review)
        
        return {
            'city': city_name,
            'name': name,
            'location': location,
            'address': address,
            'price_range': price_range,
            'rating': rating,
            'facilities': ', '.join(facilities),
            'reviews': ' | '.join(reviews)
        }
    
    @staticmethod
    def random_sleep():
        time.sleep(Config.REQUEST_INTERVAL + random.uniform(0, 1))