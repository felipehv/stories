from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime as dt

def upload_file(folder_id, username, filename):
    """
    folder_id: id of the drive folder
    username: username being captured
    filename: something like thisismyimage.jpg
    """
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    date = str(dt.datetime.now()).split(" ")[0]

    # Create and upload file
    file1 = drive.CreateFile()
    full_filename = f"{username}-{date}-{filename}"
    file1['title'] = full_filename
    file1['parents'] = [{'id':folder_id}]
    file1.SetContentFile(f'temp/{filename}')
    file1.Upload() # If file exists, it overwrites

if __name__ == "__main__":
    upload_file("1ahyuKxxTWQ8Zc-EuvVyxTBpPLkrp9Iwt", "iusermame", "65645455_338710733721953_390513323127802153_n.mp4")