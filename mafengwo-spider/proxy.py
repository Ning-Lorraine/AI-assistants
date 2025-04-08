import requests
from config import Config
import time

class ProxyManager:
    @staticmethod
    def get_proxy():
        if not Config.PROXY_ENABLED:
            return None
        
        try:
            response = requests.get(Config.PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text.strip()
        except Exception as e:
            print(f"获取代理失败: {e}")
            return None
    
    @staticmethod
    def get_request_proxies():
        proxy = ProxyManager.get_proxy()
        if proxy:
            return {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}'
            }
        return None