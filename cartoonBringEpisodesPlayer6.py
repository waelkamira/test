# import xlsxwriter
# from datetime import datetime
# import uuid
# import os

# def generate_episode_links(base_url, start_id, num_episodes):
#     """
#     توليد روابط الحلقات تلقائيًا بناءً على الرابط الأساسي
#     """
#     links = []
#     for i in range(num_episodes):
#         episode_id = start_id + i
#         episode_number = i + 1  # رقم الحلقة الحالي
#         # تعديل الرابط ليتضمن رقم الحلقة
#         episode_link = f"{base_url}?url=NWY3VlBsbTNWYll5cmxLMjhuUGFFQT09&id={episode_id}&funame=al7deqa_alseria_{episode_number + 33}.mp4&y=1"
#         links.append(episode_link)
#     return links

# def create_excel_file(file_name, series_name, episode_links):
#     """
#     إنشاء ملف Excel وحفظ الحلقات به
#     """
#     # إنشاء ملف Excel
#     workbook = xlsxwriter.Workbook(file_name)
#     worksheet = workbook.add_worksheet()

#     # كتابة العناوين
#     headers = ['id', 'seriesName', 'episodeName', 'episodeLink', 'created_at', 'updated_at']
#     for col, header in enumerate(headers):
#         worksheet.write(0, col, header)

#     # تهيئة المتغيرات
#     created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "+00"
#     updated_at = created_at

#     # توليد الحلقات وحفظها في الملف
#     for i, link in enumerate(episode_links):
#         episode_number = str(i + 1).zfill(2)  # تنسيق رقم الحلقة
#         episode_name = f"{series_name} الحلقة {i + 1}"
#         episode_id = str(uuid.uuid4())

#         # كتابة البيانات في Excel
#         episode_data = [episode_id, series_name, episode_name, link, created_at, updated_at]
#         for col, data in enumerate(episode_data):
#             worksheet.write(i + 1, col, data)

#     # إغلاق الملف لحفظه
#     workbook.close()
#     print(f"تم حفظ الملف على سطح المكتب: {file_name}")

# def main():
#     # تحديد الرابط الأساسي وعدد الحلقات
#     base_url = 'https://www.arteenz.com/plugins/server6/embed.php'
#     start_id = 667  # بداية معرف الحلقة
#     num_episodes = 43  # عدد الحلقات التي تريد استخراجها

#     # توليد روابط الحلقات
#     episode_links = generate_episode_links(base_url, start_id, num_episodes)

#     # تحديد مسار حفظ ملف Excel
#     desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#     file_name = os.path.join(desktop_path, 'الحلقات.xlsx')

#     # إنشاء ملف Excel
#     create_excel_file(file_name, "الفتى النبيل", episode_links)

# if __name__ == "__main__":
#     main()


import requests
from bs4 import BeautifulSoup

def extract_iframe_links(url):
    # إرسال طلب HTTP للحصول على محتوى الصفحة
    response = requests.get(url)
    
    # تحقق من نجاح الطلب
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    # استخدام BeautifulSoup لتحليل الصفحة
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # استخراج جميع روابط iframe
    iframes = soup.find_all('iframe')
    
    links = []
    for iframe in iframes:
        src = iframe.get('src')
        if src:
            links.append(src)
    
    return links

def main():
    # الرابط إلى الصفحة الأولى
    url = 'https://www.arteenz.com/watch-634.html'  # استبدل هذا برابط الصفحة الحقيقي
    
    # استخراج الروابط
    links = extract_iframe_links(url)
    
    # طباعة الروابط المستخرجة
    for link in links:
        print(link)

if __name__ == "__main__":
    main()
