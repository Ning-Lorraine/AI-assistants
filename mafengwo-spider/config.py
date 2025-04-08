# 爬虫配置
class Config:
    # 请求头
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.mafengwo.cn/'
    }
    
    # 目标城市
    TARGET_CITIES = {
        '乌鲁木齐': '10218',
        '伊犁': '11471',
        '喀什': '164841'
    }
    
    # 请求间隔(秒)
    REQUEST_INTERVAL = 3
    
    # 代理设置
    PROXY_ENABLED = False
    PROXY_POOL_URL = 'http://proxy-pool-url.com/get'