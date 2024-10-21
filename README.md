# Manga Reader Application

This Python project is a simple Manga Reader application that allows users to view manga images from a selected folder. It includes features such as right-to-left navigation, image scaling, and a toggleable dark mode. The application is built using PyQt5 for the GUI and offers a straightforward way to read manga stored locally.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How to Run](#how-to-run)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Additional Notes](#additional-notes)
- [License](#license)

## Prerequisites

1. Python 3.7+ - Make sure Python is installed on your system.
2. PyQt5 - Required for GUI development.
3. OS module - For handling file paths.
4. re module - For regular expressions used in image sorting.

## Setup

### 1. Clone or Download the Repository

Open a `Terminal` window and navigate to your desired directory. Clone the repository to your local machine:

`git clone https://github.com/mitchelldeamon/manga-reader.git`

`cd manga_reader`

### 2. Install the Requirements

Install the required dependencies using pip:

`pip install -r requirements.txt`

### 3. Set Up Image Files

Prepare a folder containing your manga images. The images should be named in the format `page_1.jpg`, `page_2.jpg`, etc., to ensure proper sorting.

## How to Run

To run the Manga Reader application, use the following command:

`python manga_reader.py`

## How It Works

### 1. Load Images:

- Upon launching, the application will prompt you to select a folder containing manga images. It loads the images in numerical order based on their filenames (e.g., `page_1.jpg`, `page_2.jpg`).

### 2. Display Manga Pages:

- The application displays images in a right-to-left reading format, meaning the "Next" button will display the following image in sequence, while the "Previous" button will display the former image.

### 3. Dark Mode:

- You can toggle dark mode using the "Toggle Dark Mode" button, which switches the UI palette to a darker color scheme.

### 4. Key Navigation:

- The application supports keyboard navigation:
  - **Left Arrow Key**: Moves forward (right-to-left).
  - **Right Arrow Key**: Moves backward (right-to-left).

### 5. Progress Tracking:

- Page numbers at the bottom of the window displays the current page number and the total number of pages.

## Troubleshooting

- **Issue: Images not displaying properly.**

  - Solution: Ensure the image filenames follow the correct format (e.g., `page_1.jpg`, `page_2.jpg`), and that the images are in the selected folder.

- **Issue: Dark mode not toggling.**

  - Solution: Verify that PyQt5 is properly installed and that the application is running without errors.

- **Issue: GUI not resizing images.**
  - Solution: Ensure that the images are not corrupted and that they can be opened with standard image viewers.

## Additional Notes

- **Supported Image Formats:** Currently, the application only supports `.jpg` images. You can modify the code to add support for other formats like `.png` if needed.
- **Sorting Mechanism:** Images are sorted based on the numeric part of their filenames to ensure correct page order.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
