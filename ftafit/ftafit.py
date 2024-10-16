import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time

# إعدادات الموقع
base_url = 'https://www.fatafeat.com'
output_folder = r'C:\Users\ramon\Desktop\FatafeatLinks'

visited_links = set()
new_links = set()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_recipe_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting the recipe image
        image_div = soup.find('div', class_='recipe-img-api')
        image_url = image_div['style'].split("url('")[1].split("')")[0] if image_div else None
        
        # Extracting the recipe name
        recipe_name_tag = soup.find('h1', class_='recipe-page-title')
        meal_name = recipe_name_tag.text.strip() if recipe_name_tag else None
        
        # Extracting the ingredients
        ingredients = []
        ingredients_sections = soup.find_all('div', class_='ingredients')
        for section in ingredients_sections:
            amount_tag = section.find('p', class_='firsttext')
            name_tag = section.find('p', class_='secondtext')
            if amount_tag and name_tag:
                ingredient = f"{amount_tag.text.strip()} {name_tag.text.strip()}"
                ingredients.append(ingredient)
        ingredients_text = "\n".join(ingredients)
        
        # Extracting the preparation steps
        preparation_steps = []
        preparation_sections = soup.find_all('div', class_='row px-3 mx-3')
        for section in preparation_sections:
            step_tag = section.find('p', class_='counter-text')
            if step_tag:
                step = step_tag.text.strip()
                preparation_steps.append(step)
        preparation_text = "\n".join(preparation_steps)

        # Check if all required elements are present
        if not meal_name or not image_url or not ingredients_text or not preparation_text:
            return None
        
        current_time = datetime.now().isoformat()

        user_name = "بهيجة أشرق لبن"
        created_by = "waelkamira@gmail.com"
        user_image = "https://res.cloudinary.com/dh2xlutfu/image/upload/v1718716951/cooking/bahiga_cmzcf4.png"
        selected_value = "N/A"
        advise = "N/A"
        hearts = 0
        likes = 0
        emojis = 0
        
        return {
            "id": str(uuid.uuid4()),
            "userName": user_name,
            "createdBy": created_by,
            "userImage": user_image,
            "mealName": meal_name,
            "selectedValue": selected_value,
            "image": image_url,
            "ingredients": ingredients_text,
            "theWay": preparation_text,
            "advise": advise,
            "link": url,
            "createdAt": current_time,
            "updatedAt": current_time,
            "hearts": hearts,
            "likes": likes,
            "emojis": emojis
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

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

def generate_recipes(base_url, start, end, batch_size):
    recipes = []
    file_count = 1
    counter = start
    while counter <= end:
        url = base_url.format(counter)
        recipe_info = get_recipe_info(url)
        if recipe_info:
            recipes.append(recipe_info)
            if len(recipes) >= batch_size:
                save_to_csv(recipes, file_count)
                recipes = []
                file_count += 1
        new_links.update(extract_links(url))  # جلب الروابط من الصفحة الحالية
        counter += 1
        time.sleep(1)  # تأخير لمدة 1 ثانية بين الطلبات
    if recipes:
        save_to_csv(recipes, file_count)

def save_to_csv(recipes, file_count):
    csv_file_path = os.path.join(output_folder, f"recipes_{file_count}.csv")
    df = pd.DataFrame(recipes)
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    print(f"Recipes saved to {csv_file_path}")

start_url = "https://www.fatafeat.com/recipe/998/طريقة عمل"

# بدء الزحف من الصفحة المحددة
visited_links.add(start_url)
new_links.update(extract_links(start_url))

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

base_url = "https://www.fatafeat.com/recipe/{}/طريقة عمل"

generate_recipes(base_url, 20000, 100000, 100)  # Example range from 998 to 20000 with batch size of 100
