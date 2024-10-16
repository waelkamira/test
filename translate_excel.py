import pandas as pd
import time
import os
import pyautogui
import pyperclip

# تحميل ملف Excel
excel_path = r'C:\Users\ramon\Desktop\كل الوصفات الاجنبية.xlsx'
df = pd.read_excel(excel_path)

# تحديد الأعمدة التي سيتم ترجمتها
columns_to_translate = ['mealName','ingredients', 'theWay', 'advise' ]

# إنشاء مجلد لحفظ الملف المترجم
output_folder = r'C:\Users\ramon\Desktop\translated_recipes'
os.makedirs(output_folder, exist_ok=True)

# دالة للنقر مع تأكيد الموقع
def click_with_confirmation(x, y, wait_time=2):
    pyautogui.click(x, y)
    time.sleep(wait_time)

# إحداثيات منطقة الإدخال والإخراج بناءً على الصورة
input_box_x, input_box_y = 320, 170    # إحداثيات مربع النص للإدخال
output_box_x, output_box_y = 1400, 170  # إحداثيات منطقة الإخراج في أقصى اليمين

# ترجمة الصف الأول فقط
translated_row = {}
row = df.iloc[0]  # اختيار الصف الأول

for column in columns_to_translate:
    if pd.notnull(row[column]):
        try:
            # نسخ النص الأصلي إلى الحافظة
            original_text = str(row[column])
            pyperclip.copy(original_text)
            time.sleep(1)  # الانتظار للتأكد من نسخ النص

            # النقر على منطقة الإدخال
            click_with_confirmation(input_box_x, input_box_y)  # النقر على منطقة الإدخال
            
            # تنظيف الحقل
            pyautogui.hotkey('ctrl', 'a')  # تحديد الكل
            pyautogui.press('delete')  # حذف المحتوى

            # لصق النص
            pyautogui.hotkey('ctrl', 'v')  # لصق النص
            time.sleep(1)  # الانتظار للتأكد من لصق النص وانتظار الترجمة

            # نقل المؤشر إلى أقصى اليمين لتحديد النص المترجم ونسخه
            click_with_confirmation(output_box_x, output_box_y)  # النقر في منطقة الإخراج في أقصى اليمين
            pyautogui.hotkey('ctrl', 'a')  # تحديد الكل في منطقة الإخراج
            pyautogui.hotkey('ctrl', 'c')  # نسخ النص
            translated_text = pyperclip.paste().strip()

            # التحقق من نجاح الترجمة
            if translated_text and translated_text != original_text:
                translated_row[column] = translated_text
            else:
                print(f"تحذير: قد تكون ترجمة العمود '{column}' فشلت، سيتم استخدام النص الأصلي.")
                translated_row[column] = original_text

        except Exception as e:
            print(f"خطأ أثناء ترجمة العمود '{column}': {e}")
            translated_row[column] = row[column]  # الاحتفاظ بالنص الأصلي إذا فشلت الترجمة

# إنشاء DataFrame للصف المترجم
translated_df = pd.DataFrame([translated_row])

# حفظ الصف المترجم في ملف Excel جديد
translated_excel_path = os.path.join(output_folder, 'recipe_translated_first.xlsx')
translated_df.to_excel(translated_excel_path, index=False)

print(f"تم حفظ الوصفة المترجمة في {translated_excel_path}")