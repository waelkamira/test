

import os
import json

# المجلد الذي يحتوي على ملفات JSON
input_folder = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks'
output_file = os.path.join(input_folder, 'merged_links.json')
all_links = set()  # مجموعة لتخزين الروابط والتحقق من عدم التكرار

# قراءة جميع ملفات JSON في المجلد
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, 'r') as file:
            links = json.load(file)
            all_links.update(links)

# حفظ الروابط في ملف JSON واحد بعد إزالة التكرارات
with open(output_file, 'w') as output:
    json.dump(list(all_links), output, indent=4)

print(f"Total unique links collected: {len(all_links)}")
print(f"Merged links saved to: {output_file}")
