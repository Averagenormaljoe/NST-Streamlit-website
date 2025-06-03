import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from API import transfer_style


def video_transfer_style(input_video_path : str,style_image_path : str, width : int =256,height : int =256,fps : int =30):

    # Load the style image
    style_image = cv2.imread(style_image_path)
    if style_image is None:
        raise "Could not read style image from {style_image_path}"
    style_image = cv2.resize(style_image, (width, height))
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = tf.image.resize(style_image, (256, 256))
    # Load the video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise "Could not open video file {input_video_path}"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video_path = input_video_path.replace('.mp4', '_styled.mp4')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    # Load the pre-trained model
    hub_module = hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")
    # Process each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame to the desired width and height
        frame = cv2.resize(frame, (width, height))
        # Convert to float32 numpy array and normalize to range [0, 1]
        content_image = frame.astype(np.float32)[np.newaxis, ...] / 255.
        # Stylize the image
        stylized_image = transfer_style(content_image, style_image, hub_module)
        # Convert back to uint8 and write to output video
        stylized_image = (stylized_image * 255).astype(np.uint8)
        out.write(stylized_image[0])
    # Release resources
    cap.release()
    out.release()
    output_video_path = input_video_path.replace('.mp4', '_styled.mp4')
    print(f"Styled video saved to {output_video_path}")
    return output_video_path