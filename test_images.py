import cv2
import os

folder = "dataset/Bhuvan"

for img_name in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, img_name))

    if img is not None:
        print(img_name, img.shape)