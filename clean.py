import re

# فتح الملف النصي وقراءته
with open(r'C:\Users\ramon\Desktop\BBCGoodFoodLinks\all_links.txt', 'r') as file:
    text = file.read()

# تعريف النمط للروابط
pattern = r'https?://www\.bbcgoodfood\.com/recipes/[\w-]+'

# استخدام التعبيرات النمطية لاستخراج الروابط
links = re.findall(pattern, text)

# حفظ الروابط في ملف نصي جديد
with open('filtered_links.txt', 'w') as file:
    for link in links:
        file.write(link + '\n')

print(f'تم استخراج {len(links)} رابطًا وحفظها في filtered_links.txt')
