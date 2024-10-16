import os
import json
import shutil

source_folder = r'Q:\وصفات عربية واجنبية\not found'
destination_folder = r'Q:\وصفات عربية واجنبية\allrecipes'
output_file = os.path.join(destination_folder, 'allrecipes_links.txt')

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# فتح الملف النصي لكتابة الروابط
with open(output_file, 'w', encoding='utf-8') as out_file:
    for filename in os.listdir(source_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(source_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if 'url' in data and 'allrecipes' in data['url']:
                        # كتابة الرابط في الملف النصي
                        out_file.write(data['url'] + '\n')
                        # نقل الملف إلى المجلد الوجهة
                        shutil.move(file_path, os.path.join(destination_folder, filename))
                        print(f"Moved: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

print("Finished moving files and extracting links.")
