import shutil
import os

def create_video_copies(original_video_path, base_name, num_episodes, destination_folder):
    # تأكد أن المسار الوجهة موجود
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # استخراج امتداد الملف الأصلي
    video_extension = os.path.splitext(original_video_path)[1]
    
    # تكرار عدد الحلقات وإنشاء النسخ
    for i in range(1, num_episodes + 1):
        new_video_name = f"{base_name} الحلقة {i}{video_extension}"
        new_video_path = os.path.join(destination_folder, new_video_name)
        
        # تجاوز النسخ إذا كانت الوجهة هي نفس المصدر
        if original_video_path == new_video_path:
            print(f"تم تجاوز النسخ للفيديو الأصلي: {new_video_name}")
            continue
        
        shutil.copy(original_video_path, new_video_path)
        print(f"تم إنشاء النسخة: {new_video_name}")

# مثال على الاستخدام:
original_video_path = r"C:\Users\wael\Desktop\ساندي بل الحلقة 1.mp4"  # ضع مسار الفيديو الأصلي هنا مع r قبل المسار
base_name = "ساندي بل"
num_episodes = 47  # عدد الحلقات
destination_folder = r"C:\Users\wael\Desktop\ساندي بل الحلقات"  # مسار المجلد الوجهة على سطح المكتب

create_video_copies(original_video_path, base_name, num_episodes, destination_folder)
