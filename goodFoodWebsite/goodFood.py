import requests
from bs4 import BeautifulSoup
import csv
import uuid
import os
import re
from urllib.parse import urljoin

# مسار ملفات النصوص
input_file = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks\all_links.txt'
output_folder = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks'
missing_image_folder = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks\MissingImages'
visited_file_path = os.path.join(output_folder, 'visited.txt')
links_folder = os.path.join(output_folder, 'CollectedLinks')

# التأكد من وجود المجلدات المطلوبة
if not os.path.exists(missing_image_folder):
    os.makedirs(missing_image_folder)

if not os.path.exists(links_folder):
    os.makedirs(links_folder)

# قراءة ملف النص
with open(input_file, 'r') as file:
    recipe_links = [line.strip().strip('"') for line in file if line.strip()]

# دالة لجلب الوصفة من رابط معين
def fetch_recipe(url, base_url='https://www.bbcgoodfood.com'):
    try:
        # التأكد من أن الرابط يحتوي على "bbcgoodfood"
        if 'bbcgoodfood' not in url:
            print(f"Skipping URL (not a BBC Good Food link): {url}")
            return None
        
        print(f"Fetching recipe from URL: {url}")
        
        # Ensure the URL is absolute
        full_url = url if url.startswith('http') else urljoin(base_url, url)
        
        response = requests.get(full_url)
        if response.status_code != 200:
            print(f"Failed to fetch {full_url}: Status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'lxml')

        # استخراج اسم الوصفة
        title_tag = soup.find('h1', class_='heading-1')
        title = title_tag.text.strip() if title_tag else None
        if not title:
            return None

        # محاولة استخراج صورة الوصفة باستخدام الارتفاع الأول
        image_tag = soup.find('img', class_='image__img', height='504.848')
        if not image_tag:
            # إذا لم يتم العثور على صورة، المحاولة باستخدام الارتفاع الثاني
            image_tag = soup.find('img', class_='image__img', height='399.52000000000004')
        
        image_url = image_tag['src'] if image_tag else None

        # استخراج المقادير
        ingredients_section = soup.find('section', class_='recipe__ingredients')
        ingredients = []
        if ingredients_section:
            for item in ingredients_section.find_all('li', class_='list-item'):
                ingredients.append(item.text.strip())

        # استخراج طريقة التحضير
        method_section = soup.find('section', class_='recipe__method-steps')
        method = []
        if method_section:
            for step in method_section.find_all('li', class_='list-item'):
                step_text = step.find('div', class_='editor-content').text.strip()
                method.append(step_text)

        # استخراج معلومات التغذية
        nutrition_table = soup.find('table', class_='key-value-blocks')
        nutrition_info = {}
        if nutrition_table:
            for row in nutrition_table.find_all('tr', class_='key-value-blocks__item'):
                key = row.find('td', class_='key-value-blocks__key').text.strip()
                value = row.find('td', class_='key-value-blocks__value').text.strip()
                nutrition_info[key] = value

        # جمع جميع الروابط الموجودة في الصفحة
        links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
        
        # بناء القاموس للنتائج
        recipe = {
            'mealName': title,
            'image': image_url,
            'ingredients': "\n".join(ingredients),
            'theWay': "\n".join(method),
            'link': full_url,
            'nutrition': nutrition_info,  # إضافة معلومات التغذية هنا
            'links': links  # إضافة جميع الروابط
        }
        
        return recipe
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# بيانات ثابتة لكل وصفة
fixed_data = {
    "userName": "Sara Rose",
    "createdBy": "waelkamira@gmail.com",
    "userImage": "https://res.cloudinary.com/dh2xlutfu/image/upload/v1722936751/cooking/s3dndvhifburzy4fvehe.jpg",
    "selectedValue": "main",
    "advise": "",
    "createdAt": "2024-07-13T18:02:53.313Z",
    "updatedAt": "2024-07-13T18:02:53.313Z",
    "hearts": 0,
    "likes": 0,
    "emojis": 0,
}

# دالة لحفظ الوصفات في ملف CSV
def save_recipe_to_csv(recipe, folder, batch_num):
    output_file = os.path.join(folder, f'recipe_{batch_num}.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "userName", "createdBy", "userImage", "mealName", "selectedValue", "image", "ingredients", "theWay", "advise", "link", "createdAt", "updatedAt", "hearts", "likes", "emojis",
                      "kcal", "fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        row = {
            "id": str(uuid.uuid4()),
            "userName": fixed_data["userName"],
            "createdBy": fixed_data["createdBy"],
            "userImage": fixed_data["userImage"],
            "mealName": recipe["mealName"],
            "selectedValue": fixed_data["selectedValue"],
            "image": recipe["image"] if recipe["image"] else 'No image found',
            "ingredients": recipe["ingredients"],
            "theWay": recipe["theWay"],
            "advise": fixed_data["advise"],
            "link": recipe["link"],
            "createdAt": fixed_data["createdAt"],
            "updatedAt": fixed_data["updatedAt"],
            "hearts": fixed_data["hearts"],
            "likes": fixed_data["likes"],
            "emojis": fixed_data["emojis"],
            "kcal": recipe["nutrition"].get("kcal", ""),
            "fat": recipe["nutrition"].get("fat", ""),
            "saturates": recipe["nutrition"].get("saturates", ""),
            "carbs": recipe["nutrition"].get("carbs", ""),
            "sugars": recipe["nutrition"].get("sugars", ""),
            "fibre": recipe["nutrition"].get("fibre", ""),
            "protein": recipe["nutrition"].get("protein", ""),
            "salt": recipe["nutrition"].get("salt", ""),
        }
        writer.writerow(row)
    print(f"Saved recipe to {output_file}")

# دالة لحفظ الروابط التي تم جمعها في ملف نصي مع إضافة أرقام تسلسلية
def save_links_to_file(links, url, folder):
    # استخراج اسم الصفحة وتغيير الحروف غير الصالحة
    base_filename = url.split('/')[-1].split('.')[0]
    base_filename = re.sub(r'[^\w\-_\. ]', '_', base_filename)  # استبدال الحروف غير الصالحة

    # إيجاد رقم تسلسلي متاح للملف
    counter = 1
    while True:
        output_file = os.path.join(folder, f"{counter}_{base_filename}_links.txt")
        if not os.path.exists(output_file):
            break
        counter += 1

    # حفظ الروابط في الملف النصي
    with open(output_file, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')
    print(f"Saved collected links to {output_file}")

# جلب وحفظ الوصفات والروابط مباشرة
batch_num = 1
for link in recipe_links:
    recipe = fetch_recipe(link)
    
    # تسجيل الرابط في ملف visited.txt
    with open(visited_file_path, 'a', encoding='utf-8') as visited_file:
        visited_file.write(link + "\n")
    
    if recipe:
        if recipe['image']:
            save_recipe_to_csv(recipe, output_folder, batch_num)
        else:
            save_recipe_to_csv(recipe, missing_image_folder, batch_num)
        
        # حفظ الروابط التي تم جمعها في ملف
        save_links_to_file(recipe['links'], link, links_folder)
        
        batch_num += 1
