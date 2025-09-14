import traceback
import cv2
import numpy as np
import tensorflow as tf
from cv2.typing import MatLike

from helper.image_transfer import get_result_image
def resize_image(input_image,name : str="Content Image"):
    try:
        size_threshold : tuple[int, int] = (2000,2000)
        resizing_shape : tuple[int, int]  = (1000,1000)

        input_image_shape : tuple[int,int] = input_image.shape
        
        resize_content : bool = True if input_image_shape[0] > size_threshold[0] or input_image_shape[1] > size_threshold[1] else False
    
        if resize_content is True:
            print(f"{name} bigger than {size_threshold}, resizing to {resizing_shape}")
            return get_resize_image(input_image,resizing_shape)

        print(f"{name} Shape: ", input_image_shape)
        return input_image
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'resize_image': {e}")  
        return None



def get_resize_image(image,resizing_shape : tuple[int,int]):
    try:
        input_image : MatLike = cv2.resize(image,(resizing_shape[0],resizing_shape[1]))
        numpy_input_image = np.array(input_image)
        return numpy_input_image
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'get_resize_image': {e}")  
        return None

def convert_to_numpy_image(image):
    return image.astype(np.float32)[np.newaxis, ...] / 255.
    

def resize_then_covert(image,name : str):
    try:
        resized_image = resize_image(image, name)
        # Convert to float32 numpy array, add batch dimension, and normalize to range [0, 1]. Example using numpy:
        numpy_image = convert_to_numpy_image(resized_image)
        return numpy_image
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'resize_then_covert': {e}")  
        return None


def resize_tf_style(style_image): 
    try:
        resize_style_shape: tuple[int, int] = (256, 256)
        style_tf_image = tf.image.resize(style_image, resize_style_shape)
        return style_tf_image
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'resize_tf_style': {e}")  
        return None


def transfer_style(content_image, style_image, hub_module,resize_style : bool = True,resize  : bool  = True):
    try:
        if style_image is None:
            return content_image
        print("Starting style transfer: ", style_image)

        content_numpy_image = resize_then_covert(content_image, "Content Image") if resize else content_image
        if resize_style and resize:
            style_numpy_image = resize_then_covert(style_image, "Style Image")
            style_tf_image = resize_tf_style(style_numpy_image)
        else:
            style_tf_image = style_image
        print("Loading pre-trained model...")
        # The hub.load() loads any TF Hub model
        
        print("Generating stylized image now...wait a minute")
        # Stylize image.
        stylized_image = process_image(content_numpy_image, style_tf_image, hub_module)
        

        return stylized_image
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'transfer_style': {e}")
        return content_image

def process_image(content_image,style_image,model, output_size : tuple[int,int] = (224,224),resize = False): 
    
    try:
        start_time = tf.timestamp()
        if resize:
            content_image = tf.image.resize(content_image, [224, 224])
            style_image = tf.image.resize(style_image, [224, 224])
        outputs = model(inputs=( style_image,content_image))
        stylized_image = get_model_image(outputs)
        test_output = get_result_image(stylized_image, output_size[0], output_size[1])
        end_time = tf.timestamp()
        processing_time : float = float(end_time - start_time)
        print(f"Stylizing completed in {processing_time:.2f} seconds...")
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'process_image': {e}")  
  
    return test_output
def get_model_image(outputs):
    try:
        output_image = outputs[0]
        # reshape the stylized image
        stylized_image = np.array(output_image)

        return stylized_image   
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'get_model_image': {e}")  
  