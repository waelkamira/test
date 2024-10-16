import os
import pandas as pd

# تحديد مسار المجلد الذي يحتوي على ملفات CSV
folder_path = r'C:\Users\wael\Desktop\csv-main'

# الحصول على قائمة بجميع الملفات في المجلد
files = os.listdir(folder_path)

# التحقق من كل ملف إذا كان ملف CSV ثم تحويله إلى Excel
for file in files:
    if file.endswith('.csv'):
        csv_file_path = os.path.join(folder_path, file)
        
        # قراءة ملف CSV باستخدام pandas
        df = pd.read_csv(csv_file_path)
        
        # تحديد اسم ملف الإكسل الجديد
        excel_file_path = csv_file_path.replace('.csv', '.xlsx')
        
        # حفظه كملف Excel
        df.to_excel(excel_file_path, index=False)
        
        print(f"تم تحويل {file} إلى {os.path.basename(excel_file_path)} بنجاح.")

print("تم تحويل جميع الملفات بنجاح!")
