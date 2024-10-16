import pandas as pd

# مسار ملف Excel
excel_file_path = r'C:\Users\wael\Desktop\turkishSongs.xlsx'

# قراءة ملف Excel
df = pd.read_excel(excel_file_path)

# تحديد مسار حفظ ملف CSV
csv_file_path = r'C:\Users\wael\Desktop\turkishSongs.csv'

# تحويل ملف Excel إلى CSV وحفظه
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"تم تحويل ملف Excel إلى CSV بنجاح وحفظه في {csv_file_path}")
