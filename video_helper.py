from os import read
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
from cv2.typing import MatLike
#read image, convert to tensor, normalize and resize 
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


#convert tensor to numpy array
def tensor_toimage(tensor):
  tensor =tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0]==1
    tensor=tensor[0]
  return tensor



def open_style_image(style_image):
 
    open_style_im : MatLike = cv2.imread(style_image)
    colored_style_im : MatLike = cv2.cvtColor(open_style_im, cv2.COLOR_BGR2RGB)
    processed_style_im = image_read(colored_style_im)
    
    return processed_style_im
def read_frame(frame,x : int):
    return image_read(frame)[0].shape[x]
def process_video(image):
  
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    style_im = open_style_image(image)

    cap = cv2.VideoCapture("assets/man_at_sea_sliced.mp4")
    #in order to get the size of width and shape of video, we used first frame of video
    ret, frame = cap.read()
    frame_width = read_frame(frame, 1)
    frame_height= read_frame(frame, 0)

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 10, 
                        (frame_width,frame_height))

    while True:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = image_read(frame)
            stylized_frame = hub_model(tf.constant(frame), tf.constant(style_im))[0]
            image = tensor_toimage(stylized_frame)
            out.write(image)
        else:
            break

    cap.release()
    out.release()