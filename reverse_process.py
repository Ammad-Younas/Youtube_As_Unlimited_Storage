import imageio.v2 as imageio
import os
from PIL import Image


def extract_frame():
    input_video = 'output_video.mp4'

    if os.path.exists('Extracted_Frames') == False:
        os.mkdir('Extracted_Frames')
        

    output_dir = 'Extracted_Frames'

    os.makedirs(output_dir, exist_ok=True)

    reader = imageio.get_reader(input_video)

    for i, frame in enumerate(reader, start=1):
        frame_filename = os.path.join(output_dir, f'frame_{i:04d}.png')
        imageio.imwrite(frame_filename, frame)

    reader.close()


def reverse_file():
    filename = 'output.exe'
    width = 1280
    height = 720
    block_size = 4

    blocks_per_row = width // block_size
    blocks_per_column = height // block_size
    total_blocks_per_frame = blocks_per_row * blocks_per_column

    total_frames = 1
    while True:
        try:
            Image.open(f'Extracted_Frames/frame_{total_frames:04d}.png')
            total_frames += 1
        except FileNotFoundError:
            break

    binary_data = []

    for frame_number in range(1, total_frames):
        frame_image = Image.open(f'Extracted_Frames/frame_{frame_number:04d}.png')
        frame_data = []

        for block_index in range(total_blocks_per_frame):
            block_row = block_index // blocks_per_row
            block_col = block_index % blocks_per_row

            top_left_x = block_col * block_size
            top_left_y = block_row * block_size

            block_pixels = []
            for row in range(block_size):
                for col in range(block_size):
                    pixel_value = frame_image.getpixel((top_left_x + col, top_left_y + row))
                    pixel_value = pixel_value[0]

                    if pixel_value > 127:
                        block_pixels.append('1')
                    else:
                        block_pixels.append('0')

            if block_pixels:
                average_value = sum(int(bit) for bit in block_pixels) / len(block_pixels)
                frame_data.append('1' if average_value > 0.5 else '0')

        binary_data.extend(frame_data)

    byte_data = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = ''.join(binary_data[i:i+8])
        byte_data.append(int(byte, 2))

    with open(filename, 'wb') as f:
        f.write(byte_data)



def remove_extracted_frames():
    if os.path.exists('Extracted_Frames'):
        for file in os.listdir('Extracted_Frames'):
            os.remove(os.path.join('Extracted_Frames', file))
        os.rmdir('Extracted_Frames')


if __name__ == '__main__':
    extract_frame()
    reverse_file()
    remove_extracted_frames()