import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urlparse

base_url = 'https://www.allrecipes.com'
recipe_url_prefix = 'https://www.allrecipes.com/recipe/'
output_folder = r'C:\Users\ramon\Desktop\AllRecipesLinks'

visited_links = set()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def extract_links(url):
    """جلب الروابط من صفحة معينة."""
    new_links = set()
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                # التأكد من أن الرابط يحتوي على recipe_url_prefix وليس موجودًا في visited_links
                if href and href.startswith(recipe_url_prefix) and href not in visited_links:
                    visited_links.add(href)
                    new_links.add(href)
            print(f"Extracted {len(new_links)} links from: {url}")
        else:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return new_links

def save_links_to_file(links, url):
    """حفظ الروابط في ملف نصي خاص بكل صفحة."""
    # إنشاء اسم ملف يعتمد على اسم الصفحة
    parsed_url = urlparse(url)
    file_name = parsed_url.path.replace('/', '_').strip('_')
    output_file = os.path.join(output_folder, f'{file_name}.txt')
    with open(output_file, 'w') as file:
        for link in links:
            file.write(link + '\n')
    print(f"Saved {len(links)} links to {output_file}")

# قراءة الروابط من الملفات النصية وزيارة كل رابط لاستخراج روابط جديدة
def extract_links_from_saved_files():
    files = [f for f in os.listdir(output_folder) if f.startswith('all_links_') and f.endswith('.txt')]
    for file in files:
        file_path = os.path.join(output_folder, file)
        with open(file_path, 'r') as f:
            for line in f:
                link = line.strip()
                if link and link not in visited_links:
                    visited_links.add(link)
                    # زيارة كل رابط واستخراج روابط جديدة منه
                    new_links = extract_links(link)
                    # حفظ الروابط المستخرجة في ملف نصي خاص
                    save_links_to_file(new_links, link)
                    # تأخير بين الطلبات لتجنب التحميل الزائد على الخادم
                    time.sleep(1)  # تأخير لمدة 1 ثانية بين الطلبات

# بدء الزحف من الروابط المخزنة في الملفات النصية
extract_links_from_saved_files()

print(f"Total unique links visited: {len(visited_links)}")
print(f"Links saved in folder: {output_folder}")
