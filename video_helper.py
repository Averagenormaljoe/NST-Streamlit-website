from os import read
import tensorflow as tf
from helper import get_model_path
import tensorflow_hub as hub
import numpy as np
import cv2
from cv2.typing import MatLike

def image_read(image : MatLike):
  max_dim : int =512
  image_tensor : tf.Tensor = tf.convert_to_tensor(image, dtype = tf.float32)
  image_tensor_reduced = image_tensor /255.0
  shape = tf.cast(tf.shape(image_tensor_reduced)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim/long_dim
  new_shape = tf.cast(shape*scale, tf.int32)
  new_image = tf.image.resize(image, new_shape)
  new_image = new_image[tf.newaxis, :]
  
  return new_image




def open_style_image(style_image):
 
    open_style_im : MatLike = cv2.imread(style_image)
    colored_style_im : MatLike = cv2.cvtColor(open_style_im, cv2.COLOR_BGR2RGB)
    processed_style_im = image_read(colored_style_im)
    
    return processed_style_im
