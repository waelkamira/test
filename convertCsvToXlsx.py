import pandas as pd

# تحديد مسار ملف CSV وملف XLSX
csv_file_path = r'C:\Users\wael\Desktop\episodes.csv'  # استبدل wael باسم المستخدم الخاص بك واسم الملف بملفك
xlsx_file_path = r'C:\Users\wael\Desktop\episodes.xlsx'  # استبدل wael باسم المستخدم الخاص بك واسم الملف بملفك

# قراءة ملف CSV
df = pd.read_csv(csv_file_path)

# تحويله إلى ملف XLSX
df.to_excel(xlsx_file_path, index=False)

print(f"تم تحويل {csv_file_path} إلى {xlsx_file_path} بنجاح!")
