import os
import json

metadata_file_path = 'project_metadata.json'
projects_folder_path = 'C:/Users/sudha/OneDrive/Desktop/Files/Coding Project Final'

with open(metadata_file_path, 'r') as file:
    metadata = json.load(file)

def sanitize_folder_name(name):
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

for project_id, project_details in metadata.items():
    folder_name = project_details['projectId']
    new_name = project_details['projectName']
    
    sanitized_new_name = sanitize_folder_name(new_name)
    
    old_folder_path = os.path.join(projects_folder_path, folder_name)
    new_folder_path = os.path.join(projects_folder_path, sanitized_new_name)
    
    if os.path.exists(old_folder_path):
        os.rename(old_folder_path, new_folder_path)
        print(f'Renamed folder: {old_folder_path} to {new_folder_path}')
    else:
        print(f'Folder not found: {old_folder_path}')