import os
import json
import requests
from bs4 import BeautifulSoup

# المجلدات
input_folder = r"Q:\وصفات عربية واجنبية\not found"
output_folder = os.path.join(os.path.expanduser("~"), 'Desktop', 'done')

# التأكد من وجود مجلد الإخراج
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# دالة لتحميل الصفحة واستخراج روابط الوسائط
def extract_media_urls(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # استخراج رابط الصورة
        image_url = None
        primary_image_div = soup.find("div", class_="primary-image__media")
        if primary_image_div:
            img_tag = primary_image_div.find("img")
            if img_tag and img_tag.has_attr('src'):
                image_url = img_tag['src']

        # استخراج رابط الفيديو
        video_url = None
        video_tag = soup.find("video", class_="jw-video jw-reset")
        if video_tag and video_tag.has_attr('src') and not video_tag['src'].startswith('blob:'):
            video_url = video_tag['src']

        return {
            "image_url": image_url,
            "video_url": video_url
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# معالجة الملفات JSON
def process_json_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    url = data.get('url')
                    if not url:
                        print(f"No URL found in {filename}")
                        continue

                    media_urls = extract_media_urls(url)
                    if media_urls:
                        # Update data with extracted URLs if found
                        if media_urls.get('image_url') or media_urls.get('video_url'):
                            data.update(media_urls)

                            # Save updated data to a new file
                            new_file_path = os.path.join(output_folder, filename)
                            with open(new_file_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4, ensure_ascii=False)
                            print(f"Updated data saved to {new_file_path}")
                        else:
                            print(f"No image or video URL found for {url}")
                    else:
                        print(f"Failed to extract media URLs from {url}")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error processing {filename}: {e}")

# Set input and output folder paths
input_folder = r"Q:\وصفات عربية واجنبية\not found"
output_folder = os.path.join(os.path.expanduser("~"), 'Desktop', "Modified_Recipes")

# Process JSON files
process_json_files(input_folder, output_folder)

print("Processing complete.")
