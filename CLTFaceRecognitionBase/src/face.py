class Face:
    def __init__(self, faceId, croppedFace, faceRecNo=None, emotionClass=None, emotionScore=None, coordinates=None, name=None):
        self.faceId = faceId
        self.croppedFace = croppedFace
        self.faceRecNo = faceRecNo
        self.emotionClass = emotionClass
        self.emotionScore = emotionScore
        self.coordinates = coordinates
        self.name = name
