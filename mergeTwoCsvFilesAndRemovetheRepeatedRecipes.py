import pandas as pd

# مسارات ملفات CSV
csv_file_path1 = r'C:\Users\ramon\Desktop\ar_recipes.csv'
csv_file_path2 = r'C:\Users\ramon\Desktop\fatafeat.csv'

# قراءة ملفات CSV
df1 = pd.read_csv(csv_file_path1, encoding='utf-8-sig')
df2 = pd.read_csv(csv_file_path2, encoding='utf-8-sig')

# دمج الملفات في داتا فريم واحد
merged_df = pd.concat([df1, df2], ignore_index=True)

# إيجاد الصفوف المكررة بناءً على العمودين 'mealName' و 'theWay'
duplicate_rows = merged_df[merged_df.duplicated(subset=['mealName', 'theWay'], keep=False)]

# إزالة الصفوف المكررة من الداتا فريم المدموج
unique_df = merged_df.drop_duplicates(subset=['mealName', 'theWay'])

# تحديد مسارات حفظ الملفات
output_csv_path_unique = r'C:\Users\ramon\Desktop\merged_no_duplicates.csv'
output_csv_path_duplicates_ar = r'C:\Users\ramon\Desktop\duplicates_ar.csv'
output_csv_path_duplicates_fatafeat = r'C:\Users\ramon\Desktop\duplicates_fatafeat.csv'

# حفظ الداتا فريم المدموج بعد إزالة التكرارات في ملف CSV جديد
unique_df.to_csv(output_csv_path_unique, index=False, encoding='utf-8-sig')

# حفظ الصفوف المكررة في ملفين منفصلين
duplicates_ar = df1[df1.set_index(['mealName', 'theWay']).index.isin(duplicate_rows.set_index(['mealName', 'theWay']).index)]
duplicates_fatafeat = df2[df2.set_index(['mealName', 'theWay']).index.isin(duplicate_rows.set_index(['mealName', 'theWay']).index)]

duplicates_ar.to_csv(output_csv_path_duplicates_ar, index=False, encoding='utf-8-sig')
duplicates_fatafeat.to_csv(output_csv_path_duplicates_fatafeat, index=False, encoding='utf-8-sig')

print(f"تم دمج الملفين وإزالة التكرارات بناءً على 'mealName' و'theWay'، وحفظ النتيجة في {output_csv_path_unique}")
print(f"تم حفظ الصفوف المكررة من الملف الأول في {output_csv_path_duplicates_ar}")
print(f"تم حفظ الصفوف المكررة من الملف الثاني في {output_csv_path_duplicates_fatafeat}")
