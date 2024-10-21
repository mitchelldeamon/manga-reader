import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MangaReader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Right-to-Left Manga Reader")
        self.setGeometry(100, 100, 800, 600)

        # Initialize variables
        self.images = []
        self.current_index = 0

        # Set up UI
        self.layout = QVBoxLayout()
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.btn_layout = QHBoxLayout()

        # Next button on the left, moving forward in the list (page 1 to 2, 3, etc.)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_image)
        self.btn_layout.addWidget(self.next_button)

        # Previous button on the right, moving backward in the list (page 2 to 1, etc.)
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_image)
        self.btn_layout.addWidget(self.prev_button)

        self.layout.addLayout(self.btn_layout)
        self.setLayout(self.layout)

        # Status bar to show current page info
        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)

        # Load images
        self.load_images()

    def load_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Volume Folder")
        if folder:
            # Load images and sort in natural order for reading direction
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

    def show_next_image(self):  # Move forward (page 1 to 2, etc.)
        if self.current_index < len(self.images) - 1:
            self.show_image(self.current_index + 1)

    def show_previous_image(self):  # Move backward (page 2 to 1, etc.)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = MangaReader()
    reader.show()
    sys.exit(app.exec_())
