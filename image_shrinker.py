import os
from PIL import Image

def shrink_all_in_dir(path):
    epsilon = 0.1
    for name in os.listdir(path):
        img = Image.open(path+"/"+name)
        img = img.resize((int(img.size[0]*epsilon), int(img.size[1]*epsilon)))
        img.save(path+"/"+name)

shrink_all_in_dir("resources/player/idle_r")
shrink_all_in_dir("resources/player/idle_l")
shrink_all_in_dir("resources/player/punch_r")
shrink_all_in_dir("resources/player/punch_l")
shrink_all_in_dir("resources/player/kick_r")
shrink_all_in_dir("resources/player/kick_l")
shrink_all_in_dir("resources/player/run_r")
shrink_all_in_dir("resources/player/run_l")
shrink_all_in_dir("resources/player/crouch_r")
shrink_all_in_dir("resources/player/crouch_l")
shrink_all_in_dir("resources/player/crouch_punch_r")
shrink_all_in_dir("resources/player/crouch_punch_l")
shrink_all_in_dir("resources/player/crouch_kick_r")
shrink_all_in_dir("resources/player/crouch_kick_l")
shrink_all_in_dir("resources/player/crawl_r")
shrink_all_in_dir("resources/player/crawl_l")
shrink_all_in_dir("resources/player/jump_r")
shrink_all_in_dir("resources/player/jump_l")
shrink_all_in_dir("resources/player/jump_punch_r")
shrink_all_in_dir("resources/player/jump_punch_l")
shrink_all_in_dir("resources/player/jump_kick_r")
shrink_all_in_dir("resources/player/jump_kick_l")