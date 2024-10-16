import os

input_file_path = r'C:\Users\ramon\Desktop\AllRecipesLinks\merge_from_ofoct.txt'  # ضع مسار الملف النصي الذي يحتوي على الروابط هنا
output_file_path = r'C:\Users\ramon\Desktop\filtered_links.txt'  # ضع المسار الذي تريد حفظ الروابط المفلترة فيه

def filter_links(input_file, output_file, pattern):
    """تصفية الروابط التي تحتوي على النمط المحدد وحفظها في ملف منفصل."""
    filtered_links = []
    
    # قراءة الروابط من الملف النصي
    with open(input_file, 'r') as file:
        links = file.readlines()
    
    # تصفية الروابط التي تحتوي على النمط المحدد
    for link in links:
        if pattern in link:
            filtered_links.append(link.strip())
    
    # حفظ الروابط المفلترة في ملف نصي منفصل
    with open(output_file, 'w') as file:
        for link in filtered_links:
            file.write(link + '\n')
    
    print(f"Saved {len(filtered_links)} filtered links to {output_file}")

# تنفيذ وظيفة التصفية
filter_links(input_file_path, output_file_path, 'https://www.allrecipes.com/recipe/')
