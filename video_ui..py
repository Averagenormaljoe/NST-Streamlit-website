def get_video_uploader():
    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=video_types, key="video_uploader"
    )
    return video_file