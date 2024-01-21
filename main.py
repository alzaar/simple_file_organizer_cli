#!/usr/bin/env python3

import os
import sys
import shutil

class DirectoryError(Exception):
    pass

class DirectoryOrganizer:
    def __init__(self, directory):
        self.directory = directory
        self.file_types = set()

    def is_valid_directory(self):
        if not os.path.isdir(self.directory):
            raise DirectoryError("Invalid directory provided")

    def get_file_types(self):
        for file_name in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, file_name)):
                _, file_extension = os.path.splitext(file_name)
                if file_extension:
                    self.file_types.add(file_extension)

    def create_folders_based_on_file_extensions(self):
        for file_type in self.file_types:
            folder_name = file_type[1:]
            folder_path = os.path.join(self.directory, folder_name)
            try:
                os.mkdir(folder_path)
            except FileExistsError:
                print(f"Folder already exists - folder name: {folder_name}")

    def get_files_directories(self):
        files, directories = [], []

        for item in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, item)):
               files.append(item)
            elif os.path.isdir(item):
                directories.append(item)

        return [files, directories]

    def move_files_to_folders(self):
        files, directories = self.get_files_directories()

        for file in files:
            _, extension = os.path.splitext(file)
            for directory in directories:
                if extension[1:] == directory:
                    file_path = os.path.join(self.directory, file)
                    folder_path = os.path.join(self.directory, directory)
                    shutil.move(file_path, folder_path)
                    break

    def organize(self):
        self.is_valid_directory()
        self.get_file_types()
        self.create_folders_based_on_file_extensions()
        self.move_files_to_folders()


def main():
    if len(sys.argv) != 2:
        raise DirectoryError("Invalid number of arguments provided. Expecting one argument.")
    
    directory = sys.argv[1]
    organizer = DirectoryOrganizer(directory)
    organizer.organize()
    print("Successfully organized files in directory")


if __name__ == "__main__":
    main()

