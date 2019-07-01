from scraper import StoriesWD
from drive import upload_file
from utils import get_filename, download_file
import os

with open("clients.csv") as reader:
    scraper = StoriesWD()
    scraper.load_cookies()
    for linea in reader:
        client, folder_id, username = linea.strip().split(',')
        print(f"Client: {client}, username: {username}")
        images, videos = scraper.download_stories(username, force=True)
        print(f"{len(images)} images found, {len(videos)} videos found")
        print("Uploading images")
        for image_url in images:
            filename = get_filename(image_url)
            download_file(image_url)
            upload_file(folder_id, username, filename)
            os.remove(f"temp/{filename}")
        print("Uploading videos")
        for video_url in videos:
            filename = get_filename(video_url)
            download_file(video_url)
            upload_file(folder_id, username, filename)
            os.remove(f"temp/{filename}")
        print("End of client")
    scraper.save_cookies()
    scraper.close()
