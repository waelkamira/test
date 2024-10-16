import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import re

# إعدادات الموقع
base_url = 'https://www.foodnetwork.com'
recipe_url_prefix = 'https://www.foodnetwork.com/recipes'
output_folder = r'C:\Users\ramon\Desktop\FoodNetworkLinks'

visited_links = set()
new_links = set()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def extract_links(url):
    """جلب الروابط من صفحة معينة."""
    links = set()
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(base_url, href)
            # التحقق من أن الرابط يبدأ بـ recipe_url_prefix
            if re.match(f"^{recipe_url_prefix}", full_url) and full_url not in visited_links:
                visited_links.add(full_url)
                links.add(full_url)
        print(f"Extracted {len(links)} recipe links from: {url}")

        # حفظ الروابط في ملف نصي منفصل لكل صفحة
        page_name = os.path.basename(urlparse(url).path) or 'index'
        save_links_to_file(links, os.path.join(output_folder, f"{page_name}_recipe_links.txt"))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return links

def read_links_from_file(filename):
    """قراءة الروابط من ملف نصي."""
    links = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                link = line.strip()
                if link:
                    links.add(link)
    return links

def save_links_to_file(links, filename):
    """حفظ الروابط في ملف نصي."""
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')
    print(f"Saved {len(links)} links to {filename}")

# قراءة الروابط من الملف النصي
input_file = os.path.join(output_folder, 'all_links.txt')
visited_links.update(read_links_from_file(input_file))

# جلب روابط جديدة من كل رابط تم قراءته
urls_to_process = list(visited_links)  # إنشاء نسخة من الروابط للتكرار عليها
for url in urls_to_process:
    new_links.update(extract_links(url))
    time.sleep(1 + len(new_links) % 3)  # تأخير ديناميكي بين 1 إلى 3 ثوانٍ بين الطلبات

# حفظ الروابط الجديدة في الملف النصي الرئيسي
output_file = os.path.join(output_folder, 'all_links.txt')
save_links_to_file(visited_links.union(new_links), output_file)

print(f"Total recipe links collected: {len(visited_links)}")
print(f"Links saved in folder: {output_folder}")
