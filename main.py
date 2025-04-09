import sys
import os
import re
import natsort
import json
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


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

        # Removed self.history_key from here (it's now set in load_images)
        self.reading_history = {}

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

        # # Jump to Page input
        # self.page_input = QLineEdit()
        # self.page_input.setPlaceholderText("Jump to page #")
        # self.page_input.setFixedWidth(100)
        # btn_layout.addWidget(self.page_input)

        # # Jump button
        # jump_btn = QPushButton("Go")
        # jump_btn.clicked.connect(self.jump_to_page)
        # btn_layout.addWidget(jump_btn)

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
        """Load images from multiple folders and load/save history per manga root."""
        parent_folder = QFileDialog.getExistingDirectory(
            self, "Select Manga Folder Containing Chapters")
        if not parent_folder:
            return

        # Set the manga-specific history file and history key
        self.history_key = parent_folder  # Set history_key here
        self.history_file = os.path.join(parent_folder, "reading_history.json")

        image_extensions = ('.jpg', '.png')
        all_images = []

        # Walk through all subfolders to collect images
        for root, dirs, files in os.walk(parent_folder):
            for file in files:
                if file.lower().endswith(image_extensions):
                    all_images.append(os.path.join(root, file))

        self.images = natsort.natsorted(all_images, alg=natsort.ns.IGNORECASE)

        # Load the history specific to this manga root folder
        self.reading_history = self.load_reading_history()

        if self.images:
            first_image_folder = os.path.dirname(self.images[0])
            if self.history_key in self.reading_history:
                saved_index = self.reading_history[self.history_key]
                resume = QMessageBox.question(
                    self, "Resume Reading?",
                    f"Resume from page {saved_index + 1}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                self.current_index = saved_index if resume == QMessageBox.Yes else 0
            else:
                self.current_index = 0

            self.show_image(self.current_index)

    def show_image(self, index):
        """Display the image at the specified index."""
        if 0 <= index < len(self.images):
            try:
                pixmap = QPixmap(self.images[index])
                self.display_pixmap(pixmap)
                self.current_index = index
                self.update_status_bar()
                self.save_reading_history()  # 🔥 Save after displaying
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

    def jump_to_page(self):
        """Jump to a specific page based on user input."""
        try:
            page = int(self.page_input.text()) - 1  # Convert to 0-based index
            if 0 <= page < len(self.images):
                self.show_image(page)
            else:
                self.status_bar.showMessage(
                    f"Page {page + 1} is out of range.")
        except ValueError:
            self.status_bar.showMessage("Invalid page number.")

        # Remove focus from the input field after jumping to the page
        self.page_input.clearFocus()

    def load_reading_history(self):
        """Load reading history from a JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as file:
                    return json.load(file)
            except Exception:
                return {}
        return {}

    def save_reading_history(self):
        """Save the current page index using the manga root folder as key."""
        if self.images:
            self.reading_history[self.history_key] = self.current_index
            try:
                with open(self.history_file, 'w') as file:
                    json.dump(self.reading_history, file, indent=4)
            except Exception as e:
                self.status_bar.showMessage(f"Error saving history: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reader = MangaReader()
    reader.show()
    sys.exit(app.exec_())
