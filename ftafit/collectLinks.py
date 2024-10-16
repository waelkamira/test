import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse

# إعدادات الموقع
base_url = 'https://www.fatafeat.com'
output_folder = r'C:\Users\ramon\Desktop\FatafeatLinks'

visited_links = set()
new_links = set()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def extract_links(url):
    """جلب الروابط من صفحة معينة."""
    links = set()
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                full_url = urljoin(base_url, href)
                if href and full_url not in visited_links and 'https://www.fatafeat.com/recipe/' in full_url:
                    visited_links.add(full_url)
                    links.add(full_url)
            print(f"Extracted {len(links)} links from: {url}")

            # حفظ الروابط في ملف نصي منفصل لكل صفحة
            page_name = urlparse(url).path.replace('/', '_').strip('_')
            save_links_to_file(links, os.path.join(output_folder, f"{page_name}_links.txt"))
        else:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return links

def save_links_to_file(links, filename):
    """حفظ الروابط في ملف نصي."""
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')
    print(f"Saved {len(links)} links to {filename}")

# بدء الزحف من الملف النصي
with open(os.path.join(output_folder, 'recipes.txt'), 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file]

for url in urls:
    visited_links.add(url)
    new_links.update(extract_links(url))
    time.sleep(1)  # تأخير لمدة 1 ثانية بين الطلبات

# جلب روابط جديدة من كل رابط تم جمعه
urls_to_process = list(new_links)  # إنشاء نسخة من الروابط للتكرار عليها
for url in urls_to_process:
    new_links.update(extract_links(url))
    time.sleep(1)  # تأخير لمدة 1 ثانية بين الطلبات

# حفظ جميع الروابط المجمعة في الملف النصي
output_file = os.path.join(output_folder, 'all_links.txt')
save_links_to_file(visited_links, output_file)

print(f"Total links collected: {len(visited_links)}")
print(f"Links saved in folder: {output_folder}")
