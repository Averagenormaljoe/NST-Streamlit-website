from PIL import Image
import numpy as np
import av

def frame_to_image(frame: av.VideoFrame) -> np.ndarray:
    """Convert an av.VideoFrame to a numpy array."""
    return frame.to_ndarray(format="bgr24")
def get_result_image(transferred: np.ndarray, orig_w: int, orig_h: int) -> np.ndarray:
    result = Image.fromarray((transferred * 255).astype(np.uint8))
    image = np.asarray(result.resize((orig_w, orig_h)))
    return av.VideoFrame.from_ndarray(image, format="bgr24")
def resize_image(image: np.ndarray, width: int, orig_h: int, orig_w: int) -> np.ndarray:
    return np.asarray(Image.fromarray(image).resize((width, int(width * orig_h / orig_w))))