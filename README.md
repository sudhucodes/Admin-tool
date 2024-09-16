# Project Automation Script for Netflix Login Page

This Python script automates several essential tasks for web development projects, particularly aimed at packaging and organizing project assets for delivery or archiving. The script handles various operations such as zipping the entire project, taking screenshots, converting files, and organizing the output into a well-structured folder.

## Features

1. **Zips the Entire Project Folder**  
   The script compresses the entire project folder (`Your-Project-Folder`) into a `.zip` file with a `-full` suffix, saving it in a temporary location.

2. **Captures a Screenshot of the Project**  
   A screenshot of the `index.html` file is taken using Selenium and saved in PNG format with the specified dimensions (1280x720). This feature is useful for creating quick project previews or for documentation purposes.

3. **Zips the Image Folder**  
   The `image` folder within the project is compressed into a separate `.zip` file named `-assets.zip`. This allows easy packaging of all image assets for delivery.

4. **Converts HTML and CSS Files to TXT Format**  
   Both the `index.html` and `style.css` files are converted to `.txt` files. The output is named `projectname-html.txt` and `projectname-css.txt`, ensuring all relevant files are stored in a simple, readable format.

5. **Creates an Organized Output Folder**  
   After all operations are complete, the script creates an `Output` folder and moves all the generated files (zipped project, screenshot, asset zip, and txt files) into it, maintaining a clean and organized project structure.

## How It Works

The script performs the following steps:

1. **Zip the Main Project Folder**  
   Compress the entire `Your-Project-Folder` into a `.zip` archive named `<ProjectName>-full.zip`.

2. **Take a Screenshot of the Project**  
   Using Selenium and the Edge WebDriver, open the `index.html` file, wait for the page to load, and capture a screenshot. The image is resized and saved in the desired location.

3. **Zip the Image Folder**  
   Look for the `image` folder within the project and zip its contents into a separate `.zip` file, named `<ProjectName>-assets.zip`.

4. **Convert HTML and CSS to TXT**  
   Read the HTML (`index.html`) and CSS (`style.css`) files and save them as `.txt` files with appropriate naming conventions.

5. **Move Files to Output Folder**  
   Move all created files to an `Output` folder for easy access and organization.

## Requirements

- Python 3.x
- Selenium (`pip install selenium`)
- PIL (Python Imaging Library) (`pip install pillow`)
- Microsoft Edge WebDriver


**SudhuCodes.**
By ~ SUDHANSHU