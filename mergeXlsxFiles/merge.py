import os
import pandas as pd

# مسار المجلد الذي يحتوي على ملفات Excel
folder_path = r'C:\Users\wael\Desktop\New folder'

# قائمة لتخزين الداتا فريمز
dataframes = []

# قراءة كل ملفات Excel في المجلد وإضافتها إلى القائمة
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path)  # قراءة ملف Excel
        dataframes.append(df)

# دمج جميع الداتا فريمز في داتا فريم واحد
merged_df = pd.concat(dataframes, ignore_index=True)

# حفظ الداتا فريم المدموج في ملف Excel جديد
merged_excel_path = os.path.join(folder_path, 'merged_recipes.xlsx')
merged_df.to_excel(merged_excel_path, index=False)  # إزالة encoding

print(f"All Excel files have been merged into {merged_excel_path}")
