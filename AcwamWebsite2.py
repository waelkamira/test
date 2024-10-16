import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import os

async def extract_video_links():
    video_links = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # الرابط الأول
        await page.goto("https://ak.sv/watch/149274/80937")

        while True:
            # استخراج رابط الفيديو
            video_url = await page.eval_on_selector("div.plyr__video-wrapper video source", "el => el.src")
            print(f"Extracted video link: {video_url}")
            video_links.append(video_url)

            # حفظ الروابط في ملف Excel في مجلد على سطح المكتب
            df = pd.DataFrame(video_links, columns=["Video Link"])
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            folder_path = os.path.join(desktop_path, 'Video_Links')
            os.makedirs(folder_path, exist_ok=True)
            df.to_excel(os.path.join(folder_path, 'video_links.xlsx'), index=False)

            # محاولة العثور على زر "الحلقة التالية"
            next_button = await page.query_selector('a:has(h3.entry-title:has-text("الحلقة التالية"))')
            if not next_button:
                break  # الخروج من الحلقة إذا لم يتم العثور على زر "الحلقة التالية"

            # الضغط على زر "الحلقة التالية"
            await next_button.click()

            # الانتظار 5 ثوانٍ بعد الضغط على زر "الحلقة التالية"
            await page.wait_for_timeout(5000)  # انتظار تحميل الصفحة التالية

        await browser.close()

    print(f"Video links saved to video_links.xlsx in {folder_path} on the desktop.")

# تشغيل الوظيفة
asyncio.run(extract_video_links())
