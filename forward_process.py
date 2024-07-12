from PIL import Image, ImageDraw
import os
import imageio.v2 as imageio

def generate_images_of_binary_data():
    filename = 'status.exe'
    with open(filename, 'rb') as f:
        data = f.read()
        binary_data = ''.join(format(byte, '08b') for byte in data)

    width = 1280
    height = 720
    block_size = 4

    blocks_per_row = width // block_size
    blocks_per_column = height // block_size

    total_blocks_per_frame = blocks_per_row * blocks_per_column
    total_bits_per_frame = total_blocks_per_frame
    total_frames = len(binary_data) // total_bits_per_frame + 1

    for frame_number in range(total_frames):
        start_index = frame_number * total_bits_per_frame
        end_index = start_index + total_bits_per_frame
        frame_data = binary_data[start_index:end_index]
        
        frame_image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(frame_image)
        
        for block_index in range(total_bits_per_frame):
            if block_index < len(frame_data):
                binary_value = int(frame_data[block_index])
                color = 'white' if binary_value == 1 else 'black'
                
                block_row = block_index // blocks_per_row
                block_col = block_index % blocks_per_row
                
                top_left_x = block_col * block_size
                top_left_y = block_row * block_size
                
                for row in range(block_size):
                    for col in range(block_size):
                        draw.point((top_left_x + col, top_left_y + row), fill=color)
        
        if os.path.exists('Gnerated_Images') == False:
            os.mkdir('Gnerated_Images')
        frame_image.save(f'Gnerated_Images/frame_{frame_number:04d}.png')



def generate_binary_images_video():
    frame_dir = 'Gnerated_Images'
    frames = sorted([os.path.join(frame_dir, file) for file in os.listdir(frame_dir) if file.endswith('.png')])
    output_video = 'output_video.mp4'
    writer = imageio.get_writer(output_video, fps=30)

    for frame in frames:
        image = imageio.imread(frame)
        writer.append_data(image)

    writer.close()


def remove_temp_files():
    if os.path.exists('Gnerated_Images'):
        for file in os.listdir('Gnerated_Images'):
            os.remove(os.path.join('Gnerated_Images', file))
        os.rmdir('Gnerated_Images')



if __name__ == '__main__':
    generate_images_of_binary_data()
    generate_binary_images_video()
    remove_temp_files()