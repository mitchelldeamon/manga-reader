import sys
import os
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt


class MangaReader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Right-to-Left Manga Reader")
        self.setGeometry(0, 0, 900, 1350)

        # Initialize variables
        self.images = []
        self.current_index = 0
        self.dark_mode = False

        # Set up UI components
        self.layout = QVBoxLayout()
        self.init_ui()

        # Set the main layout
        self.setLayout(self.layout)

    def init_ui(self):
        """Initialize the UI layout and components."""
        # Image display label
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label, stretch=1)

        # Create a horizontal layout for buttons
        btn_layout = QHBoxLayout()

        # Load Images button
        load_button = self.create_button(
            "Choose Volume or Chapter", self.load_images)
        btn_layout.addWidget(load_button)

        # Next and Previous buttons for navigation
        btn_layout.addWidget(self.create_button("Next", self.show_next_image))
        btn_layout.addWidget(self.create_button(
            "Previous", self.show_previous_image))

        # Dark Mode toggle button
        btn_layout.addWidget(self.create_button(
            "Toggle Dark Mode", self.toggle_dark_mode))

        # Add the button layout at the bottom
        self.layout.addLayout(btn_layout)

        # Status bar to show current page info
        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)

    def create_button(self, text, function):
        """Create a button with specified text and function."""
        button = QPushButton(text)
        button.clicked.connect(function)
        button.setStyleSheet("QPushButton { color: black; }")
        button.setFocusPolicy(Qt.NoFocus)
        return button

    def load_images(self):
        """Load images from a selected folder and sort them numerically."""
        folder = QFileDialog.getExistingDirectory(self, "Select Volume Folder")
        if folder:
            # Include both .jpg and .png images
            self.images = sorted(
                [os.path.join(folder, img) for img in os.listdir(folder)
                 if img.lower().endswith(('.jpg', '.png'))],
                key=lambda x: int(re.search(r'page_(\d+)', x).group(1)
                                  ) if re.search(r'page_(\d+)', x) else float('inf')
            )
            if self.images:
                self.current_index = 0  # Start from the first page
                self.show_image(self.current_index)

    def show_image(self, index):
        """Display the image at the specified index."""
        if 0 <= index < len(self.images):
            try:
                pixmap = QPixmap(self.images[index])
                self.display_pixmap(pixmap)
                self.current_index = index
                self.update_status_bar()
            except Exception as e:
                self.status_bar.showMessage(f"Error loading image: {e}")

    def display_pixmap(self, pixmap):
        """Resize pixmap to fit label while maintaining aspect ratio."""
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """Adjust the image display when the window is resized."""
        if self.images:  # Ensure images are loaded
            pixmap = QPixmap(self.images[self.current_index])
            self.display_pixmap(pixmap)

    def show_next_image(self):
        """Move forward to the next image."""
        if self.current_index < len(self.images) - 1:
            self.show_image(self.current_index + 1)

    def show_previous_image(self):
        """Move backward to the previous image."""
        if self.current_index > 0:
            self.show_image(self.current_index - 1)

    def keyPressEvent(self, event):
        """Override key press events for left/right arrow navigation."""
        if event.key() == Qt.Key_Left:  # Left arrow moves forward (next)
            self.show_next_image()
        elif event.key() == Qt.Key_Right:  # Right arrow moves backward (previous)
            self.show_previous_image()

    def update_status_bar(self):
        """Update status bar with the current page information."""
        self.status_bar.showMessage(
            f"Page {self.current_index + 1} of {len(self.images)}")

    def toggle_dark_mode(self):
        """Toggle between light and dark modes."""
        dark_palette = QPalette()
        if self.dark_mode:
            self.setPalette(QApplication.palette())  # Light mode
        else:
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            self.setPalette(dark_palette)  # Dark mode
        self.dark_mode = not self.dark_mode


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = MangaReader()
    reader.show()
    sys.exit(app.exec_())
