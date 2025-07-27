from asyncio import subprocess
import os
import tempfile
def save_ffmpg(output_video_path : str):
    temp_dir = tempfile.mkdtemp()
    converted_video = "temp_video.mp4"
    path = os.path.join(temp_dir, converted_video)
    command = f"ffmpeg -y -i {output_video_path} -c:v libx264 {path}"
    subprocess.call(args=command.split(" "))
    return path
