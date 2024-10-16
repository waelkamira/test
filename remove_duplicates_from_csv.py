


import pandas as pd

# مسار ملف CSV على سطح المكتب
input_file = r'C:\Users\ramon\Desktop\ar_recipes.csv'  # استبدل "your_file.csv" باسم ملفك
output_file = r'C:\Users\ramon\Desktop\cleaned_file.csv'

# قراءة ملف CSV
df = pd.read_csv(input_file)

# إزالة الصفوف المكررة بناءً على عمود 'theWay'
df_cleaned = df.drop_duplicates(subset='theWay')

# حفظ الملف بدون الصفوف المكررة
df_cleaned.to_csv(output_file, index=False)

print(f"تمت إزالة الصفوف المكررة بناءً على العمود 'theWay' وحفظ الملف في: {output_file}")
