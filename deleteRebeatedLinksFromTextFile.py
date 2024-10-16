import os

def remove_duplicate_links(file_path):
    # قراءة الروابط من الملف
    with open(file_path, 'r', encoding='utf-8') as file:
        links = file.readlines()
    
    # إزالة الروابط المكررة باستخدام مجموعة (set)
    unique_links = list(set(link.strip() for link in links))
    
    # حفظ الروابط الفريدة في ملف جديد
    new_file_path = os.path.splitext(file_path)[0] + '_unique.txt'
    with open(new_file_path, 'w', encoding='utf-8') as file:
        for link in unique_links:
            file.write(link + "\n")
    
    print(f"Unique links saved to {new_file_path}")

# مسار ملف النصوص الذي يحتوي على الروابط
txt_file_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'merged_links.txt')

remove_duplicate_links(txt_file_path)
