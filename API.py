import cv2
import numpy as np
import tensorflow as tf
from cv2.typing import MatLike


def resize_image(input_image,name : str="Content Image"):
    size_threshold : tuple[int, int] = (2000,2000)
    resizing_shape : tuple[int, int]  = (1000,1000)

    input_image_shape = input_image.shape
    
    resize_content = True if input_image_shape[0] > size_threshold[0] or input_image_shape[1] > size_threshold[1] else False
  
    if resize_content is True:
        print(f"{name} bigger than {size_threshold}, resizing to {resizing_shape}")
        get_resize_image(input_image,resizing_shape)

    print(f"{name} Shape: ", input_image_shape)
    return input_image

def get_resize_image(image,resizing_shape):
    input_image : MatLike = cv2.resize(image,(resizing_shape[0],resizing_shape[1]))
    numpy_input_image = np.array(input_image)
    return numpy_input_image

def convert_to_numpy_image(image):
    return image.astype(np.float32)[np.newaxis, ...] / 255.
    

def resize_then_covert(image,name : str):
    resized_image = resize_image(image, name)
    # Convert to float32 numpy array, add batch dimension, and normalize to range [0, 1]. Example using numpy:
    numpy_image = convert_to_numpy_image(resized_image)
    return numpy_image


def resize_tf_style(style_image): 
    # Optionally resize the images. It is recommended that the style image is about
    # 256 pixels (this size was used when training the style transfer network).
    # The content image can be any size.
    resize_style_shape: tuple[int, int] = (256, 256)
    style_tf_image = tf.image.resize(style_image, resize_style_shape)
    return style_tf_image

def transfer_style(content_image, style_image, hub_module):
    if style_image is None:
        return content_image
    print("Starting style transfer: ", style_image)

    content_numpy_image = resize_then_covert(content_image, "Content Image")
    style_numpy_image = resize_then_covert(style_image, "Style Image")

    style_tf_image = resize_tf_style(style_numpy_image)

    print("Loading pre-trained model...")
    # The hub.load() loads any TF Hub model
    
    print("Generating stylized image now...wait a minute")
    # Stylize image.
    outputs = process_image(content_numpy_image, style_tf_image, hub_module)
    
    stylized_image = get_stylized_image(outputs)
    return stylized_image

def process_image(content_image,style_image,hub_module): 
    start_time = tf.timestamp()
    content_image = tf.image.resize(content_image, [224, 224])
    style_image = tf.image.resize(style_image, [224, 224])
    outputs = hub_module(
        tf.constant(content_image),
        tf.constant(style_image)
    )
  
    end_time = tf.timestamp()
    processing_time : float = float(end_time - start_time)
    print(f"Stylizing completed in {processing_time:.2f} seconds...")
    return outputs
def get_stylized_image(outputs):
    output_image = outputs[0]
    # reshape the stylized image
    stylized_image = np.array(output_image)
    generated_image = stylized_image.reshape(
        stylized_image.shape[1], stylized_image.shape[2], stylized_image.shape[3])
    return generated_image