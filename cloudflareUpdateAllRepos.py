import os
import shutil

# المجلد الأساسي الذي يحتوي على الملفات المراد نسخها
source_project = r"J:/cartoon - Copy"

# قائمة المجلدات الهدف
repos = [
    r"J:/cloudflare/cloudflare_repo1",
    r"J:/cloudflare/cloudflare_repo2",
    r"J:/cloudflare/cloudflare_repo3",
    r"J:/cloudflare/cloudflare_repo4",
    r"J:/cloudflare/cloudflare_repo5",
    r"J:/cloudflare/cloudflare_repo6",
    r"J:/cloudflare/cloudflare_repo7",
    r"J:/cloudflare/cloudflare_repo8",
    r"J:/cloudflare/cloudflare_repo9",
    r"J:/cloudflare/cloudflare_repo10",
    r"J:/cloudflare/cloudflare_repo11",
    r"J:/cloudflare/cloudflare_repo12",
    r"J:/cloudflare/cloudflare_repo13",
    r"J:/cloudflare/cloudflare_repo14",
    r"J:/cloudflare/cloudflare_repo15",
    r"J:/cloudflare/cloudflare_repo16",
    r"J:/cloudflare/cloudflare_repo17",
    r"J:/cloudflare/cloudflare_repo18",
    r"J:/cloudflare/cloudflare_repo19",
    r"J:/cloudflare/cloudflare_repo20",
    r"J:/cloudflare/cloudflare_repo21",
]

# استثناء مجلدات معينة مثل .git و .vercel
excluded_dirs = {'.git', '.vercel','.next','node_modules',}

# دالة لنسخ الملفات باستثناء المجلدات المحددة
def copy_project_files(source, destination):
    for root, dirs, files in os.walk(source):
        # استثناء المجلدات المحددة
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        # إنشاء المسارات داخل الوجهة
        dest_dir = os.path.join(destination, os.path.relpath(root, source))
        os.makedirs(dest_dir, exist_ok=True)
        
        # نسخ الملفات
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dst_file)
            print(f"Copied: {src_file} to {dst_file}")

# نسخ المحتويات إلى كل مجلد من المجلدات الفرعية
for repo in repos:
    try:
        print(f"Copying files to {repo} ...")
        copy_project_files(source_project, repo)
        print(f"Successfully updated {repo}.")
    except Exception as e:
        print(f"Failed to update {repo}: {e}")
