import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS


def get_date_taken(path):
    image = Image.open(path)
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'DateTimeOriginal':
                return value
    return None


def create_directory_structure(base_dir, year, month):
    year_dir = os.path.join(base_dir, year)
    month_dir = os.path.join(year_dir, month)
    if not os.path.exists(year_dir):
        print("Create directory {}".format(year_dir))
        os.mkdir(year_dir)
    if not os.path.exists(month_dir):
        print("Create directory {}".format(month_dir))
        os.mkdir(month_dir)
    return month_dir


def sort_jpg_files(base_dir):
    for file_name in os.listdir(base_dir):
        if (file_name.lower().endswith('.jpg')
                or file_name.lower().endswith('.jpeg')
                or file_name.lower().endswith('.JPG')):
            file_path = os.path.join(base_dir, file_name)
            date_taken = get_date_taken(file_path)
            if date_taken:
                year, month = date_taken.split(':')[0], date_taken.split(':')[1]
                target_dir = create_directory_structure(base_dir, year, month)
                shutil.move(file_path, os.path.join(target_dir, file_name))
                print(f"Moved {file_name} to {target_dir}")
            else:
                print(f"No date taken info for {file_name}")


if __name__ == "__main__":
    directory = r"\\192.168.1.14\photo\Sauvegarde auto"
    sort_jpg_files(directory)
