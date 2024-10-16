from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Path to your ChromeDriver executable
CHROME_DRIVER_PATH = 'path/to/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the page
    driver.get('https://www.arteenz.com/watch-1.html')

    # Wait for the page to load and find the video thumbnail
    time.sleep(5)  # Adjust the sleep time as needed
    thumbnail = driver.find_element(By.CSS_SELECTOR, 'img')  # Update selector if necessary

    # Click on the thumbnail to load the video
    thumbnail.click()

    # Wait for the video to load
    time.sleep(5)

    # Find the video URL
    video_element = driver.find_element(By.CSS_SELECTOR, 'video.jw-video')
    video_url = video_element.get_attribute('src')

    # Save the video URL to a text file
    with open('video_url.txt', 'w') as file:
        file.write(video_url)

    print("تم حفظ رابط الفيديو بنجاح.")
except Exception as e:
    print(f"حدث خطأ: {e}")
finally:
    # Close the WebDriver
    driver.quit()
