# CClibsExtractor
"""
Adobe CC Library Extractor

This Python script extracts and organizes files from an Adobe Creative Cloud Library (.cclibs) archive. It reads the manifest file, preserves the original folder structure and file names, and creates a new directory named after the library with the current date. The script handles nested group hierarchies and ensures unique filenames to avoid conflicts. After extraction, it cleans up temporary files, providing a streamlined way to access and manage Adobe CC Library assets.

Key features:
- Extracts .cclibs archives
- Maintains original folder structure and file names
- Handles nested group hierarchies
- Ensures unique filenames
- Creates date-stamped output directory
- Cleans up temporary files after extraction

This script is based on the work of https://github.com/Sensibo/cclib_utils/blob/master/ccutil.py, with modifications and improvements to suit specific requirements.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import zipfile
import datetime

def extract_archive(archive_path, extract_path):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def parse_manifest(path):
    with open(os.path.join(path, "manifest"), "r") as f:
        return json.load(f)

def get_group_hierarchy(element, groups):
    hierarchy = []
    if "library#groups" in element:
        group_id = next(iter(element["library#groups"].keys()), "").split("#")[-1]
        while group_id:
            group = groups.get(group_id, {})
            hierarchy.insert(0, group.get("name", "Ungrouped"))
            group_id = group.get("library#parentId")
    return hierarchy if hierarchy else ["Ungrouped"]

def extract_cclib(cclib_path, dest_folder):
    manifest = parse_manifest(cclib_path)
    
    # Créer le dossier de destination
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    
    # Extraire les groupes
    groups = {group["id"]: group for child in manifest["children"] if child["name"] == "groups" for group in child["children"]}
    
    # Extraire les éléments
    elements = [element for child in manifest["children"] if child["name"] == "elements" for element in child["children"]]
    
    for element in elements:
        element_path = os.path.join(cclib_path, element["path"])
        if not os.path.exists(element_path):
            continue
        
        # Obtenir la hiérarchie des dossiers pour cet élément
        folder_hierarchy = get_group_hierarchy(element, groups)
        
        # Créer le chemin complet du dossier
        full_folder_path = os.path.join(dest_folder, *folder_hierarchy)
        Path(full_folder_path).mkdir(parents=True, exist_ok=True)
        
        # Copier chaque composant de l'élément
        for component in element.get("components", []):
            src_file = os.path.join(element_path, component["path"])
            dest_file = os.path.join(full_folder_path, element["name"] + os.path.splitext(component["name"])[-1])
            dest_file = get_unique_filename(dest_file)
            if os.path.exists(src_file):
                shutil.copyfile(src_file, dest_file)

def get_unique_filename(filename):
    if not os.path.exists(filename):
        return filename
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"

def main():
    parser = argparse.ArgumentParser(description="Extraire une archive .cclibs d'Adobe")
    parser.add_argument("cclib_archive", help="Chemin vers l'archive .cclibs")
    args = parser.parse_args()

    # Créer un dossier temporaire pour l'extraction
    temp_dir = "temp_cclib_extract"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Extraire l'archive
        extract_archive(args.cclib_archive, temp_dir)

        # Lire le manifest
        manifest = parse_manifest(temp_dir)

        # Créer le nom du dossier de sortie
        library_name = manifest.get("name", "UnknownLibrary")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        output_folder = f"{library_name}_{current_date}"

        # Exécuter l'extraction
        extract_cclib(temp_dir, output_folder)

        print(f"Extraction terminée. Les fichiers ont été extraits dans le dossier : {output_folder}")

    finally:
        # Nettoyer le dossier temporaire
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
