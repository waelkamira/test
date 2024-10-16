import csv
from datetime import datetime
import uuid
import os

# الحصول على مسار سطح المكتب
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
file_name = os.path.join(desktop_path, 'Spacetoon Songs _ أغاني سبيستون.csv')

# فتح ملف CSV للكتابة
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # كتابة العناوين
    headers = ['id', 'seriesName', 'episodeName', 'episodeLink', 'created_at', 'updated_at']
    writer.writerow(headers)

    # تهيئة المتغيرات
    series_name = "Spacetoon Songs _ أغاني سبيستون"
    base_url = "https://cdn.arteenz.com/75441e2b95254493ab02a4e94d7710e9:arteenz/001/tom_and_jerry_old/tom_and_jerry_old_0"
    created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "+00"
    updated_at = created_at

    # توليد الحلقات وحفظها في الملف
    for i in range(625):
        episode_number = str(i + 1).zfill(2)  # تنسيق رقم الحلقة
        episode_name = f"{series_name} الحلقة {i + 1}"
        episode_link = f"{base_url}{episode_number}.mp4"
        episode_id = str(uuid.uuid4())

        # كتابة البيانات في CSV
        episode_data = [episode_id, series_name, episode_name, episode_link, created_at, updated_at]
        writer.writerow(episode_data)

print(f"تم حفظ الملف على سطح المكتب: {file_name}")



# import pandas as pd
# from datetime import datetime
# import uuid
# import os

# # الحصول على مسار سطح المكتب
# desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# file_name = os.path.join(desktop_path, 'كراش بيدامان.xlsx')

# # تهيئة المتغيرات
# series_name = "كراش بيدامان"
# base_url = "https://cdn.arteenz.com/75441e2b95254493ab02a4e94d7710e9:arteenz/001/carsh_bedaman/carsh_bedaman_"
# created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "+00"
# updated_at = created_at

# # تهيئة قائمة لتخزين البيانات
# data = []

# # توليد الحلقات وحفظها في القائمة
# for i in range(50):
#     episode_number = str(i + 1).zfill(2)  # تنسيق رقم الحلقة
#     episode_name = f"{series_name} الحلقة {i + 1}"
#     episode_link = f"{base_url}{episode_number}.mp4"
#     episode_id = str(uuid.uuid4())

#     # إضافة البيانات إلى القائمة
#     episode_data = [episode_id, series_name, episode_name, episode_link, created_at, updated_at]
#     data.append(episode_data)

# # إنشاء DataFrame وحفظه إلى ملف Excel
# df = pd.DataFrame(data, columns=['id', 'seriesName', 'episodeName', 'episodeLink', 'created_at', 'updated_at'])
# df.to_excel(file_name, index=False, engine='openpyxl')

# print(f"تم حفظ الملف على سطح المكتب: {file_name}")
