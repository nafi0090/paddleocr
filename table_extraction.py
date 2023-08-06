import cv2
import numpy as np
import pandas as pd
from PIL import Image
from typing import Union, List, Dict
from paddleocr import PPStructure


class TableExtraction:
    def __init__(self):
        self.model = PPStructure(show_log=False, image_orientation=True)

    def predict(
        self, image_pillow: Image.Image
    ) -> List[Dict[str, Union[str, int, float]]]:
        preprocessing_image = self.preprocessing_image(image_pillow)
        outputs = self.model(preprocessing_image)
        return_predicted = self.postprocessing_output(outputs)
        return return_predicted

    def preprocessing_image(self, image_pillow: Image.Image) -> np.ndarray:
        image = np.array(image_pillow)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image

    def postprocessing_output(
        self,
        outputs: List[
            Dict[
                str,
                Union[
                    str,
                    int,
                    List[int],
                    np.ndarray,
                    Dict[str, Union[str, List[List[int]]]],
                ],
            ]
        ],
    ) -> List[Dict[str, Union[str, int, float]]]:
        print(outputs)
        return_predicted = pd.read_html(outputs[0]["res"]["html"], header=0)[0]
        return_predicted = return_predicted.fillna("")
        return_predicted = return_predicted.to_dict(orient="records")
        return return_predicted


if __name__ == "__main__":
    image = Image.open("asd.jpeg")
    model = TableExtraction()
    result = model.predict(image)
    print(result)
