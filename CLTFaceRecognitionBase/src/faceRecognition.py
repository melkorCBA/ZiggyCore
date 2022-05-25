import cv2
from face import Face
from typing import Any, Union, Sequence


def recognizeFaces(classifier, faces: Sequence[Face], image, color=(255, 0, 0)) -> Union[Sequence[Face], Any]:

    for face in faces:
        if(len(face.coordinates) == 4):
            x, y, w, h = face.coordinates
            grayscaleImage = cv2.cvtColor(face.croppedFace, cv2.COLOR_BGR2GRAY)
            faceRecNo, _ = classifier.predict(grayscaleImage)
            face.faceRecNo = faceRecNo
            cv2.putText(image, str(faceRecNo), (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, color, 1, cv2.LINE_AA)
    return faces, image
