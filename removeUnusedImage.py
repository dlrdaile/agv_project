import os
with open('./README.md','r') as f:
    text = f.read()
all_image = os.listdir('./image/')
for image in all_image:
    if image not in text:
        os.remove(os.path.join('./image',image))