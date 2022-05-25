import cv2
from face import Face
from dataGenerator import getNameFromFaceRecNo
from typing import Any, Sequence


def addTextTopLeft(text: str, frame, position=(50, 50), color=(255, 0, 0), font=cv2.FONT_HERSHEY_SIMPLEX, lineSpace: int = 15, initYIndex=50):
    lines: list = text.split("#")
    y: int = initYIndex
    for line in lines:
        cv2.putText(frame,  line,  (50, y),  font,
                    0.5,  color,  1,  cv2.LINE_4)
        y += lineSpace
    return y


def drawFaceinfo(face: Face, frame, yIndex=50) -> int:
    text = "Person: " + str(face.name) + "#" + "FaceRecNo : " + str(
        face.faceRecNo) + "#" + "Emotion: " + str(face.emotionClass) + "#"
    return addTextTopLeft(text, frame, initYIndex=yIndex)


def drawFacesInfo(faces: Sequence[Face], frame, faceRecNoList: list):
    outputText: str = ""
    yPostion = 50
    for face in faces:
        face.name = getNameFromFaceRecNo(face.faceRecNo, faceRecNoList)
        yPostion = drawFaceinfo(face, frame, yIndex=yPostion + 20)
