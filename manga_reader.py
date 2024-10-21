import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt


class MangaReader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Right-to-Left Manga Reader")
        self.setGeometry(100, 100, 800, 600)

        # Initialize variables
        self.images = []
        self.current_index = 0
        self.dark_mode = False

        # Set up UI
        self.layout = QVBoxLayout()
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.btn_layout = QHBoxLayout()

        # Next button on the left, moving forward
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_image)
        self.btn_layout.addWidget(self.next_button)

        # Previous button on the right, moving backward
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_image)
        self.btn_layout.addWidget(self.prev_button)

        self.layout.addLayout(self.btn_layout)

        # Dark mode toggle button
        self.dark_mode_button = QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.layout.addWidget(self.dark_mode_button)

        # Status bar to show current page info
        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)

        self.setLayout(self.layout)

        # Set button stylesheet to keep text black
        self.set_button_stylesheet()

        # Load images
        self.load_images()

    def set_button_stylesheet(self):
        # Set a stylesheet to keep the button text black
        button_style = """
            QPushButton {
                color: black;
            }
        """
        self.next_button.setStyleSheet(button_style)
        self.prev_button.setStyleSheet(button_style)
        self.dark_mode_button.setStyleSheet(button_style)

    def load_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Volume Folder")
        if folder:
            # Load images and sort in natural order
            self.images = sorted([os.path.join(folder, img)
                                  for img in os.listdir(folder)
                                  if img.lower().endswith(('.jpg', '.jpeg', '.png'))])
            if self.images:
                self.current_index = 0  # Start from the first page
                self.show_image(self.current_index)

    def show_image(self, index):
        if 0 <= index < len(self.images):
            pixmap = QPixmap(self.images[index])
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.current_index = index
            self.update_status_bar()

    def show_next_image(self):  # Move forward
        if self.current_index < len(self.images) - 1:
            self.show_image(self.current_index + 1)

    def show_previous_image(self):  # Move backward
        if self.current_index > 0:
            self.show_image(self.current_index - 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:  # Move forward
            self.show_next_image()
        elif event.key() == Qt.Key_Left:  # Move backward
            self.show_previous_image()

    def update_status_bar(self):
        self.status_bar.showMessage(
            f"Page {self.current_index + 1} of {len(self.images)}")

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.BrightText, Qt.red)

        self.setPalette(palette)
        self.dark_mode = True

    def set_light_mode(self):
        self.setPalette(QApplication.palette())  # Reset to default palette
        self.dark_mode = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = MangaReader()
    reader.show()
    sys.exit(app.exec_())
