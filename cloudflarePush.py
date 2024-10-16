import os
import subprocess

# قائمة المخازن التي تحتوي على "cloudflare" فقط
repos = [
    "https://github.com/waelkamira/cartoon_cloudflare",
    "https://github.com/waelkamira/cartoon_cloudflare_repo1.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo2.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo3.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo4.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo5.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo6.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo7.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo8.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo9.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo10.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo11.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo12.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo13.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo14.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo15.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo16.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo17.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo18.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo19.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo20.git",
    "https://github.com/waelkamira/cartoon_cloudflare_repo21.git",
]

# الدليل الأساسي الذي يحتوي على جميع المشاريع
base_dir = "J:/cloudflare"

# البدء في عملية الدفع لكل مخزن
for repo in repos:
    # استخراج اسم المشروع من عنوان URL
    project_name = os.path.basename(repo).replace(".git", "")
    
    # تعديل الاسم ليتوافق مع المجلدات الموجودة مثل "cloudflare_repo1" بدلاً من "cartoon_cloudflare_repo1"
    project_name = project_name.replace("cartoon_", "")  # إزالة "cartoon_"

    # الدليل المحلي للمشروع
    project_dir = os.path.join(base_dir, project_name)

    # التحقق من وجود الدليل المحلي للمشروع
    if not os.path.isdir(project_dir):
        print(f"Directory for project {project_name} does not exist: {project_dir}")
        continue

    # الانتقال إلى دليل المشروع
    os.chdir(project_dir)

    # سحب آخر التحديثات من المخزن البعيد
    subprocess.run(["git", "pull", "origin", "main"], check=True)

    # التحقق من وجود تغييرات غير مدفوعة
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

    if status.stdout.strip():
        print(f"Found uncommitted changes in {project_name}. Committing changes...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto commit changes before pushing"], check=True)

    # الدفع إلى المخزن البعيد
    subprocess.run(["git", "push", "origin", "main"], check=True)

    print(f"Successfully pushed to {project_name}.")
