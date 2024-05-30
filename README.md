# fix-google-fotos-metadata
Python script for fixing the metadata of images obtained from a Google Takeout archive.

This script will parse the metadata json files included in the Google Takeout archive and update the filesystem metadata of the images accordingly.

At the moment, only the creation date  and the modification date of the images are updated.

## Usage
1. Download your Google Takeout archive from [https://takeout.google.com/](https://takeout.google.com/)
2. Extract the archive
3. Run the script with the path to the extracted archive as an argument
    ```console
    python fix_metadata.py "/full/path/to/Google Fotos"
    ```