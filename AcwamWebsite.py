import requests
from bs4 import BeautifulSoup
import xlsxwriter
from datetime import datetime
import uuid
import os

# إعدادات المسلسل
series_name = "أدغال الديجيتال الموسم 1"
base_url = "https://ak.sv/watch/"
start_first_number = 98756
start_second_number = 52709
episode_count = 100
# الحصول على مسار سطح المكتب
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
file_name = os.path.join(desktop_path, f'{series_name}.xlsx')

# إنشاء ملف Excel
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()

# كتابة العناوين
headers = ['id', 'seriesName', 'episodeName', 'episodeLink', 'created_at', 'updated_at']
for col, header in enumerate(headers):
    worksheet.write(0, col, header)

# التواريخ الثابتة
created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "+00"
updated_at = created_at

# Function to extract video link from a page
def get_video_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video')
        if (video_tag := soup.find('video')) and (source_tag := video_tag.find('source')) and source_tag.has_attr('src'):
            return source_tag['src']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None

# توليد الحلقات وحفظها في الملف
for i in range(episode_count):
    episode_number = str(i + 1)
    episode_name = f"{series_name} الحلقة {episode_number}"
    
    # Generate the page link
    page_link = f"{base_url}{start_first_number + i}/{start_second_number + i}"
    
    # Get the video link from the page
    episode_link = get_video_link(page_link)
    
    if episode_link:
        episode_id = str(uuid.uuid4())
        episode_data = [episode_id, series_name, episode_name, episode_link, created_at, updated_at]
        
        # كتابة البيانات في Excel
        for col, data in enumerate(episode_data):
            worksheet.write(i + 1, col, data)
    else:
        print(f"لم يتم العثور على رابط الفيديو للحلقة {episode_number}")

# إغلاق الملف لحفظه
workbook.close()

print(f"تم حفظ الملف على سطح المكتب: {file_name}")
