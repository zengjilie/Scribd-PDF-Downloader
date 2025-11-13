# open contentUrl 

# docManager.addPage({
# ...
# contentUrl: "https://html.scribdassets.com/664c5hd7b4d1p9op/pages/1-cb5750cfc6.jsonp"
# });

# https://html.scribdassets.com....jsonp

# http://html.scribd.com...png

import re
import requests

html = "file.html"
org_url_pattern = r"https.*jsonp"
open_url_pattern = r"http:(.*?)png"

# get url from the downloaded html
org_urls = []
with open(html, "r") as file:
    for line in file:
       matched_url = re.search(org_url_pattern, line) 
       if matched_url:
           org_urls.append(matched_url.group(0))

# get true urls
image_urls = []
for i in range(len(org_urls)):

    response = requests.get(org_urls[i])
    res_cont = response.text

    matched_open_url = re.search(open_url_pattern, res_cont)
    if matched_open_url:
        image_urls.append(matched_open_url.group(0))

    print(f"Processing {len(org_urls) - i}/{len(org_urls)}...")


from PIL import Image
from io import BytesIO

images = []
for i in range(len(image_urls)):
    response = requests.get(image_urls[i])
    img = Image.open(BytesIO(response.content))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    images.append(img)
    print(f"Downloading {len(image_urls) - i}/{len(image_urls)}...")

print("Generating PDF...")

# Save as PDF
images[0].save('output.pdf', save_all=True, append_images=images[1:])
print("DONE!!!")