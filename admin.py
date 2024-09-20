import os
import zipfile
import shutil
from PIL import Image
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import io
import time

# Function to zip the entire project folder
def zip_project_folder(project_path, project_name):
    zip_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Admin-tool', f"{project_name}-full")  # Save to Desktop/Admin-tool
    shutil.make_archive(zip_path, 'zip', project_path)  # Create the zip file
    print(f"Project folder zipped at: {zip_path}.zip")

# Function to take a screenshot of index.html
def take_screenshot(project_path, project_name):
    options = Options()
    options.headless = True
    driver_path = 'C:/Users/sudha/Downloads/edgedriver_win64/msedgedriver.exe'
    driver = webdriver.Edge(service=EdgeService(executable_path=driver_path), options=options)

    html_path = f"file://{os.path.join(project_path, 'index.html')}"
    print(f"Opening URL: {html_path}")
    driver.get(html_path)

    # Allow some time for the page to fully load
    time.sleep(10)

    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    img = Image.open(io.BytesIO(screenshot))

    # Crop the image to 16:9 ratio centered
    width, height = img.size
    target_ratio = 16 / 9
    target_width = width
    target_height = int(width / target_ratio)

    if target_height > height:
        target_height = height
        target_width = int(height * target_ratio)

    left = (width - target_width) / 2
    top = (height - target_height) / 2
    right = (width + target_width) / 2
    bottom = (height + target_height) / 2
    img = img.crop((left, top, right, bottom))

    # Resize the image to 1280x720
    img = img.resize((1280, 720), Image.LANCZOS)

    screenshot_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Admin-tool', f"{project_name}.png")
    img.save(screenshot_path)
    if os.path.exists(screenshot_path):
        print(f"Screenshot saved at: {screenshot_path}")
    else:
        print(f"Screenshot not found at: {screenshot_path}")


# Function to zip the image folder
def zip_image_folder(project_path, project_name):
    image_folder = os.path.join(project_path, 'image')
    if os.path.exists(image_folder):
        zip_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Admin-tool', f"{project_name}-assets")  # Save to Desktop/Admin-tool
        shutil.make_archive(zip_path, 'zip', image_folder)  # Create the zip file
        print(f"Image folder zipped at: {zip_path}.zip")

# Function to convert HTML and CSS files to TXT
def convert_to_txt(project_path, project_name):
    for file_name in ['index.html', 'style.css']:
        file_path = os.path.join(project_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()

            txt_name = f"{project_name.lower()}-html.txt" if file_name == 'index.html' else f"{project_name.lower()}-css.txt"
            txt_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Admin-tool', txt_name)  # Save to Desktop/Admin-tool
            with open(txt_path, 'w') as txt_file:
                txt_file.write(content)
            print(f"Converted {file_name} to: {txt_path}")

# Function to create the Output folder and move all files
def create_output_folder_and_move_files(project_path, project_name):
    output_folder = os.path.join('C:/Users/sudha/OneDrive/Desktop/Admin-tool', 'Output')
    os.makedirs(output_folder, exist_ok=True)
    
    # List of files to move
    files_to_move = [
        f"{project_name}-full.zip",
        f"{project_name}.png",
        f"{project_name}-assets.zip",
        f"{project_name.lower()}-html.txt",
        f"{project_name.lower()}-css.txt"
    ]

    for file_name in files_to_move:
        file_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Admin-tool', file_name)
        if os.path.exists(file_path):
            shutil.move(file_path, os.path.join(output_folder, file_name))
            print(f"Moved {file_name} to Output folder.")

# Main function
def process_project(project_path, project_name):
    zip_project_folder(project_path, project_name)
    take_screenshot(project_path, project_name)
    zip_image_folder(project_path, project_name)
    convert_to_txt(project_path, project_name)
    create_output_folder_and_move_files(project_path, project_name)

# Example usage
project_path = 'C:/Users/sudha/OneDrive/Desktop/Files/Coding Project Final/Social-media-links'
project_name = 'Social-media-links-button'
process_project(project_path, project_name)


# python admin.py

