import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from datetime import datetime

def get_recipe_info(url, page_index):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        topper_title = soup.find('div', class_='topper-title')
        if not topper_title:
            return None, False  # لم يتم العثور على وصفة

        meal_name = topper_title.h1.text.strip() if topper_title.h1 else None
        if not meal_name:
            return None, False  # لم يتم العثور على وصفة

        article_img_div = soup.find('div', class_='entry-media')
        image_tag = article_img_div.img if article_img_div else None
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
        if not image_url:
            return None, False  # لم يتم العثور على وصفة

        ingredients_section = soup.find('div', class_='ingredients-area')
        ingredients = ingredients_section.get_text(separator="\n").strip() if ingredients_section else ""
        if not ingredients:
            return None, False  # لم يتم العثور على وصفة

        preparation_section = soup.find('div', class_='preparation-area')
        if preparation_section:
            preparation_steps = "\n".join([li.text.strip() for li in preparation_section.find_all('li')])
        else:
            preparation_section = soup.find('div', itemprop='instructions')
            preparation_steps = "\n".join([p.text.strip() for p in preparation_section.find_all('p')]) if preparation_section else ""

        if not preparation_steps:
            return None, False  # لم يتم العثور على وصفة

        video_section = soup.find('video', class_='jw-video')
        video_url = video_section['src'] if video_section and 'src' in video_section.attrs else None

        current_time = datetime.now().isoformat()

        user_name = "بهيجة أشرق لبن"
        created_by = "waelkamira@gmail.com"
        user_image = "https://res.cloudinary.com/dh2xlutfu/image/upload/v1718716951/cooking/bahiga_cmzcf4.png"
        selected_value = "وجبة رئيسية"
        advise = ""
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
            "advise": advise,
            "link": video_url,
            "createdAt": current_time,
            "updatedAt": current_time,
            "hearts": hearts,
            "likes": likes,
            "emojis": emojis
        }, True  # تم العثور على وصفة

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None, False  # لم يتم العثور على وصفة

def save_to_excel(recipe, page_index):
    # مسار المجلد على سطح المكتب
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'SayidatyLinks')
    
    # إنشاء المجلد إذا لم يكن موجودًا
    os.makedirs(desktop_path, exist_ok=True)

    # استخدام رقم الصفحة كاسم الملف
    xlsx_file_path = os.path.join(desktop_path, f"recipe_{page_index}.xlsx")
    
    df = pd.DataFrame([recipe])
    df.to_excel(xlsx_file_path, index=False)  # تم إزالة الوسيط encoding
    
    print(f"Recipe saved to {xlsx_file_path}")

def process_recipes(start_index=12670):
    # مسار المجلد على سطح المكتب
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'SayidatyLinks')

    # إنشاء المجلدات إذا لم تكن موجودة
    visited_path = os.path.join(desktop_path, 'visited')
    no_recipes_path = os.path.join(desktop_path, 'noRecipes')
    os.makedirs(visited_path, exist_ok=True)
    os.makedirs(no_recipes_path, exist_ok=True)
    
    index = start_index
    while True:
        url = f"https://kitchen.sayidaty.net/node/{index}/%D8%B7%D8%B1%D9%8A%D9%82%D8%A9-%D8%B9%D9%85%D9%84-%D8%A7%D9%84%D8%AA%D8%B1%D9%85%D8%B3-%D8%A7%D9%84%D8%B3%D8%B1%D9%8A%D8%B9/%D8%A7%D9%84%D9%85%D9%82%D8%A8%D9%84%D8%A7%D8%AA/%D9%88%D8%B5%D9%81%D8%A7%D8%AA"
        print(f"Processing {url}...")

        recipe_info, found_recipe = get_recipe_info(url, index)
        if found_recipe and recipe_info:
            save_to_excel(recipe_info, index)
            # حفظ الرابط الذي وجد فيه وصفة في ملف نصي منفصل
            visited_file_path = os.path.join(visited_path, f"{index}.txt")
            with open(visited_file_path, 'w', encoding='utf-8') as visited_file:
                visited_file.write(url)
        else:
            # حفظ الرابط الذي لم يجد فيه وصفة في ملف نصي منفصل
            no_recipe_file_path = os.path.join(no_recipes_path, f"{index}.txt")
            with open(no_recipe_file_path, 'w', encoding='utf-8') as no_recipe_file:
                no_recipe_file.write(url)

        # زيادة العداد للانتقال إلى الرابط التالي
        index += 1

process_recipes()
