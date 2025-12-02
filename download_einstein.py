import requests
import os

url = "https://upload.wikimedia.org/wikipedia/commons/4/4b/Albert_Einstein_Head_%28cropped%29.jpg"
output_path = "jagan_demo/static/images/einstein.jpg"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

print(f"Downloading {url}...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f"Saved to {output_path}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
