import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from datetime import datetime
import re
from urllib.parse import urljoin

# إعدادات الموقع
base_url = 'https://www.allrecipes.com'
output_folder = r'C:\Users\ramon\Desktop\AllRecipesLinks'
missing_image_folder = os.path.join(output_folder, 'MissingImages')
visited_file_path = os.path.join(output_folder, 'visited.txt')
no_recipe_file_path = os.path.join(output_folder, 'noRecipe.txt')
links_folder = os.path.join(output_folder, 'CollectedLinks')
all_links_file_path = os.path.join(output_folder, 'all_links.txt')  # مسار ملف الروابط النصية

# التأكد من وجود المجلدات المطلوبة
os.makedirs(output_folder, exist_ok=True)
os.makedirs(missing_image_folder, exist_ok=True)
os.makedirs(links_folder, exist_ok=True)

def get_recipe_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting the recipe image
        image_div = soup.find('div', class_='img-placeholder')
        img_tag = image_div.find('img') if image_div else None
        if img_tag and 'data-src' in img_tag.attrs:
            image_url = img_tag['data-src']
        else:
            image_url = None
        
        # Extracting the video link
        video_tag = soup.find('video')
        video_url = video_tag['src'] if video_tag and 'src' in video_tag.attrs else None
        
        # If neither image nor video is available, return None
        if not image_url and not video_url:
            return None, True  # Return True to log in noRecipe.txt
        
        # Extracting the recipe name
        recipe_name_tag = soup.find('h1', class_='headline heading-content')
        meal_name = recipe_name_tag.text.strip() if recipe_name_tag else "N/A"
        
        # Use video URL if available, otherwise use recipe URL
        link = video_url if video_url else url
        
        # Extracting the ingredients
        ingredients = []
        ingredients_sections = soup.find('ul', class_='ingredients-section')
        if ingredients_sections:
            for item in ingredients_sections.find_all('li', class_='ingredients-item'):
                ingredient_text = item.get_text(strip=True)
                ingredients.append(ingredient_text)
        ingredients_text = "\n".join(ingredients)
        
        # Extracting the preparation steps
        preparation_steps = []
        preparation_sections = soup.find('ol', class_='instructions-section')
        if preparation_sections:
            for step in preparation_sections.find_all('li', class_='instructions-item'):
                step_text = step.get_text(strip=True)
                preparation_steps.append(step_text)
        preparation_text = "\n".join(preparation_steps)

        # Extracting additional details
        details = soup.find('div', class_='recipe-details')
        prep_time = cook_time = additional_time = total_time = "N/A"
        servings = yield_info = "N/A"
        
        if details:
            time_items = details.find_all('div', class_='recipe-details__item')
            for item in time_items:
                label = item.find('div', class_='recipe-details__label').get_text(strip=True)
                value = item.find('div', class_='recipe-details__value').get_text(strip=True)
                if label == "Prep Time:":
                    prep_time = value
                elif label == "Cook Time:":
                    cook_time = value
                elif label == "Additional Time:":
                    additional_time = value
                elif label == "Total Time:":
                    total_time = value
                elif label == "Servings:":
                    servings = int(value)
                elif label == "Yield:":
                    yield_info = value
        
        # Nutrition facts extraction (optional, if available)
        nutrition_facts = {
            "Calories": "N/A",
            "Fat": "N/A",
            "Carbs": "N/A",
            "Protein": "N/A"
        }
        nutrition_section = soup.find('section', class_='nutrition-section')
        if nutrition_section:
            nutrition_items = nutrition_section.find_all('div', class_='nutrition-item')
            for item in nutrition_items:
                label = item.find('div', class_='nutrition-label').get_text(strip=True)
                value = item.find('div', class_='nutrition-value').get_text(strip=True)
                if label in nutrition_facts:
                    nutrition_facts[label] = value

        # Collect all links from the page
        links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]

        # Check if all required elements are present
        if not meal_name or not ingredients_text or not preparation_text:
            return None, True  # Return True to log in noRecipe.txt
        
        current_time = datetime.now().isoformat()

        user_name = "Sara Rose"
        created_by = "waelkamira@gmail.com"
        user_image = "https://res.cloudinary.com/dh2xlutfu/image/upload/v1722936751/cooking/s3dndvhifburzy4fvehe.jpg"
        selected_value = "main"
        advise = "N/A"
        hearts = 0
        likes = 0
        emojis = 0
        
        recipe = {
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
            "link": link,
            "createdAt": current_time,
            "updatedAt": current_time,
            "hearts": hearts,
            "likes": likes,
            "emojis": emojis,
            "Prep Time": prep_time,
            "Cook Time": cook_time,
            "Additional Time": additional_time,
            "Total Time": total_time,
            "Servings": servings,
            "Yield": yield_info,
            "Calories": nutrition_facts.get("Calories", "N/A"),
            "Fat": nutrition_facts.get("Fat", "N/A"),
            "Carbs": nutrition_facts.get("Carbs", "N/A"),
            "Protein": nutrition_facts.get("Protein", "N/A"),
            "links": links  # Store all collected links
        }

        return recipe, False

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"404 Error: The page {url} was not found.")
            log_no_recipe(url)  # Log as noRecipe
            return None, True  # Indicate that no recipe was found
        else:
            print(f"HTTP error occurred: {http_err}")
            return None, True  # Indicate that no recipe was found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None, True  # Indicate that no recipe was found

def log_done(url):
    with open(visited_file_path, 'a', encoding='utf-8') as file:
        file.write(url + '\n')

def log_no_recipe(url):
    with open(no_recipe_file_path, 'a', encoding='utf-8') as file:
        file.write(url + '\n')

def save_links_to_file(links, url):
    base_filename = url.split('/')[-1].split('.')[0]
    base_filename = re.sub(r'[^\w\-_\. ]', '_', base_filename)  # Replace invalid characters

    counter = 1
    while True:
        output_file = os.path.join(links_folder, f"{counter}_{base_filename}_links.txt")
        if not os.path.exists(output_file):
            break
        counter += 1

    with open(output_file, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')
    print(f"Saved collected links to {output_file}")

def read_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def generate_recipes(file_path):
    urls = read_urls_from_file(file_path)
    file_count = 1
    recipes = []
    
    urls_to_process = urls[:]
    
    for url in urls_to_process:
        recipe_info, no_recipe = get_recipe_info(url)
        
        if recipe_info:
            recipes.append(recipe_info)
            if recipe_info['image']:
                save_to_csv([recipe_info], file_count, output_folder)
            else:
                save_to_csv([recipe_info], file_count, missing_image_folder)
            
            save_links_to_file(recipe_info['links'], url)
            log_done(url)  # Log the URL in the visited.txt file
            file_count += 1
        elif no_recipe:
            urls_to_process.remove(url)  # Remove the URL from the list to avoid processing again

    # تحديث ملف all_links.txt بعد معالجة جميع الروابط
    with open(all_links_file_path, 'w', encoding='utf-8') as file:
        for url in urls_to_process:
            file.write(url + '\n')

    return recipes

def save_to_csv(recipes, file_count, folder_path):
    df = pd.DataFrame(recipes)
    file_path = os.path.join(folder_path, f'recipes_{file_count}.csv')
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Saved recipes to {file_path}")

# استبدال هذا الجزء بملف الروابط النصية الخاص بك
generate_recipes(all_links_file_path)
