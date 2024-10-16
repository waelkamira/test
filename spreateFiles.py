import os
import json
import shutil

source_folder = r'Q:\وصفات عربية واجنبية\not found'
destination_folder = r'Q:\وصفات عربية واجنبية\epicurious'

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for filename in os.listdir(source_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(source_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if 'url' in data and 'epicurious' in data['url']:
                    shutil.move(file_path, os.path.join(destination_folder, filename))
                    print(f"Moved: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Finished moving files.")
