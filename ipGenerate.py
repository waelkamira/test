import pandas as pd
import random
import os

# دالة لتوليد IP عشوائي
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# توليد مليون IP عشوائي
ip_list = [generate_random_ip() for _ in range(1000000)]

# الحصول على مسار سطح المكتب
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# حفظ IPs في ملف Excel على سطح المكتب
file_path = os.path.join(desktop_path, 'ips.xlsx')
df = pd.DataFrame(ip_list, columns=['IP Address'])
df.to_excel(file_path, index=False)

print(f"تم حفظ مليون عنوان IP في ملف {file_path} بنجاح!")
