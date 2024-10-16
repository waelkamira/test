# import os
# import pandas as pd
# from googleapiclient.discovery import build

# def get_youtube_link(query):
#     # Replace 'YOUR_API_KEY' with your actual YouTube Data API v3 key
#     api_key = 'AIzaSyDrt5G4NUQ0g6IzOPFjtXmzCvF5LIAUiUs'
    
#     # Build the YouTube service object
#     youtube = build('youtube', 'v3', developerKey=api_key)
    
#     # Call the search.list method to retrieve results matching the specified query term
#     search_response = youtube.search().list(
#         q=query,
#         part='id,snippet',
#         maxResults=1,
#         type='video'
#     ).execute()
    
#     # Check if any video was found
#     if search_response['items']:
#         video_id = search_response['items'][0]['id']['videoId']
#         video_url = f'https://www.youtube.com/watch?v={video_id}'
#         return video_url
#     else:
#         return "No video found for your search."

# # Load Excel file
# input_file_path = r'C:\Users\ramon\Desktop\الوصفات العربية.xlsx'
# df = pd.read_excel(input_file_path)

# # Define the output folder
# output_folder = r'C:\Users\ramon\Desktop\Recipes_Files'
# os.makedirs(output_folder, exist_ok=True)

# # Initialize file counter
# file_counter = 1

# # Iterate over each row in the DataFrame
# for index, row in df.iterrows():
#     meal_name = row['mealName']
#     if pd.notnull(meal_name):
#         video_link = get_youtube_link(meal_name)
#         df.at[index, 'link'] = video_link
#         print(f"Found link for {meal_name}: {video_link}")
        
#         # Create a DataFrame for the current recipe
#         recipe_df = pd.DataFrame([row])
        
#         # Save the DataFrame to a new Excel file
#         output_file_path = os.path.join(output_folder, f'{file_counter}.xlsx')
#         recipe_df.to_excel(output_file_path, index=False)
#         print(f"Saved recipe '{meal_name}' to {output_file_path}")
        
#         # Increment the file counter
#         file_counter += 1

# print("تم جلب الروابط وحفظ الملفات بنجاح.")

import requests
from bs4 import BeautifulSoup


def get_youtube_link_from_google_search(search_url):
    """
    يستخرج رابط أول فيديو يوتيوب من نتيجة بحث جوجل.

    :param search_url: رابط نتيجة البحث في جوجل.
    :return: رابط الفيديو الأول، أو None إذا لم يتم العثور على فيديو.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # البحث عن كل الروابط
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'youtube.com/watch' in href:
            # استخراج رابط الفيديو الحقيقي من نتيجة البحث
            video_link = href.split('/url?q=')[1].split('&')[0]
            return video_link

    return None

# مثال للاستخدام:
search_url = "https://www.google.com/search?q=%D9%88%D8%B5%D9%81%D8%A9+%D9%83%D9%8A%D9%83+%D8%A7%D9%84%D8%B4%D9%88%D9%83%D9%88%D9%84%D8%A7%D8%A9+site:youtube.com&gbv=1&sei=Qzi7Zo7LHtnf5OUPiujCuQw"
first_video_link = get_youtube_link_from_google_search(search_url)

if first_video_link:
    print("رابط أول فيديو:", first_video_link)
else:
    print("لم يتم العثور على فيديو.")


