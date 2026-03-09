import os
from PIL import Image

def shrink_all_in_dir(path):
    epsilon = 0.1
    for name in os.listdir(path):
        img = Image.open(path+"/"+name)
        img = img.resize((int(img.size[0]*epsilon), int(img.size[1]*epsilon)))
        img.save(path+"/"+name)

shrink_all_in_dir("resources/player/crouch_punch_r")
shrink_all_in_dir("resources/player/crouch_punch_l")
shrink_all_in_dir("resources/player/slide_l")
shrink_all_in_dir("resources/player/slide_r")