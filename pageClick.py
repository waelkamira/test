from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# قم بتحميل متصفح كروم باستخدام ChromeDriver
driver = webdriver.Chrome(executable_path='path/to/chromedriver')

# افتح الصفحة المطلوبة
driver.get('file:///C:/Users/wael/Desktop/ad-script.html')

# انتظر قليلاً حتى يتم تحميل الإعلانات والصفحة
time.sleep(5)

# محاولة النقر على الصفحة بعد تحميلها
try:
    # العثور على عنصر <body> أو أي عنصر آخر للنقر عليه
    body_element = driver.find_element(By.TAG_NAME, 'body')
    
    # محاكاة النقر على العنصر
    body_element.click()
    
    # انتظر قليلاً حتى يتم فتح نافذة جديدة
    time.sleep(5)
    
    # التحقق مما إذا كانت هناك نافذة ثانية قد فتحت (نافذة الإعلان)
    if len(driver.window_handles) > 1:
        # قم بالتبديل إلى النافذة المنبثقة
        driver.switch_to.window(driver.window_handles[1])
        
        # أغلق نافذة الإعلان
        driver.close()
        
        # العودة إلى النافذة الأصلية
        driver.switch_to.window(driver.window_handles[0])
    else:
        print("لم يتم فتح نافذة جديدة.")

except Exception as e:
    print(f"حدث خطأ: {e}")

# أغلق المتصفح الأساسي
driver.quit()
