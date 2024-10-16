import pyautogui
import pyperclip
import time
import pandas as pd

def paste_and_get_translation():
    """
    هذه الوظيفة تقوم بتفعيل مربع النص الأيسر، لصق النص، انتظار الترجمة، ومن ثم نسخ النص المترجم من المربع الأيمن.
    """
   

    # لصق النص في مربع النص الأيسر
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(10)  # الانتظار للسماح بإجراء الترجمة

    # تحديد النص المترجم في المربع الأيمن
    pyautogui.hotkey('tab')  # التبديل إلى مربع النص المترجم
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(2)  # الانتظار لنسخ النص

    # قراءة النص المترجم من الحافظة
    translated_text = pyperclip.paste()
    return translated_text

def save_translation_to_excel(text, output_file):
    """
    هذه الوظيفة تقوم بحفظ النص المترجم في ملف Excel على سطح المكتب.
    """
    df = pd.DataFrame({'Translation': [text]})
    df.to_excel(output_file, index=False)
    print(f"تم حفظ النص المترجم في {output_file}")

def main():
    """
    الوظيفة الرئيسية لتشغيل البرنامج.
    """
    text_to_translate = "Hello"
    output_file = r"C:\Users\ramon\Desktop\translated_text.xlsx"
    
    # تحضير النص للنسخ
    pyperclip.copy(text_to_translate)
    
    translated_text = paste_and_get_translation()
    save_translation_to_excel(translated_text, output_file)

if __name__ == "__main__":
    main()
