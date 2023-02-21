from mimetypes import init
import os
from code_extra import Constants
import time
import datetime
import pandas as pd

# get given experiment name
# get current year, day time
# search in current day in automated platform file system for folder with same name
# grab csv file of the experiment name in the folder
# prefill file brawser path


class CSVFileFinder:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name

    def find_experiment_path(self):
        current_time = datetime.datetime.now()
        results_path = Constants.FOLDERS['Results']
        curr_time_path = f"/{str(current_time.year)}/{str(current_time.month)}/{str(current_time.day)}"
        search_path = results_path+curr_time_path
        print(search_path)
        return self.search_for_experiment_folder(search_path)

    def search_for_experiment_folder(self, foldersearchpath):
        for folder in os.listdir(foldersearchpath):
            if folder.split("_")[-1] == self.experiment_name:
                ("fff")
                print(f"{foldersearchpath}/{folder}")
                return self.find_csv_file(f"{foldersearchpath}/{folder}")

    def find_csv_file(self, csvsearchpath):
        print("csvsearchpath")
        print(csvsearchpath)
        for file in os.listdir(csvsearchpath):
            if file.split("_")[0] == self.experiment_name:
                print("csv found")
                return f"{csvsearchpath}/{file}"
