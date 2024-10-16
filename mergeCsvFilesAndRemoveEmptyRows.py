import os
import pandas as pd

# تحديد المسار إلى المجلد الذي يحتوي على ملفات CSV
folder_path = os.path.expanduser("~/Desktop/BBCGoodFoodLinks/MissingImages")  # استبدل your_folder_name باسم مجلدك

# قائمة لتخزين البيانات من كل ملف
dataframes = []

# قراءة كل ملف CSV في المجلد
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        # الاحتفاظ فقط بالصفوف حيث العمود 'theWay' ليس فارغًا
        df = df[df['theWay'].notna()]
        
        # إضافة البيانات إلى القائمة
        dataframes.append(df)

# دمج جميع البيانات في DataFrame واحد
merged_df = pd.concat(dataframes, ignore_index=True)

# حفظ البيانات المدموجة في ملف CSV جديد
output_file_path = os.path.join(folder_path, "merged_output.csv")
merged_df.to_csv(output_file_path, index=False)

print(f"تم دمج الملفات وحفظها في: {output_file_path}")
