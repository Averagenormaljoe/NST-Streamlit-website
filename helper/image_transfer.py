from PIL import Image
import numpy as np
import av
# Code adapted from 'https://github.com/whitphx/style-transfer-web-app/blob/main/input.py'
def frame_to_image(frame: av.VideoFrame, verbose : int = 0) -> np.ndarray:
    if verbose > 0:
        print("frame:", frame, "type:", type(frame))
    return frame.to_ndarray(format=frame_format)
def get_result_image(transferred: np.ndarray, orig_w: int, orig_h: int) -> np.ndarray:
    result : Image = Image.fromarray((transferred * 255).astype(np.uint8))
    image : np.ndarray = np.asarray(result.resize((orig_w, orig_h)))
    return image
def resize_image(image: np.ndarray, width: int, orig_h: int, orig_w: int) -> np.ndarray:
    input = np.asarray(Image.fromarray(image).resize((width, int(width * orig_h / orig_w))))
    return input