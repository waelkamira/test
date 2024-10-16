



import pandas as pd


# تحميل ملف Excel من سطح المكتب
file_path = r'C:\Users\wael\Desktop\spacetoonSongs.xlsx'  # استبدل اسم_المستخدم واسم_الملف بالمعلومات الصحيحة

# قراءة الملف
df = pd.read_excel(file_path)

# إزالة المسافات البيضاء من بداية ونهاية كل خلية في العمود songName
df['spacetoonSongName'] = df['spacetoonSongName'].str.strip()

# حفظ التعديلات في نفس الملف أو ملف جديد
# df.to_excel(file_path, index=False, engine='openpyxl')  # يحفظ التعديلات في نفس الملف
# أو استخدم هذا السطر لحفظه في ملف جديد
df.to_excel(r'C:\Users\wael\Desktop\edited.xlsx', index=False, engine='openpyxl')

print("تمت إزالة المسافات البيضاء بنجاح.")
