# CClibsExtractor

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


## Usage

To use the script, run it from the command line with the path to your .cclibs archive as an argument:

```bash
python CClibsExtractor.py path/to/your_archive.cclibs