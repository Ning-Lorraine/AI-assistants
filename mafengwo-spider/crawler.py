import requests
import json
from bs4 import BeautifulSoup
from config import Config
from markdown_writer import MarkdownWriter
from proxy import ProxyManager
from utils import Utils
import time
import random

class MafengwoCrawler:
    def __init__(self):
        self.writer = MarkdownWriter()
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
    
    def crawl_city_data(self):
        """爬取所有目标城市的数据"""
        for city_name, city_id in Config.TARGET_CITIES.items():
            print(f"\n{'='*30}")
            print(f"开始爬取 {city_name} 的数据...")
            print(f"{'='*30}")
            
            # 爬取景点数据
            self.crawl_attractions(city_name, city_id)
            
            # 爬取酒店数据
            self.crawl_hotels(city_name, city_id)
            
            print(f"\n{city_name} 数据爬取完成!")
    
    def crawl_attractions(self, city_name, city_id, max_pages=3):
        """爬取指定城市的景点数据"""
        print(f"\n开始爬取 {city_name} 的景点数据...")
        
        for page in range(1, max_pages + 1):
            print(f"\n正在获取第 {page} 页景点列表...")
            
            # 获取景点列表
            attractions = self._get_attraction_list(city_id, page)
            if not attractions:
                print(f"第 {page} 页没有获取到景点数据，可能已达末尾")
                break
            
            for idx, attraction in enumerate(attractions, 1):
                try:
                    poi_id = attraction['poi_id']
                    attraction_name = attraction.get('name', '未知景点')
                    attraction_url = f"https://www.mafengwo.cn/poi/{poi_id}/gonglve.html"
                    
                    print(f"\n[{idx}/{len(attractions)}] 爬取景点: {attraction_name}")
                    print(f"URL: {attraction_url}")
                    
                    # 获取景点详情页
                    html = self._request_page(attraction_url)
                    if not html:
                        print("获取页面内容失败，跳过此景点")
                        continue
                    
                    # 解析景点数据
                    attraction_data = Utils.parse_attraction_page(html, city_name)
                    
                    # 保存到Markdown文件
                    self.writer.save_attraction(city_name, attraction_data)
                    print(f"成功保存景点: {attraction_name}")
                    
                    # 随机休眠避免被封
                    Utils.random_sleep()
                    
                except Exception as e:
                    print(f"爬取景点 {attraction.get('name', '未知')} 失败: {str(e)}")
                    continue
    
    def crawl_hotels(self, city_name, city_id, max_pages=2):
        """爬取指定城市的酒店数据"""
        print(f"\n开始爬取 {city_name} 的酒店数据...")
        
        for page in range(1, max_pages + 1):
            print(f"\n正在获取第 {page} 页酒店列表...")
            
            # 获取酒店列表
            hotels = self._get_hotel_list(city_id, page)
            if not hotels:
                print(f"第 {page} 页没有获取到酒店数据，可能已达末尾")
                break
            
            for idx, hotel in enumerate(hotels, 1):
                try:
                    hotel_id = hotel['id']
                    hotel_name = hotel.get('name', '未知酒店')
                    hotel_url = f"https://www.mafengwo.cn/hotel/{hotel_id}.html"
                    
                    print(f"\n[{idx}/{len(hotels)}] 爬取酒店: {hotel_name}")
                    print(f"URL: {hotel_url}")
                    
                    # 获取酒店详情页
                    html = self._request_page(hotel_url)
                    if not html:
                        print("获取页面内容失败，跳过此酒店")
                        continue
                    
                    # 解析酒店数据
                    hotel_data = Utils.parse_hotel_page(html, city_name)
                    
                    # 保存到Markdown文件
                    self.writer.save_hotel(city_name, hotel_data)
                    print(f"成功保存酒店: {hotel_name}")
                    
                    # 随机休眠避免被封
                    Utils.random_sleep()
                    
                except Exception as e:
                    print(f"爬取酒店 {hotel.get('name', '未知')} 失败: {str(e)}")
                    continue
    
    def _get_attraction_list(self, city_id, page=1):
        """获取景点列表API数据"""
        url = 'https://www.mafengwo.cn/ajax/router.php'
        params = {
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': city_id,
            'iTagId': 0,
            'iPage': page
        }
        
        try:
            response = self.session.post(url, data=params)
            response.raise_for_status()
            data = response.json()
            return data.get('list', [])
        except Exception as e:
            print(f"获取景点列表失败: {str(e)}")
            return []
    
    def _get_hotel_list(self, city_id, page=1):
        """获取酒店列表API数据"""
        url = 'https://www.mafengwo.cn/hotel/ajax.php'
        params = {
            'sAct': 'KMdd_StructWebAjax|GetHotelList',
            'iMddid': city_id,
            'iPage': page,
            'iRows': 20
        }
        
        try:
            response = self.session.post(url, data=params)
            response.raise_for_status()
            data = response.json()
            return data.get('list', [])
        except Exception as e:
            print(f"获取酒店列表失败: {str(e)}")
            return []
    
    def _request_page(self, url):
        """发送HTTP请求获取页面内容"""
        try:
            proxies = ProxyManager.get_request_proxies() if Config.PROXY_ENABLED else None
            response = self.session.get(url, proxies=proxies)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"请求失败: {url} 状态码: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {url} 错误: {str(e)}")
            return None
        except Exception as e:
            print(f"未知错误: {url} 错误: {str(e)}")
            return None
    
    def close(self):
        """关闭会话"""
        self.session.close()
        print("\n爬虫会话已关闭")

if __name__ == '__main__':
    print("马蜂窝新疆旅游数据爬取程序启动")
    print("=" * 50)
    
    crawler = MafengwoCrawler()
    try:
        crawler.crawl_city_data()
    except KeyboardInterrupt:
        print("\n用户中断爬虫程序")
    except Exception as e:
        print(f"\n爬虫程序异常终止: {str(e)}")
    finally:
        crawler.close()
        print("\n程序执行完毕")