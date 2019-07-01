import requests

def get_filename(url):
    url = url.split("?")[0]
    filename = url.split("/")[-1]

    return filename

def download_file(url):
    filename = get_filename(url)
    r = requests.get(url)
    with open(f"temp/{filename}", 'wb') as f:  
        f.write(r.content)