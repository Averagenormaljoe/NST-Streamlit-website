import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image



def video_transfer_style(input_video_path, output_video_path, style_image_path, width=256,height=256,fps=30):

    # Load the pre-trained model from TensorFlow Hub
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Load the content and style images
    content_image = cv2.imread(input_video_path)
    style_image = cv2.imread(style_image_path)

    # Convert images to float32 and normalize
    content_image = tf.image.convert_image_dtype(content_image, dtype=tf.float32)
    style_image = tf.image.convert_image_dtype(style_image, dtype=tf.float32)

    # Resize the style image to match the content image size
    style_image = tf.image.resize(style_image, (content_image.shape[0], content_image.shape[1]))

    # Add batch dimension
    content_image = content_image[tf.newaxis, :]
    style_image = style_image[tf.newaxis, :]

    # Perform style transfer
    stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]

    # Convert the result to uint8 and save it
    stylized_image = tf.image.convert_image_dtype(stylized_image[0], dtype=tf.uint8)
    
    # Save the stylized image
    cv2.imwrite(output_video_path, stylized_image.numpy())