from paz.applications import HaarCascadeFrontalFace, MiniXceptionFER
import paz.processors as pr
from face import Face
from typing import Any, Union, Sequence


class EmotionDetector(pr.Processor):
    def __init__(self):
        super(EmotionDetector, self).__init__()
        self.detect = HaarCascadeFrontalFace(draw=False)
        self.crop = pr.CropBoxes2D()
        self.classify = MiniXceptionFER()
        # self.draw = pr.DrawBoxes2D(self.classify.class_names)

    def call(self, faces: Sequence[Face]) -> Sequence[Face]:

        for face in faces:
            class_names = self.classify(face.croppedFace)['class_name']
            face.emotionClass = class_names
            # face.emotionScore = scores
        return faces
