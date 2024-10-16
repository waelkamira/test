import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import uuid
from datetime import datetime



def safe_header(header_value):
    return header_value.encode('ascii', 'ignore').decode('ascii')

def get_recipe_links(base_url, categories):
    recipe_links = set()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # لتشغيل المتصفح في الخلفية
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # انتظار التحميل

    try:
        for category in categories:
            url = f"{base_url}/{category}/"
            driver.get(url)
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # التمرير إلى أسفل الصفحة
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # الانتظار لتحميل المحتوى الجديد

                # الحصول على الروابط الحالية
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link.get('href')
                    if href and '/%d9%' in href and all(c not in href for c in categories):
                        recipe_links.add(href)

                # التحقق مما إذا كانت الصفحة قد وصلت إلى النهاية
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

    finally:
        driver.quit()

    return list(recipe_links)

def get_recipe_info(url):
    headers = {
        "User-Agent": safe_header("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML، مثل Gecko) Chrome/91.0.4472.124 Safari/537.36"),
        "Accept-Charset": safe_header("utf-8")
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        meal_name = soup.find('h1', class_='entry-title').text.strip() if soup.find('h1', class_='entry-title') else "Unknown Recipe"
        
        image_tag = soup.find('div', class_='post-thumbnail-inner').img if soup.find('div', class_='post-thumbnail-inner') else None
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else "https://via.placeholder.com/150"
        
        content_section = soup.find('div', class_='entry-content single-content')
        
        ingredients = ""
        if content_section:
            ingredients_list = []

            keywords = ["مقادير", "المقادير", "المكونات", "مكونات"]
            spice_keywords = ["توابل", "التوابل"]

            for keyword in keywords:
                keyword_tag = content_section.find(text=lambda text: text and keyword in text)
                if keyword_tag:
                    ul_tag = keyword_tag.find_next('ul')
                    if ul_tag:
                        ingredients_list.extend([f"🧀 {li.text.strip()}" for li in ul_tag.find_all('li')])
                        break

            for spice_keyword in spice_keywords:
                spice_keyword_tag = content_section.find(text=lambda text: text and spice_keyword in text)
                if spice_keyword_tag:
                    ul_tag = spice_keyword_tag.find_next('ul')
                    if ul_tag:
                        ingredients_list.extend([f"🧀 {li.text.strip()}" for li in ul_tag.find_all('li')])
                        break

            ingredients = "\n".join(ingredients_list)

        preparation_steps = ""
        if content_section:
            first_ol = content_section.find('ol')
            preparation_steps = "\n".join([f"🧀 {li.text.strip()}" for li in first_ol.find_all('li')]) if first_ol else "No preparation steps available."
        
        advice = ""
        if content_section:
            ol_tags = content_section.find_all('ol', limit=2)
            if len(ol_tags) > 1:
                advice = "\n".join([f"🧀 {li.text.strip()}" for li in ol_tags[1].find_all('li')])

        if not all([meal_name, ingredients, preparation_steps, image_url]):
            return None
        
        current_time = datetime.now().isoformat()

        user_name = "بهيجة أشرق لبن"
        created_by = "waelkamira@gmail.com"
        user_image = "https://res.cloudinary.com/dh2xlutfu/image/upload/v1718716951/cooking/bahiga_cmzcf4.png"
        selected_value = "وجبة رئيسية"
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
            "ingredients": ingredients,
            "theWay": preparation_steps,
            "advise": advice,
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

def generate_recipes(base_url, categories, batch_size=1000):
    recipe_links = get_recipe_links(base_url, categories)
    recipes = []
    file_count = 1
    
    for url in recipe_links:
        recipe_info = get_recipe_info(url)
        if recipe_info:
            recipes.append(recipe_info)
            
            if len(recipes) >= batch_size:
                save_to_csv(recipes, file_count)
                recipes = []
                file_count += 1
                
    if recipes:
        save_to_csv(recipes, file_count)

def save_to_csv(recipes, file_count):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    csv_file_path = os.path.join(desktop_path, f"recipesways_{file_count}.csv")
    
    df = pd.DataFrame(recipes)
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
    
    print(f"Recipes saved to {csv_file_path}")

base_url = "https://cooking-ways.com"
categories = ["أطباق-رئيسية", "مقبلات", "معجنات", "شوربات", "حلويات", "مشروبات"]

generate_recipes(base_url, categories, 1000)
