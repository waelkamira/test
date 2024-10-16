import os
import pandas as pd

# مسار المجلد الذي يحتوي على ملفات CSV
folder_path = r'C:\Users\ramon\Desktop\BBCGoodFoodLinks'

# قائمة لتخزين الداتا فريمز
dataframes = []

# قائمة لتخزين الروابط
links = []

# قراءة كل ملفات CSV في المجلد وإضافتها إلى القائمة
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, encoding='utf-8-sig')  # تأكد من استخدام نفس الترميز للقراءة
        
        # تحويل القيم في عمود ingredients إلى نصوص ثم استبعاد السطور التي لا تحتوي على ingredients
        df['ingredients'] = df['ingredients'].astype(str)  # تحويل القيم إلى نصوص
        df = df[df['ingredients'].notna() & df['ingredients'].str.strip().ne('')]
        
        # إضافتها إلى قائمة الداتا فريمز
        dataframes.append(df)
        
        # استخراج الروابط وإضافتها إلى القائمة
        if 'link' in df.columns:
            links.extend(df['link'].dropna().tolist())

# دمج جميع الداتا فريمز في داتا فريم واحد مع تجنب التكرار على حسب العمود theWay
merged_df = pd.concat(dataframes, ignore_index=True).drop_duplicates(subset=['theWay'])

# حفظ الداتا فريم المدموج في ملف CSV جديد
merged_csv_path = os.path.join(folder_path, 'merged_recipes.csv')
merged_df.to_csv(merged_csv_path, index=False, encoding='utf-8-sig')

# حفظ الروابط في ملف نصي
links_txt_path = os.path.join(folder_path, 'all_links.txt')
with open(links_txt_path, 'w', encoding='utf-8-sig') as f:
    for link in links:
        f.write(link + '\n')

print(f"All CSV files have been merged into {merged_csv_path} without duplicates based on 'theWay'")
print(f"All links have been saved into {links_txt_path}")
