
import os

def read_links_from_file(filename):
    """قراءة الروابط من ملف نصي."""
    links = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                link = line.strip()
                if link:
                    links.add(link)
    return links

def save_links_to_file(links, filename):
    """حفظ الروابط في ملف نصي."""
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')
    print(f"Saved {len(links)} links to {filename}")

# قراءة الروابط من الملفين
file1 = r'C:\Users\ramon\Desktop\AllRecipesLinks\links.txt'
file2 = r'C:\Users\ramon\Desktop\AllRecipesLinks\all_links.txt'

links_file1 = read_links_from_file(file1)
links_file2 = read_links_from_file(file2)

# إيجاد الروابط المشتركة
common_links = links_file1.intersection(links_file2)

# حذف الروابط المشتركة من كل ملف
unique_links_file1 = links_file1 - common_links
unique_links_file2 = links_file2 - common_links

# حفظ الروابط غير المشتركة في ملفات جديدة
output_file1 = r'C:\Users\ramon\Desktop\AllRecipesLinks\unique_file1.txt'
output_file2 = r'C:\Users\ramon\Desktop\AllRecipesLinks\unique_file2.txt'

save_links_to_file(unique_links_file1, output_file1)
save_links_to_file(unique_links_file2, output_file2)

print("Operation completed successfully!")
