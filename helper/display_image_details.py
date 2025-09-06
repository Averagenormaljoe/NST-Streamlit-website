import streamlit as st
def display_image_details(image):
    try:
        if image is not None:
            st.subheader("Image Details")
            st.write(f"Extension: {image.format}")
            st.write(f"Width: {image.size[0]} Height: {image.size[1]}")

    except Exception as e:
        print(f"Error: Failed to display image details {e}")
        st.error("Failed to display the details of the uploaded image.")