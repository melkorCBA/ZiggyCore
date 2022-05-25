import cv2
from faceDetection import detect, drawBoundary, getRoI
from dataGenerator import captureImage
from faceRecognition import recognizeFaces
import threading
from frameDraw import addTextTopLeft
from face import Face

faceCascade = cv2.CascadeClassifier(
    "cascades/haarcascade_frontalface_default.xml")
customClassifier = cv2.face.LBPHFaceRecognizer_create()
customClassifier.read("cascades/classifier.yml")
video_capture = cv2.VideoCapture(-1)
frameId = 0
faceRecNo = 2
captureLimit = 120


while True:
    _, img = video_capture.read()
    faces: list = detect(img, frameId,  faceCascade, "face", drawBox=False)
    if(len(faces) > 0):
        face: Face = faces[0]
        if(len(face.coordinates) == 4 and frameId < captureLimit):
            addTextTopLeft("capturing started", img)
            RoI = getRoI(img, face.coordinates)
            captureImage(RoI, faceRecNo, frameId)
            frameId += 1

            # if(id == None):
            #     timerThread.start()
            # else:
        else:
            addTextTopLeft("capturing complete", img)
    cv2.imshow("capture new face", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()

# training logic

# if(faceRecNo == None):
#     addTextTopLeft("new face detected", position=(50, 50), frame=img)
#     if(imgId > 0):
#         addTextTopLeft("capturing started - " + str(imgId) +
#                        "/" + str(captureLimit), position=(50, 55), frame=img)
#     if(imgId < captureLimit):
#         captureImage(RoI, faceId, imgId)
#     trainClassifier()
#     imgId = 0

# id, img = recognizeFaces(customClassifier, RoI, coordinates, img)
# if(id == None):
#     timerThread.start()
# else:
