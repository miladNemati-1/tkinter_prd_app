from customtkinter import *
from ctypes import alignment
from re import S
from turtle import pen, width
from regex import R
from sqlalchemy import create_engine
import pymysql.connections
import pymysql as mdb
from time import gmtime, strftime, sleep
from tkinter import CENTER, filedialog
from code_extra.log_method import setup_logger
import pandas as pd
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.defining_folder import defining_communication_folder, defining_PsswinFolder, defining_NMRFolder, \
    SearchExperimentFolder
from tkinter import ttk
import tkinter as tk
import tkinter
import datetime
from email.policy import default
from gc import callbacks
import pymysql
from datetime import datetime
from datetime import timedelta
import os
import save_plots
import UpdateDF_NMRdata
from PIL import Image, ImageTk
from pathlib import Path
from sys import exec_prefix
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import pandas as pd
from ExperimentFolder import findexperimentcsvfile
from code_extra.log_method import setup_logger
from code_extra.defining_folder import defining_communication_folder, defining_PsswinFolder, defining_NMRFolder, SearchExperimentFolder
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.calculateScans import calculate_scans
from code_extra.precheck import check_files, check_Emailconnection
from code_extra.start_experiment import starting
from code_extra import Constants
from code_extra.start_experiment import starting, SearchForNMRfolder, CreateExpDF
from model import isfloat
import UpdateDF_GPCdata
from constants import *
import pandas as pd
from syringepump import SyringePump as Pump
import time

import templates.conversion as conversion_view
import templates.nmr_gpc as nmr_view
import templates.setup as setup_view
import templates.timesweeps as timesweeps_view
import templates.welcome as welcome_view
import templates.pop_up as pop_up_view
import util.csv as csvutil


class View(tk.Tk):

    col_names = ['Start', 'Stop', 'volume', 'StartFR', 'StopFR', 'stabilisation time', 'dead volume 1', 'Dead Volume 2', 'GPC Interval',
                 'Dead Volume 3', 'Dilution FR', 'DeadVolume1(min)', 'DeadVolume2(min)', 'DeadVolume3(min)', 'NMR interval', 'mode']
    parametersDF = pd.DataFrame(columns=col_names)
    wGPC_all_ts_info = []
    experiment_extra = pd.DataFrame(columns=['code', 'Mainfolder', 'GPCfolder', 'Timesweepfolder',
                                             'Infofolder', 'Softwarefolder', 'Rawfolder', 'Plotsfolder', 'COMMUNICATION', 'GPC', 'NMR'])
    Labviewscript = 'GPC-NMR Timesweep_GUIversion_version4_lab112_gpcPC.vi'

    BUTTON_CAPTIONS = ["NMR", "NMR-GPC",
                       "BrowseComm", "BrowseSpin", "BrowsePsswin"]
    PADDING = 100
    PsswinFolder = defining_PsswinFolder(FOLDERS['GPC'])
    NMRFolder = defining_NMRFolder(FOLDERS['NMR'])
    FONTS = {'FONT_NORMAL': ('Ariel', 15),
             'FONT_HEADER': ('Ariel', 30),
             'FONT_BOTTON': ('Ariel', 10),
             'FONT_HEADER_BOLD': ('Ariel', 18, 'bold'),
             'FONT_ENTRY': ('Ariel', 17),
             'FONT_SMALL': ('Ariel', 10),
             'FONT_SMALL_BOLD': ('Ariel', 10, 'bold')}
    chemicals = pd.read_csv('Chemicals/Chemicals.csv')
    reactor_volume = SETUP_DEFAULT_VALUES_NMR[0][4]
    NMRinterval1 = SETUP_DEFAULT_VALUES_NMR[4][4]
    GPCinterval1 = SETUP_DEFAULT_VALUES_NMR[5][4]
    NMRGPC_all_ts_info = []

    # extracts all chemicals by class
    RAFTlist = chemicals[chemicals["class"] == 'RAFT']
    solventlist = chemicals[chemicals["class"] == 'solvent']
    initiatorlist = chemicals[chemicals["class"] == 'initiator']
    monomerlist = chemicals[chemicals["class"] == 'monomer']

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.CommunicationMainFolder = FOLDERS['COMMUNICATION']
        self.controller.set_experiment_folders(self.CommunicationMainFolder)
        self.title("NMR Platform")
        self.geometry(('{}x{}'.format(1000, 750)))
        self.wm_iconbitmap("Pictures/Benchtop NMR.ico")
        self.value_var = tk.StringVar()
        self._create_tabs()
        self._make_main_frame()
        self._make_welcome_screen()
        self._make_NMR_setup_screen()
        self._make_timesweep_frame()
        self._make_conversion_screen()
        self._make_NMRGPC_initialisation_tab()

    def _make_NMR_setup_screen(self):
        setup_view._make_NMR_setup_screen(self)

    def _make_welcome_screen(self):
        welcome_view._make_welcome_screen(self)

    def _make_timesweep_frame(self):
        timesweeps_view._make_timesweep_frame(self)

    def _make_conversion_screen(self):
        conversion_view.make_conversion_screen(self)

    def _make_NMRGPC_initialisation_tab(self):
        nmr_view.initialise_params(self)
        nmr_view._make_NMRGPC_initialisation_tab(self)

    def show_timesweep_info(self):
        timesweeps_view.show_timesweep_info(self)

    def change_values(self):

        nmr_view.change_values(self)

    def select_internal_standard(self):
        conversion_view.select_internal_standard(self)

    def select_monomer(self):
        conversion_view.select_monomer(self)

    def select_solvent(self):
        conversion_view.select_solvent(self)

    def csv_to_GPC_table(self, f):
        csvutil.csv_to_GPC_table(self, f)

    def csv_to_table_nmr(self, f):
        csvutil.csv_to_table_nmr(self, f)

    def upload(self):
        csvutil.upload(self)

    def browseFiles(self):
        csvutil.browseFiles(self)

    def _create_experiment_upload_screen(self):
        nmr_view.create_experiment_upload_screen(self)

    def _upload_results_pop_up(self):
        nmr_view.upload_results_pop_up(self)

    def add_experiment_data(self):
        nmr_view.add_experiment_data(self)

    def startexp(self):
        nmr_view.startexp(self)
    def start(self):
        nmr_view.start(self)

    def db_connect(self):
        nmr_view.db_connect()

    def check_experimentFoldertxtfile(self, expfolder, exp_code):
        nmr_view.check_experimentFoldertxtfile()

    def confirmSpinsolve(self):
        nmr_view.confirmSpinsolve(self)

    def confirm_code(self):
        nmr_view.confirm_code(self)

    def confirmLabview(self):
        nmr_view.confirmLabview(self)

    def Confirm_reactor_parameters(self):
        setup_view.Confirm_reactor_parameters(self)

    def show_final_timesweep_info(self, total_time, total_scan, total_gpc, scan_numbers):
        timesweeps_view.show_final_timesweep_info(
            self, total_time, total_scan, total_gpc, scan_numbers)

    def get_user_experiments(self, v):
        nmr_view.get_user_experiments(self, v)

    def show_user_experiments(self, list, primary_id_list):
        nmr_view.show_user_experiments(self, list, primary_id_list)

    def make_pop_up_tab(self):
        pop_up_view.make_pop_up_tab(self)

    def confirm_emailadress(self):
        nmr_view.confirm_emailadress(self)

    def main(self):
        set_appearance_mode("light")  # Modes: system (default), light, dark
        # Themes: blue (default), dark-blue, green
        set_default_color_theme("blue")
        self.tab.select(self.welcome_tab)
        self.mainloop()

    def _create_tabs(self):
        self.tab = ttk.Notebook(self, height=800)
        self.welcome_tab = ttk.Frame(self.tab)
        self.welcome_tab.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.tab_overview = ttk.Frame(self.tab)
        self.setup = ttk.Frame(self.tab)
        self.tab_experiment = ttk.Frame(self.tab)
        self.tab_NMR = ttk.Frame(self.tab)
        self.tab_NMR_GPC = ttk.Frame(self.tab)
        self.tab_NMRGPC_Setup = ttk.Frame(self.tab)
        self.tab_NMRGPC_Timesweeps = ttk.Frame(self.tab)
        self.tab_NMRGPC_Conversion = Frame(self.tab, width=900, height=600)
        self.tab_NMRGPC_Initialisation = Frame(self.tab, width=550, height=550)
        self.tab_NMRGPC_Conversion.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.upload_screen = ttk.Frame(self.tab)
        self.upload_pop_up = ttk.Frame(self.tab)
        self.tab.add(self.tab_NMRGPC_Timesweeps, text='Timesweeps')
        self.tab.add(self.tab_NMRGPC_Conversion, text="Conversion")
        self.tab.add(self.welcome_tab, text="Welcome")
        self.tab.add(self.setup, text="Setup")
        self.tab.add(self.tab_NMRGPC_Initialisation, text="NMR GPC Init")
        self.tab_NMR_Setup = ttk.Frame(self.tab)
        self.tab_NMR_Timesweeps = ttk.Frame(self.tab)
        self.tab_NMR_Conversion = ttk.Frame(self.tab)
        self.tab_NMR_Initialisation = ttk.Frame(self.tab)
        self.tab.pack(expand=True, fill='both')

    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.pack(padx=self.PADDING, pady=self.PADDING, expand=True)

    def make_solution_summary_view(self, summary_string):
        solution_summary = CTkLabel(self.NMRGPC_setup_parameter_frame, text='Reaction Solution', bg_color='gray',
                                    font=FONTS['FONT_NORMAL'], pady=20)
        solution_summary.grid(row=8, column=0, columnspan=2, rowspan=2)
        solution_summary.configure(text=summary_string)

    def go_to_tab(self, next_tab):
        self.tab.select(next_tab)

    def change_parameter_view_values(self):
        for i, parameter in enumerate(SETUP_DEFAULT_VALUES_NMR):
            parameter[1] = CTkLabel(self.NMRGPC_setup_parameter_frame, text=parameter[4], bg_color='gray',
                                    width=20)  # changes value in GUI
            parameter[1].configure(font=View.FONTS['FONT_NORMAL'], anchor='e')
            parameter[1].grid(row=i, column=4)

    def show_warning(self, error_message="Please enter a valid floating point number for all fields"):
        warning = tk.Toplevel(self)
        warning.title("Incorrect entry")
        header_wrong_input = CTkLabel(warning, text=error_message,
                                      bg_color='white', font=self.FONTS['FONT_HEADER'])
        header_wrong_input.grid(padx=5, pady=5)
        exit_button = CTkButton(warning, text="Exit", command=warning.destroy)
        exit_button.grid()

    def clear_fields(self, *args):
        for field in args:
            field.delete(0, 'end')

    def _set_conversion_formula(self, monomer_key):
        Constants.Conversion_values = Constants.Monomer_Conversion[monomer_key]

    def indent_conversion_elements(self, label):
        label.config(padx=(0, 20), pady=(0, 5))

    def HelpLabView(self):
        return

    def HelpPss(self):
        self.labelPssInfo.configure(text='Pss Check')
        logger.info('Psswin is okay')
        self.labelSpinsolve.configure(
            text='Name the experiment ({}) in the Spinsolve software.'.format(self.code_en.get()))
        self.confirmpss.configure(state='disabled')
        self.Helppss.configure(state='disabled')
        self.confirmspinsolve.configure(state='normal')
        self.Helpspinsolve.configure(state='normal')

    def HelpSpinsolve(self):
        return

    def confirmPss(self):
        self.labelPssInfo.configure(text='Pss Check')
        logger.info('Psswin is okay')
        self.labelSpinsolve.configure(
            text='Name the experiment ({}) in the Spinsolve software.'.format(self.code_en))
        self.confirmpss.configure(state='disabled')
        self.Helppss.configure(state='disabled')
        self.confirmspinsolve.configure(state='normal')
        self.Helpspinsolve.configure(state='normal')

    def button_spacing(self, button):
        button.pack(pady=(0, 10))
