import os
import pandas as pd

# تحديد مسار المجلد الذي يحتوي على ملفات Excel
folder_path = r'C:\Users\wael\Desktop\csv-main'

# الحصول على قائمة بجميع الملفات في المجلد
files = os.listdir(folder_path)

# التحقق من كل ملف إذا كان ملف Excel ثم تحويله إلى CSV
for file in files:
    if file.endswith('.xlsx'):
        excel_file_path = os.path.join(folder_path, file)
        
        # قراءة ملف Excel باستخدام pandas
        df = pd.read_excel(excel_file_path)
        
        # تحديد اسم ملف CSV الجديد
        csv_file_path = excel_file_path.replace('.xlsx', '.csv')
        
        # حفظه كملف CSV
        df.to_csv(csv_file_path, index=False)
        
        print(f"تم تحويل {file} إلى {os.path.basename(csv_file_path)} بنجاح.")

print("تم تحويل جميع الملفات بنجاح!")
