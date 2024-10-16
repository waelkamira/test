
# ! csv هذا الكود لدمج ملفات ال
import os
import pandas as pd

# مسار المجلد الذي يحتوي على ملفات CSV
folder_path = r'C:\Users\ramon\Desktop\Converted_Recipes'

# مسار المجلد الناتج لملفات CSV المدمجة
combined_csv_folder_path = r'C:\Users\ramon\Desktop\Combined_Recipes'
os.makedirs(combined_csv_folder_path, exist_ok=True)

# الدالة لدمج ملفات CSV
def combine_csv_files_in_batches(folder_path, combined_csv_folder_path, batch_size=1000):
    csv_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.csv')]
    batch_number = 0
    
    for i in range(0, len(csv_files), batch_size):
        batch_files = csv_files[i:i+batch_size]
        combined_df = pd.concat([pd.read_csv(f, encoding='utf-8-sig') for f in batch_files])
        
        batch_number += 1
        output_file_path = os.path.join(combined_csv_folder_path, f'combined_recipes_batch_{batch_number}.csv')
        combined_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
        print(f"Combined CSV batch {batch_number} saved to {output_file_path}")

# تشغيل عملية الدمج
combine_csv_files_in_batches(folder_path, combined_csv_folder_path)
