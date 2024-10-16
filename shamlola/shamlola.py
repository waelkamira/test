import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid
from datetime import datetime

# Function to get recipe information from a recipe URL
def get_recipe_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Ensure content is decoded as UTF-8
        content = response.content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        # Extract recipe name
        topper_title = soup.find('div', class_='topper-title')
        meal_name = topper_title.h1.text.strip() if topper_title and topper_title.h1 else None

        # Extract recipe image URL
        article_img_div = soup.find('div', class_='article-item-img')
        image_tag = article_img_div.img if article_img_div else None
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

        if not meal_name or not image_url:
            return None

        # Extract ingredients
        ingredients_section = soup.find('div', class_='ingredients-area')
        ingredients = ingredients_section.get_text(separator="\n").strip() if ingredients_section else ""

        # Extract preparation steps
        preparation_section = soup.find('div', class_='preparation-area') or soup.find('div', itemprop='instructions')
        preparation_steps = "\n".join([p.text.strip() for p in preparation_section.find_all('p')]) if preparation_section else ""

        if not ingredients or not preparation_steps:
            return None

        # Additional information
        video_url = None

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
            "ingredients": ingredients,
            "theWay": preparation_steps,
            "advise": advise,
            "link": video_url,
            "createdAt": current_time,
            "updatedAt": current_time,
            "hearts": hearts,
            "likes": likes,
            "emojis": emojis
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Function to generate recipes from a base URL and save them in CSV files
def generate_recipes(base_url, batch_size):
    print(f"Fetching recipes from {base_url}")
    recipes = []
    file_count = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    url = base_url
    while True:
        try:
            print(f"Fetching page: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            content = response.content.decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')

            # Extract recipe links
            recipe_links = [a['href'] for a in soup.find_all('a', class_='recipe-link', href=True)]

            if not recipe_links:
                print("No more recipes found.")
                break

            for link in recipe_links:
                full_link = "https://www.shamlola.com" + link
                print(f"Fetching recipe: {full_link}")
                recipe_info = get_recipe_info(full_link)
                if recipe_info:
                    recipes.append(recipe_info)

                    if len(recipes) >= batch_size:
                        save_to_csv(recipes, file_count)
                        recipes = []
                        file_count += 1

            # Check for pagination
            load_more_button = soup.find('button', {'class': 'load-more'})
            if load_more_button and not load_more_button.get('disabled'):
                url = base_url + f"?page={file_count + 1}"
            else:
                print("No more pages to load.")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {url}: {e}")
            break

    if recipes:
        save_to_csv(recipes, file_count)

# Function to save recipes to a CSV file
def save_to_csv(recipes, file_count):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    csv_file_path = os.path.join(desktop_path, f"recipes_{file_count}.csv")

    df = pd.DataFrame(recipes)
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

    print(f"Recipes saved to {csv_file_path}")

# Base URL of the website
base_url = "https://www.shamlola.com/recipes/"

# Start the recipe generation process
generate_recipes(base_url, 10)
