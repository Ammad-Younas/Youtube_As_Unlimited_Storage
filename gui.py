import os
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QProgressBar, QFrame, QFileDialog, QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QProgressBar, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PIL import Image, ImageDraw
import imageio.v2 as imageio
import sys

class GenerateAndReverse(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Generate And Reverse", self)
        self.label.setGeometry(0, 0, 1400, 50)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; color: white;")
        self.label.setFont(QFont("Times New Roman", 18))

        self.generate_video_frame = QFrame(self)
        self.generate_video_frame.setGeometry(50, 70, 1300, 270)
        self.generate_video_frame.setStyleSheet("background-color: white; border: 2px solid lightgray; border-radius: 23px;")

        self.title_label = QLabel("Generate Video from Images Written By Binary Data", self.generate_video_frame)
        self.title_label.setGeometry(0, 0, 1300, 50)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background-color: black; color: white;")
        self.title_label.setFont(QFont("Times New Roman", 14))

        self.choose_file_entry = QLineEdit(self.generate_video_frame)
        self.choose_file_entry.setGeometry(20, 60, 1000, 40)
        self.choose_file_entry.setPlaceholderText("Choose a file...")
        self.choose_file_entry.setStyleSheet("background-color: none; border: 1px solid lightgray; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: 1px solid black; padding: 7px;")
        self.choose_file_entry.setFont(QFont("Times New Roman", 13))
        self.choose_file_entry.setDisabled(True)

        self.browse_button = QPushButton("Browse", self.generate_video_frame)
        self.browse_button.setGeometry(1050, 60, 200, 40)
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 23px;
                border: 1px solid black;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                border-radius: 23px;
                border: 1px solid black;
            }
        """)
        self.browse_button.setFont(QFont("Times New Roman", 13))
        self.browse_button.setCursor(Qt.PointingHandCursor)
        self.browse_button.clicked.connect(self.choose_file_generate_video)

        self.generate_video = QPushButton("Start Processing...", self.generate_video_frame)
        self.generate_video.setGeometry(20, 110, 200, 40)
        self.generate_video.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 23px;
                border: 1px solid black;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                border-radius: 23px;
                border: 1px solid black;
            }
        """)
        self.generate_video.setFont(QFont("Times New Roman", 12))
        self.generate_video.setCursor(Qt.PointingHandCursor)
        self.generate_video.clicked.connect(self.start_generate_video_thread)

        self.progress_bar = QProgressBar(self.generate_video_frame)
        self.progress_bar.setGeometry(230, 120, 1022, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid lightgray;
                background-color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color:black;
            }
        """)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.reverse_to_original = QFrame(self)
        self.reverse_to_original.setGeometry(50, 400, 1300, 270)
        self.reverse_to_original.setStyleSheet("background-color: white; border: 2px solid lightgray; border-radius: 23px;")

        self.title_label_reverse = QLabel("Reverse To Original", self.reverse_to_original)
        self.title_label_reverse.setGeometry(0, 0, 1300, 50)
        self.title_label_reverse.setAlignment(Qt.AlignCenter)
        self.title_label_reverse.setStyleSheet("background-color: black; color: white;")
        self.title_label_reverse.setFont(QFont("Times New Roman", 14))

        self.choose_file_reverse = QLineEdit(self.reverse_to_original)
        self.choose_file_reverse.setGeometry(20, 60, 1000, 40)
        self.choose_file_reverse.setPlaceholderText("Choose a file...")
        self.choose_file_reverse.setStyleSheet("background-color: none; border: 1px solid lightgray; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: 1px solid black; padding: 10px;")
        self.choose_file_reverse.setFont(QFont("Times New Roman", 13))
        self.choose_file_reverse.setDisabled(True)

        self.browse_reverse = QPushButton("Browse", self.reverse_to_original)
        self.browse_reverse.setGeometry(1050, 60, 200, 40)
        self.browse_reverse.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 23px;
                border: 1px solid black;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                border-radius: 23px;
                border: 1px solid black;
            }
        """)
        self.browse_reverse.setFont(QFont("Times New Roman", 13))
        self.browse_reverse.setCursor(Qt.PointingHandCursor)
        self.browse_reverse.clicked.connect(self.choose_file_reverse_video)

        self.generate_reverse = QPushButton("Start Processing...", self.reverse_to_original)
        self.generate_reverse.setGeometry(20, 110, 200, 40)
        self.generate_reverse.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 23px;
                border: 1px solid black;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
                border-radius: 23px;
                border: 1px solid black;
            }
        """)
        self.generate_reverse.setFont(QFont("Times New Roman", 12))
        self.generate_reverse.setCursor(Qt.PointingHandCursor)
        self.generate_reverse.clicked.connect(self.start_reverse_video_thread)

        self.progress_reverse = QProgressBar(self.reverse_to_original)
        self.progress_reverse.setGeometry(230, 120, 1022, 20)
        self.progress_reverse.setStyleSheet("""
            QProgressBar {
                border: 1px solid lightgray;
                background-color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: black;
            }
        """)
        self.progress_reverse.setValue(0)
        self.progress_reverse.setTextVisible(False)

    def choose_file_generate_video(self):
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "Choose a file")
        if self.file_path:
            self.choose_file_entry.setEnabled(True)
            self.choose_file_entry.setText(self.file_path)
            self.choose_file_entry.setEnabled(False)

    def choose_file_reverse_video(self):
        file_dialog = QFileDialog()
        self.file_path_reverse, _ = file_dialog.getOpenFileName(self, "Choose a file")
        if self.file_path_reverse:
            self.choose_file_reverse.setEnabled(True)
            self.choose_file_reverse.setText(self.file_path_reverse)
            self.choose_file_reverse.setEnabled(False)

    def start_generate_video_thread(self):
        if self.choose_file_entry.text() == '':
            QMessageBox.warning(self, 'Warning', 'Please choose a file first')
        else:
            self.thread = QThread()
            self.worker = GenerateVideoWorker(self.file_path)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.remove_temp_files)
            self.thread.start()

    def start_reverse_video_thread(self):
        if self.choose_file_reverse.text() == '':
            QMessageBox.warning(self, 'Warning', 'Please choose a video which is generated by binary data')
        else:
            self.thread = QThread()
            self.worker = ReverseVideoWorker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.progress.connect(self.progress_reverse.setValue)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.remove_extracted_frames)
            self.thread.start()

    def remove_temp_files(self):
        if os.path.exists('Generated_Images'):
            for file in os.listdir('Generated_Images'):
                os.remove(os.path.join('Generated_Images', file))
            os.rmdir('Generated_Images')
        QMessageBox.information(self, 'Success', 'Video has been generated successfully from binary data')

    def remove_extracted_frames(self):
        if os.path.exists('Extracted_Frames'):
            for file in os.listdir('Extracted_Frames'):
                os.remove(os.path.join('Extracted_Frames', file))
            os.rmdir('Extracted_Frames')
        QMessageBox.information(self, 'Success', 'Orignal file retrieved successfully')

class GenerateVideoWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        with open(self.file_path, 'rb') as f:
            byte_data = f.read()

        binary_data = ''.join(format(byte, '08b') for byte in byte_data)

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

            if not os.path.exists('Generated_Images'):
                os.mkdir('Generated_Images')
            frame_image.save(f'Generated_Images/frame_{frame_number:09d}.png')
            self.progress.emit((frame_number + 1) * 100 // total_frames)

        self.generate_binary_images_video()

    def generate_binary_images_video(self):
        frame_dir = 'Generated_Images'
        frames = sorted([os.path.join(frame_dir, file) for file in os.listdir(frame_dir) if file.endswith('.png')])
        output_video = 'output_video.mp4'
        writer = imageio.get_writer(output_video, fps=30)

        for frame in frames:
            image = imageio.imread(frame)
            writer.append_data(image)
            self.progress.emit((frames.index(frame) + 1) * 100 // len(frames))

        writer.close()
        self.finished.emit()

class ReverseVideoWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        self.extract_frame()
        self.reverse_file()
        self.finished.emit()

    def extract_frame(self):
        input_video = 'output_video.mp4'
        output_dir = 'Extracted_Frames'
        os.makedirs(output_dir, exist_ok=True)

        reader = imageio.get_reader(input_video)
        num_frames = reader.count_frames()

        for i, frame in enumerate(reader, start=1):
            frame_filename = os.path.join(output_dir, f'frame_{i:09d}.png')
            imageio.imwrite(frame_filename, frame)
            self.progress.emit((i * 50) // num_frames)

        reader.close()

    def reverse_file(self):
        filename = 'output.mp4'
        width = 1280
        height = 720
        block_size = 4

        blocks_per_row = width // block_size
        blocks_per_column = height // block_size
        total_blocks_per_frame = blocks_per_row * blocks_per_column

        total_frames = 1
        while True:
            try:
                Image.open(f'Extracted_Frames/frame_{total_frames:09d}.png')
                total_frames += 1
            except FileNotFoundError:
                break

        binary_data = []

        for frame_number in range(1, total_frames):
            frame_image = Image.open(f'Extracted_Frames/frame_{frame_number:09d}.png')
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
            self.progress.emit(50 + (frame_number * 50) // total_frames)

        byte_data = bytearray()
        for i in range(0, len(binary_data), 8):
            byte = ''.join(binary_data[i:i+8])
            byte_data.append(int(byte, 2))

        with open(filename, 'wb') as f:
            f.write(byte_data)



class DataBaseTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Database Tab Content")
        layout.addWidget(self.label)
        self.setLayout(layout)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unlimited Storage")
        
        self.tabs = QTabWidget()
        self.make_reverse_tab = GenerateAndReverse()
        self.database_tab = DataBaseTab()
        
        self.tabs.addTab(self.make_reverse_tab, "Make And Reverse")
        self.tabs.addTab(self.database_tab, "Data Base")
        
        self.setCentralWidget(self.tabs)

        self.setFixedSize(1400, 750)

        


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
