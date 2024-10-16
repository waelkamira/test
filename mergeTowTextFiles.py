import os

# تحديد اسم المستخدم الخاص بك
username = 'ramon'  # استبدل 'ramon' باسم المستخدم الخاص بك

# تحديد مسار سطح المكتب
desktop_path = os.path.join('C:\\', 'Users', username, 'Desktop')

# قراءة الروابط من الملف الأول
with open(r'C:\Users\ramon\Desktop\AllRecipesLinks\merged_links.txt', 'r') as file1:
    links1 = file1.readlines()

# قراءة الروابط من الملف الثاني
with open(r'C:\Users\ramon\Desktop\AllRecipesLinks\New Text Document.txt', 'r') as file2:
    links2 = file2.readlines()

# إزالة التكرارات باستخدام مجموعة
unique_links = set(links1 + links2)

# تحديد مسار الملف الجديد على سطح المكتب
output_file_path = os.path.join(desktop_path, 'merged_links.txt')

# كتابة الروابط المدمجة في الملف الجديد
with open(output_file_path, 'w') as output_file:
    for link in unique_links:
        output_file.write(link)

print(f"تم دمج الروابط بدون تكرار في ملف '{output_file_path}'")
