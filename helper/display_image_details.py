import streamlit as st
def display_image_details(image) -> None:
    try:
        if image is not None:
            st.subheader("Image Details")
            st.write(f"Extension: {image.format}")
            st.write(f"Width: {image.size[0]} Height: {image.size[1]}")
        else:
            st.error("The provided image is none.")
            return
    except Exception as e:
        print(f"Error: Failed to display image details {e}")
        st.error(f"Failed to display the details of the uploaded image. Message: {e}.")