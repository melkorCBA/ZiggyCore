import cv2
import os
import errno
import json
from typing import Sequence, Any


def captureImage(RoI, faceRecNo, imgId, parentDir="data"):

    try:
        path = os.path.join(parentDir, str(faceRecNo))
        if not os.path.exists(path):
            os.mkdir(path)
        cv2.imwrite(path + "/user." + str(faceRecNo) +
                    "." + str(imgId) + ".jpg", RoI)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise


def getFaceRecNoListFromJSON(path: str = "faceRECs/facesRecNumbers.json") -> Sequence[Any]:
    with open(path) as f:
        data = json.load(f)
        f.close()
    return data


def getNameFromFaceRecNo(faceRecNo: int, faceRecNoList) -> str:
    return next(filter(lambda element: element["faceRecNo"] ==
                       faceRecNo, faceRecNoList))["name"] or ""
