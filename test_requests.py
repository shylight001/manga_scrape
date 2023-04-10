import requests
import os
img = 'https://img.pic-server.com/美丽新世界/1/14.jpg'
file_path = "downloads\\new_world\\"
file_name = file_path+img.split('/')[-1]
if not os.path.exists(file_path):
   os.makedirs(file_path)
print(img)
try:
    r = requests.get(img, stream=True,headers={'User-Agent': 'Mozilla/5.0'})
    print(r)
    print(r.status_code)
    print(file_name)
    if r.status_code == 200:
        with open(file_name, 'wb+') as f:
            for chunk in r:
                f.write(chunk)
except Exception as e:
    print(e)