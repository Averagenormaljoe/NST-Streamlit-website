import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


def transfer_style(content_image, style_image, model_path ):

    """
    :param content_image: content image as numpy array
    :param style_image: style image as numpy array
    :param model_path: path to the downloaded pre-trained model.

    The 'model' directory already contains the downloaded pre-trained model,but 
    you can also download the pre-trained model from the below TF HUB link:
    https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2

    :return: A Styled image as 3D numpy array.

    """

    #--------------------------------------------------------------

    # resize the images to (1000,1000) if greater than (2000 x 2000)

    size_threshold = 2000
    resizing_shape = (1000,1000)
    resize_style_shape = (256,256)
    content_shape = content_image.shape
    style_shape = style_image.shape

    resize_content = True if content_shape[0] > size_threshold or content_shape[1] > size_threshold else False
    resize_style = True if style_shape[0] > size_threshold or style_shape[1] > size_threshold else False

    if resize_content is True:
        print("Content Image bigger than (2000x2000), resizing to (1000x1000)")
        content_image = cv2.resize(content_image,(resizing_shape[0],resizing_shape[1]))
        content_image = np.array(content_image)
    
    if resize_style is True :
        print("Style Image bigger than (2000x2000), resizing to (1000x1000)")
        style_image = cv2.resize(style_image,(resizing_shape[0],resizing_shape[1]))
        style_image = np.array(style_image)

    #--------------------------------------------------------------


    print("Resizing and Normalizing images...")
    # Convert to float32 numpy array, add batch dimension, and normalize to range [0, 1]. Example using numpy:
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.

    # Optionally resize the images. It is recommended that the style image is about
    # 256 pixels (this size was used when training the style transfer network).
    # The content image can be any size.
    style_image = tf.image.resize(style_image, resize_style_shape)

    print("Loading pre-trained model...")
    # The hub.load() loads any TF Hub model
    hub_module = hub.load(model_path)

    print("Generating stylized image now...wait a minute")
    # Stylize image.
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]

    # reshape the stylized image
    stylized_image = np.array(stylized_image)
    stylized_image = stylized_image.reshape(
        stylized_image.shape[1], stylized_image.shape[2], stylized_image.shape[3])

    print("Stylizing completed...")
    return stylized_image



def webcam_input(style_model_name):
    st.header("Webcam Live Feed")
    WIDTH = st.sidebar.select_slider('QUALITY (May reduce the speed)', list(range(150, 501, 50)))
    width = WIDTH

    @st_session_memo
    def load_model(model_name, width):  # `width` is not used when loading the model, but is necessary as a cache key.
        return get_model_from_path(model_name)

    model = load_model(style_models_dict[style_model_name], width)

    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")

        if model is None:
            return image

        orig_h, orig_w = image.shape[0:2]

        # cv2.resize used in a forked thread may cause memory leaks
        input = np.asarray(Image.fromarray(image).resize((width, int(width * orig_h / orig_w))))

        transferred = style_transfer(input, model)

        result = Image.fromarray((transferred * 255).astype(np.uint8))
        image = np.asarray(result.resize((orig_w, orig_h)))
        return av.VideoFrame.from_ndarray(image, format="bgr24")

    ctx = webrtc_streamer(
        key="neural-style-transfer",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": get_ice_servers()},
        media_stream_constraints={"video": True, "audio": False},
    )