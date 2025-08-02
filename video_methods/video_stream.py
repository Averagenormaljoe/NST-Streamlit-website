        
from fractions import Fraction
import io
import av

def prepare_stream( width: int, height: int,fps):
    output_memory_file = io.BytesIO()
    output = av.open(output_memory_file, mode='w', format='mp4')
    try:
        stream = output.add_stream('h264', rate=Fraction(fps))
    except OverflowError:
        stream = output.add_stream('h264', rate=Fraction(30))
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    return output, stream, output_memory_file

def save_packet(stream, output, frame: av.VideoFrame):
    packet = stream.encode(frame)
    output.mux(packet)
def close_stream(stream,output, output_memory_file: io.BytesIO):
    # flush the stream
    save_packet(stream, output, None)
    output.close()

    output_memory_file.seek(0)

    return output_memory_file
