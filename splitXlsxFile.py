import pandas as pd

# تحميل ملف Excel
excel_path = r'C:\Users\ramon\Desktop\كل الوصفات الاجنبية.xlsx'
df = pd.read_excel(excel_path)

# فصل البيانات إلى ملفين بناءً على شرط معين
# على سبيل المثال، يمكننا تقسيم الصفوف إلى نصفين
half = len(df) // 2

# البيانات الأولى (النصف الأول)
df1 = df.iloc[:half, :]

# البيانات الثانية (النصف الثاني)
df2 = df.iloc[half:, :]

# حفظ البيانات في ملفات Excel منفصلة
df1.to_excel(r'C:\Users\ramon\Desktop\اسم_الملف_الأول.xlsx', index=False)
df2.to_excel(r'C:\Users\ramon\Desktop\اسم_الملف_الثاني.xlsx', index=False)

print("تم فصل الملف إلى ملفين بنجاح.")
