import numpy as np
from PIL import Image
import os
import cv2


def trainClassifier(dataDir="data", destination="cascades/classifier.yml"):

    path = [os.path.join(dataDir, file) for file in os.listdir(dataDir)]

    faces = []
    ids = []

    for image in path:
        try:
            img = Image.open(image).convert('L')
            faces.append(np.array(img, 'uint8'))
            ids.append(int(os.path.split(image)[1].split(".")[1]))
        except IsADirectoryError as err:
            pass
    ids = np.array(ids)

    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.train(faces, ids)
    classifier.write(destination)


trainClassifier()
