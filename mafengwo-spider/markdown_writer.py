import os
from datetime import datetime

class MarkdownWriter:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_attraction(self, city_name, data):
        filename = f"{self.output_dir}/{city_name}_景点.md"
        mode = 'a' if os.path.exists(filename) else 'w'
        
        with open(filename, mode, encoding='utf-8') as f:
            if mode == 'w':
                f.write(f"# {city_name}景点信息\n\n")
                f.write(f"> 最后更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## {data['name']}\n\n")
            f.write(f"- **位置**: {data['location']}\n")
            f.write(f"- **地址**: {data['address']}\n")
            f.write(f"- **门票价格**: {data['ticket_price'] or '暂无信息'}\n")
            f.write(f"- **学生票价**: {data['student_price'] or '暂无信息'}\n")
            f.write(f"- **开放时间**: {data['open_time'] or '暂无信息'}\n")
            f.write(f"- **评分**: {data['rating'] or '暂无评分'}\n")
            
            if data['image_url']:
                f.write(f"\n![{data['name']}图片]({data['image_url']})\n")
            
            if data['description']:
                f.write(f"\n**景点介绍**:\n\n{data['description']}\n")
            
            f.write("\n---\n\n")
    
    def save_hotel(self, city_name, data):
        filename = f"{self.output_dir}/{city_name}_酒店.md"
        mode = 'a' if os.path.exists(filename) else 'w'
        
        with open(filename, mode, encoding='utf-8') as f:
            if mode == 'w':
                f.write(f"# {city_name}酒店信息\n\n")
                f.write(f"> 最后更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## {data['name']}\n\n")
            f.write(f"- **位置**: {data['location']}\n")
            f.write(f"- **地址**: {data['address']}\n")
            f.write(f"- **价格范围**: {data['price_range'] or '暂无信息'}\n")
            f.write(f"- **评分**: {data['rating'] or '暂无评分'}\n")
            
            if data['facilities']:
                f.write(f"- **设施**: {data['facilities']}\n")
            
            if data['reviews']:
                f.write("\n**用户评价**:\n\n")
                reviews = data['reviews'].split(' | ')
                for i, review in enumerate(reviews, 1):
                    f.write(f"{i}. {review}\n")
            
            f.write("\n---\n\n")