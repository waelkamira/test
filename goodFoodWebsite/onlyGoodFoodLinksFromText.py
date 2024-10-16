import os

# مسار ملف النص
input_file = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks\all_links.txt'
output_file = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks\bbcgoodfood_links.txt'

# قراءة الروابط من الملف واستخراج الروابط التي تحتوي على "bbcgoodfood"
with open(input_file, 'r') as file:
    all_links = [line.strip() for line in file if 'www.bbcgoodfood' in line]

# كتابة الروابط المستخرجة إلى ملف جديد
with open(output_file, 'w') as file:
    for link in all_links:
        file.write(link + '\n')

print(f"Extracted {len(all_links)} links containing 'bbcgoodfood' to {output_file}")
