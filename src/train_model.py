import cv2
import numpy as np
import os

dataset_path = "dataset"

faces = []
labels = []

label_id = 0

for person_name in os.listdir(dataset_path):

    person_folder = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_folder):
        continue

    for image_name in os.listdir(person_folder):

        image_path = os.path.join(person_folder, image_name)

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        faces.append(img)
        labels.append(label_id)

    label_id += 1

print("Faces Loaded:", len(faces))
print("Labels Loaded:", len(labels))

if len(faces) == 0:
    print("No training images found!")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(faces, np.array(labels))

recognizer.save("trainer.yml")

print("Model trained successfully!")