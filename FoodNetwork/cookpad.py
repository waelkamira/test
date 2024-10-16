from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_image_url(url):
    # إعداد خيارات المتصفح
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # تشغيل المتصفح في الخلفية
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # تشغيل متصفح كروم
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # الانتظار لعدة ثواني لضمان تحميل الصفحة بالكامل

        # جلب رابط الصورة
        img_tag = driver.find_element(By.CSS_SELECTOR, 'picture img')
        image_url = img_tag.get_attribute('src')

        return image_url

    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
        return None
    finally:
        driver.quit()

# الرابط للوصفة
url = "https://cookpad.com/us/recipes/23911279-boston-cream-pie-poke-cake?ref=search&search_term=cake"

# جلب رابط الصورة
image_url = get_image_url(url)

# طباعة رابط الصورة
if image_url:
    print("رابط الصورة:", image_url)
else:
    print("لم يتم العثور على الصورة.")
