import os
import shutil
import json
import random
import re
from PIL import Image
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import io
import time
from datetime import datetime

def generate_random_suffix(length=5):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def generate_unique_id(category, short_name):
    
    short_name_initials = ''.join(word[0].upper() for word in short_name.split())

    
    current_date = datetime.now().strftime('%Y%m%d')

    
    random_suffix = generate_random_suffix()

    
    professional_id = f"{category.upper()}-{short_name_initials}-{current_date}-{random_suffix}"

    return professional_id

def copy_project_folder(project_path, project_id, destination_folder):
    new_project_path = os.path.join(destination_folder, project_id)
    shutil.copytree(project_path, new_project_path)
    print(f"\nProject folder copied to: {new_project_path}")
    return new_project_path

def zip_project_folder(project_path, project_id):
    zip_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', f"{project_id}-full")
    shutil.make_archive(zip_path, 'zip', project_path)
    print(f"\nProject folder zipped at: {zip_path}.zip")

def take_screenshot(project_path, project_name):
    options = Options()
    options.headless = True
    driver_path = 'C:/Users/sudha/Downloads/edgedriver_win64/msedgedriver.exe'
    driver = webdriver.Edge(service=EdgeService(executable_path=driver_path), options=options)

    html_path = f"file://{os.path.join(project_path, 'index.html')}"
    print(f"Opening URL: {html_path}")
    driver.get(html_path)

    
    time.sleep(15)

    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    img = Image.open(io.BytesIO(screenshot))

    
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

    
    img = img.resize((1280, 720), Image.LANCZOS)

    screenshot_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', f"{project_name}.png")
    img.save(screenshot_path)
    if os.path.exists(screenshot_path):
        print(f"Screenshot saved at: {screenshot_path}")
    else:
        print(f"Screenshot not found at: {screenshot_path}")

def zip_image_folder(image_folder, project_id):
    if os.path.exists(image_folder):
        zip_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', f"{project_id}-assets")
        shutil.make_archive(zip_path, 'zip', image_folder)
        print(f"\nImage folder zipped at: {zip_path}.zip")
        return True
    return False

def convert_to_txt(project_path, project_id):
    for file_name in ['index.html', 'style.css', 'script.js']:
        file_path = os.path.join(project_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            if file_name == 'index.html':
                txt_name = f"{project_id}-html.txt"
            elif file_name == 'style.css':
                txt_name = f"{project_id}-css.txt"
            elif file_name == 'script.js':
                txt_name = f"{project_id}-js.txt"
            txt_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', txt_name)
            with open(txt_path, 'w') as txt_file:
                txt_file.write(content)
            print(f"\nConverted {file_name} to: {txt_path}")
        else:
            print(f"\n{file_name} not found in the project, skipping.")

def create_project_metadata(project_id, project_name, short_name, category, files_available, has_assets):
    project_data = {
        project_id: {
            "projectId": project_id,
            "projectName": project_name,
            "shortName": short_name,
            "category": category,
            "filesAvailable": files_available,
            "hasAssets": has_assets,
            "uploadTime": datetime.now().strftime("%B %d, %Y at %I:%M %p")
        }
    }
    
    json_path = 'C:/Users/sudha/OneDrive/Desktop/Project-Manager/project_metadata.json'
    
    
    if os.path.exists(json_path):
        with open(json_path, 'r') as json_file:
            existing_data = json.load(json_file)
        existing_data.update(project_data)
    else:
        existing_data = project_data
    
    with open(json_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
    print(f"\nProject metadata saved to: {json_path}")

def create_project_metadata_js(project_id, project_name, short_name, category, files_available, has_assets):
    js_path = "C:/Users/sudha/OneDrive/Desktop/sudhucodes/js_files/backend/projects.js"
    
    
    new_project_data = {
        "name": project_name,
        "shortName": short_name,
        "projectId": project_id,
        "codeUrl": f"codes/sourcecode.html",
        "hasAssets": has_assets,
        "category": category,
        "availableFiles": files_available
    }

    
    if os.path.exists(js_path):
        
        with open(js_path, 'r') as js_file:
            js_content = js_file.read()

        
        projects_match = re.search(r'const projects\s*=\s*\[(.*?)\];', js_content, re.DOTALL)
        
        if projects_match:
            existing_projects_str = projects_match.group(1).strip()

           
            clean_data = re.sub(r"'", '"', existing_projects_str)
            clean_data = re.sub(r"//.*?\n|/\*.*?\*/", "", clean_data, flags=re.DOTALL)

           
            try:
                projects = json.loads(f"[{clean_data}]")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return
              
           
            projects.insert(0, new_project_data)

           
            formatted_projects = ",\n  ".join([json.dumps(project) for project in projects])
            updated_projects_str = f"const projects = [\n  {formatted_projects}\n];"
            
           
            updated_js_content = js_content.replace(projects_match.group(0), updated_projects_str)
        else:
           
            updated_projects_str = f"const projects = [\n  {json.dumps(new_project_data)}\n];"
            updated_js_content = updated_projects_str
    else:
        
        updated_projects_str = f"const projects = [\n  {json.dumps(new_project_data)}\n];"
        updated_js_content = updated_projects_str

    
    with open(js_path, 'w') as js_file:
        js_file.write(updated_js_content)
    
    print(f"\nProject metadata added to: {js_path}")

def move_files_to_locations(project_id, has_assets):
    if category == 'htmlcss':
        zip_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/Zip/htmlcss'
        html_txt_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/codes/htmlcss_txt_files'
        css_txt_folder = html_txt_folder  
        js_txt_folder = html_txt_folder  
    elif category == 'tailwindCSS':
        zip_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/Zip/tailwindCSS'
        html_txt_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/codes/tailwindCSS_txt_files'
        css_txt_folder = html_txt_folder  
        js_txt_folder = html_txt_folder  
    elif category == 'javascript':
        zip_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/Zip/javascript'
        html_txt_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/codes/javascript_txt_files'
        css_txt_folder = html_txt_folder  
        js_txt_folder = html_txt_folder  
    elif category == 'reactJS':
        zip_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/Zip/reactJS'
        html_txt_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/codes/reactJS_txt_files'
        css_txt_folder = html_txt_folder
        js_txt_folder = html_txt_folder
    else:
        print(f"Category {category} not recognized.")
        return

    screenshot_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/images/thumbnails'
    assets_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/Zip/assets_zip'

    os.makedirs(zip_folder, exist_ok=True)
    os.makedirs(screenshot_folder, exist_ok=True)
    os.makedirs(html_txt_folder, exist_ok=True)
    os.makedirs(css_txt_folder, exist_ok=True)
    os.makedirs(js_txt_folder, exist_ok=True)
    os.makedirs(assets_folder, exist_ok=True)

    files_to_move = [
        (f"{project_id}-full.zip", zip_folder),
        (f"{project_id}.png", screenshot_folder),
        (f"{project_id}-html.txt", html_txt_folder),
    ]

    if os.path.exists(os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', f"{project_id}-css.txt")):
        files_to_move.append((f"{project_id}-css.txt", css_txt_folder))
    if os.path.exists(os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', f"{project_id}-js.txt")):
        files_to_move.append((f"{project_id}-js.txt", js_txt_folder))

    if has_assets:
        files_to_move.append((f"{project_id}-assets.zip", assets_folder))

    for file_name, destination_folder in files_to_move:
        source_path = os.path.join('C:/Users/sudha/OneDrive/Desktop/Project-Manager', file_name)
        if os.path.exists(source_path):
            shutil.move(source_path, os.path.join(destination_folder, file_name))
            print(f"\nMoved {file_name} to {destination_folder}.")
        else:
            print(f"\n{file_name} does not exist in the source directory.")

def confirm_id(professional_id):
    print(f"\nGenerated ID: {professional_id}")
    while True:
        confirmation = input("Is this ID correct? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            return True
        elif confirmation == 'no':
            return False
        else:
            print("Please respond with 'yes' or 'no'.")

def process_project(project_path, project_name, short_name, category, files_available):
    upload_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    while True:
        project_id = generate_unique_id(category, short_name)

        
        if confirm_id(project_id):
            break

    if category == 'htmlcss':
        destination_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/demo/htmlcss'
    elif category == 'tailwindCSS':
        destination_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/demo/tailwindCSS'
    elif category == 'javascript':
        destination_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/demo/javascript'
    elif category == 'reactJS':
        destination_folder = 'C:/Users/sudha/OneDrive/Desktop/sudhucodes/demo/reactJS'
    else:
        print(f"Category {category} not recognized.")
        return
    
    os.makedirs(destination_folder, exist_ok=True)
    copied_project_path = copy_project_folder(project_path, project_id, destination_folder)

    zip_project_folder(copied_project_path, project_id)
    take_screenshot(copied_project_path, project_id)

    image_folder = os.path.join(copied_project_path, 'images')
    has_assets = zip_image_folder(image_folder, project_id)
    
    convert_to_txt(copied_project_path, project_id)
    create_project_metadata(project_id, project_name, short_name, category, files_available, has_assets)
    
    
    create_project_metadata_js(project_id, project_name, short_name, category, files_available, has_assets)
    
    move_files_to_locations(project_id, has_assets)


project_path = 'C:/Users/sudha/OneDrive/Desktop/Files/Coding Project Final/All-in-One Advanced Smart Calculator with Full Functionality'
project_name = 'All-in-One Advanced Smart Calculator with Full Functionality - JavaScript'
short_name = 'Calculator with Full Functionality - JavaScript'
category = 'javascript'
files_available = ['html', "css", "js"]

process_project(project_path, project_name, short_name, category, files_available)