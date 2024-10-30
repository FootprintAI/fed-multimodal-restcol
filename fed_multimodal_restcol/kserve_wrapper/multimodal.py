import cv2
import numpy as np
import kserve
from typing import Dict

# imread read image and converts it into GRB
def imread(filepath:str):
    import cv2

    im = cv2.imread(filepath,cv2.IMREAD_UNCHANGED)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im

def base64decode(s:str):
    import base64
    import cv2
    import numpy as np

    jpg_original = base64.b64decode(s)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    im = cv2.imdecode(jpg_as_np, cv2.IMREAD_UNCHANGED)
    return im

def base64encode(im) -> str:
    import base64
    import cv2

    im_encode = cv2.imencode('.jpg', im)[1]
    return base64.b64encode(im_encode)

class MultiModalModel(kserve.Model):
    def __init__(self, name: str, name: str):
        super().__init__(name)
        self.name = name

    def load(self):
		# TODO: load models
        self.ready = True

    def predict(self, request: Dict, headers: Dict[str, str] = None) -> Dict:
        inputs = request["instances"]
        # request is wrapped the following format
        # {
        #   "instances": [
        #     {
        #       "image_bytes": {
        #           "b64": "<b64-encoded>",
        #       },
		#		"audio_bytes": {
        #           "b64": "<b64-encoded>",
		#		},
		#		"text": <string>,
        #       "key": "somekeys",
        #     },
        #   ],
        # }
        # and response is wrapped into the following
        # {
        #  "predictions: [
        #    {
		#	   "predicted": {},
        #      "key": "somekeys",
        #      "type": "multimodal-detector",
        #    },
        #  ]
        # }

        im1 = base64decode(inputs[0]["image_bytes"]["b64"])
		h, w, c = im1.shape
		text = inputs[0]["text"]

        return {
                "predictions": [
                {
                    "predicted": {
                        "image": {
                            "h": h,
                            "w": w,
                            "c": c,
                        },
						"text": text,
                    },
                    "key": key,
                    "type": "multimodal-detector",
                },
            ]
        }
