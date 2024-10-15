# Project Management Automation Tool  

**Author:** SudhuCodes  
**Description:**  
This automation tool simplifies the process of managing projects, including creating unique project IDs, copying and zipping project folders, taking screenshots of web pages, converting HTML/CSS to text, generating metadata, and organizing files.

---

## Table of Contents  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Functions Overview](#functions-overview)  
- [File Organization](#file-organization)  
- [License](#license)  

---

## Features  
- Generate **unique project IDs** with relevant metadata.  
- Automatically **copy and zip project folders** for easy backup.  
- Take **screenshots** of project webpages with cropping and resizing options.  
- Convert **HTML/CSS files to text** for further documentation or processing.  
- Automatically **generate and update metadata** in JSON and JavaScript files.  
- **Organize files** neatly into categorized directories for better management.

---

## Installation  

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sudhucodes/project-management-tool.git
   cd project-management-tool
   ```

2. **Install dependencies**:
   Ensure you have the following installed:
   - **Python 3.x**
   - **Pillow (PIL)** for image processing:  
     ```bash
     pip install pillow
     ```
   - **Selenium** for web automation:  
     ```bash
     pip install selenium
     ```
   - Download the **Edge WebDriver** that matches your browser version from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

3. **Update paths**:  
   Update the script with paths relevant to your system. For example:
   ```python
   driver_path = 'C:/Users/sudha/Downloads/edgedriver_win64/msedgedriver.exe'
   ```

---

## Usage  

1. **Generate Project ID:**  
   The ID is generated using the category, project short name, and date. Example:
   ```
   HTMLCSS-PT-20241015-AB123
   ```

2. **Copy and Zip Project Folder:**  
   Use this functionality to back up your projects:
   ```bash
   python manage_projects.py
   ```

3. **Screenshot a Web Page:**  
   Save the webpage screenshot at a 16:9 aspect ratio for thumbnail purposes.

4. **Convert HTML/CSS to Text:**  
   This makes it easier to share code snippets as plain text documentation.

---

## Project Structure  
```
/project-management-tool
│
├── Admin-tool/
│   ├── project_metadata.json
│   ├── {project_id}-full.zip
│   ├── {project_id}.png
│   └── {project_id}-html.txt
│
├── sudhucodes/
│   ├── Zip/
│   │   ├── htmlcss/
│   │   ├── tailwindCSS/
│   │   └── javascript/
│   └── codes/
│       └── backend/projects.js
│
└── manage_projects.py
```

---

## Functions Overview  

### 1. `generate_unique_id(category, short_name)`  
**Purpose:**  
Generates a unique ID using the category, project short name, date, and a random suffix.  

**Example Output:**  
```
HTMLCSS-PT-20241015-XYZ12
```

---

### 2. `copy_project_folder(project_path, project_id, destination_folder)`  
**Purpose:**  
Copies the entire project folder to the destination directory and renames it with the project ID.

---

### 3. `zip_project_folder(project_path, project_id)`  
**Purpose:**  
Creates a zip archive of the project folder for backup.

---

### 4. `take_screenshot(project_path, project_name)`  
**Purpose:**  
Uses Selenium to open the project’s `index.html` file and take a screenshot.  
- **Screenshot Size:** Cropped to 1280x720 (16:9 aspect ratio).

---

### 5. `convert_to_txt(project_path, project_id)`  
**Purpose:**  
Converts `index.html` and `style.css` files to `.txt` format.

---

### 6. `create_project_metadata()`  
**Purpose:**  
Creates metadata for each project in JSON and updates the JavaScript project list.

---

### 7. `zip_image_folder(image_folder, project_id)`  
**Purpose:**  
Zips the assets folder if available.

---

### 8. `move_files_to_locations(project_id, has_assets)`  
**Purpose:**  
Moves the zip files, text files, and screenshots to their respective folders based on category.

---

## Example Workflow  

1. **Copy and Zip Project:**  
   The project folder is copied and zipped for backup.

2. **Generate Metadata:**  
   Metadata for the project is added to the JSON and JavaScript files.

3. **Organize Files:**  
   The files are moved to specific folders based on the project category (e.g., `htmlcss`, `tailwindCSS`).

4. **Screenshot Generation:**  
   A thumbnail of the project is generated and saved.

---

## File Organization  

The following directories are created automatically if they don't already exist:

- **Zip Folder:**  
  Stores project backups in zip format.  
  Example: `sudhucodes/Zip/htmlcss/{project_id}-full.zip`

- **Screenshot Folder:**  
  Stores thumbnails.  
  Example: `sudhucodes/images/thumbnails/{project_id}.png`

- **Code Folder:**  
  Contains text versions of HTML/CSS files.  
  Example: `sudhucodes/codes/htmlcss_txt_files/{project_id}-html.txt`

---

## License  
This project is licensed under the **MIT License**.  

---

## Author  
Developed by **SudhuCodes**  
- **GitHub:** [SudhuCodes](https://github.com/sudhucodes)  
- **Instagram:** [@sudhucodes](https://instagram.com/sudhucodes)  
- **Email:** sudhuteam@gmail.com  