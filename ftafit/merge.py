import os

# المجلد الذي يحتوي على ملفات النصوص
input_folder = r'C:\Users\ramon\Desktop\FatafeatLinks'
output_file = os.path.join(input_folder, 'merged_links.txt')
all_links = set()  # مجموعة لتخزين الروابط والتحقق من عدم التكرار

# قراءة جميع ملفات النصوص في المجلد
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as file:  # استخدام ترميز UTF-8
            for line in file:
                link = line.strip()  # إزالة المسافات البيضاء من البداية والنهاية
                if link:
                    all_links.add(link)

# حفظ الروابط في ملف نصي واحد بعد إزالة التكرارات
with open(output_file, 'w', encoding='utf-8') as output:  # استخدام ترميز UTF-8
    for link in sorted(all_links):
        output.write(link + '\n')

print(f"Total unique links collected: {len(all_links)}")
print(f"Merged links saved to: {output_file}")
