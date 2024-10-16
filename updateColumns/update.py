import pandas as pd

def convert_xlsx_to_csv(xlsx_file_path, csv_file_path):
    try:
        # قراءة ملف Excel
        df = pd.read_excel(xlsx_file_path)
        
        # حفظ الملف بصيغة CSV
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        
        print(f"تم تحويل الملف إلى CSV وحفظه في: {csv_file_path}")
        
    except Exception as e:
        print(f"حدث خطأ أثناء تحويل الملف: {e}")

# تحديد مسارات الملفات
xlsx_file_path = r'C:\Users\ramon\Desktop\New folder\2.xlsx'
csv_file_path = r'C:\Users\ramon\Desktop\New folder\recipes.csv'

# تنفيذ التحويل
convert_xlsx_to_csv(xlsx_file_path, csv_file_path)
