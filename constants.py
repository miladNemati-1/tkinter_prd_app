import os
import pandas as pd
import pymysql.connections
import pymysql as mdb
from sqlalchemy import create_engine
from code_extra.log_method import setup_logger
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.defining_folder import defining_communication_folder, defining_PsswinFolder, defining_NMRFolder, \
    SearchExperimentFolder


pymysql.install_as_MySQLdb()

my_conn = create_engine("mysql+mysqldb://root@localhost/chemistry")
DRIVE = 'S'
FOLDERS = {'COMMUNICATION': "S:/Sci-Chem/PRD/NMR 112/Automated Platform/Final_LabView_allVIs/PythonCommunication",
           'GPC': 'S:/Sci-Chem/PRD/GPC 112/2018-March/Projects',
           'NMR': 'S:/PROJECTS/DATA',
           'Results': 'S:/Sci-Chem/PRD/NMR 112/Automated Platform'}



FRAME_FG = '#d9d4d4'
logger = setup_logger('App')
Temporary_textfile, Pathlastexp_textfile, CommunicationMainFolder = defining_communication_folder(
    FOLDERS['COMMUNICATION'])



# List of list with entry values for GUI
# [entry (for entry field) , default, parameter name, unit, default value, change (for button)]
SETUP_DEFAULT_VALUES_NMR = [['entry1', 'default1', 'Reactor Volume', 'mL', 0.90, 'change1'],
                            ['entry2', 'default2', 'Dead Volume 1',
                                'mL', 0.52, 'change2'],
                            ['entry3', 'default3', 'Dead Volume 2',
                                'mL', 0.21, 'change3'],
                            ['entry4', 'default4', 'Dead Volume 3',
                                'mL', 0.17, 'change4'],
                            ['entry5', 'default5', 'NMR Interval',
                                'sec', 17, 'change5'],
                            ['entry6', 'default6', 'GPC Interval',
                                'minutes', 5, 'change6'],
                            ['entry7', 'default7', 'Stabilization factor',
                                'x', 1.3, 'change7'],
                            ['entry8', 'default8', 'Dilution Flowrate', 'mL/min', 1.5, 'change8']]

FONTS = {'FONT_NORMAL': ('Ariel', 15),
         'FONT_HEADER': ('Ariel', 30),
         'FONT_BOTTON': ('Ariel', 10),
         'FONT_HEADER_BOLD': ('Ariel', 18, 'bold'),
         'FONT_ENTRY': ('Ariel', 17),
         'FONT_SMALL': ('Ariel', 10),
         'FONT_SMALL_BOLD': ('Ariel', 10, 'bold')}

col_names_parameters = ['Start_min', 'Stop_min', 'Volume', 'StartFR', 'StopFR', 'StabilisationTime', 'DeadVolume1', 'DeadVolume2',
                        'DeadVolume3', 'NMRInterval', 'GPCInterval', 'DilutionFR', 'DeadVolume1(min)', 'DeadVolume2(min)', 'DeadVolume3(min)', 'Mode']
TIMESWEEP_PARAMETERS = pd.DataFrame(columns=col_names_parameters)


# Windows


# MAC
# DRIVE = 'S'


Monomer_Conversion = {"BA": {"monomer peak": 3, "polymer peak": 2}, "EA": {"monomer peak": 3, "polymer peak": 2}, "MA": {
    "monomer peak": 3, "polymer peak": 3}, "MMA": {"monomer peak": 2, "polymer peak": 3}}


Conversion_values = {'monomer_peak': 1, 'polymer_peak': 1}
