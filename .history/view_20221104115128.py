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


pymysql.install_as_MySQLdb()

my_conn = create_engine("mysql+mysqldb://root@localhost/chemistry")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chemistry',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
logger = setup_logger('App')
Temporary_textfile, Pathlastexp_textfile, CommunicationMainFolder = defining_communication_folder(
    FOLDERS['COMMUNICATION'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chemistry',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


class View(tk.Tk):
    """"""
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
             'FONT_HEADER': ('Courier', 30),
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
        self._make_NMR_setup_screen()
        self._make_welcome_screen()
        self._make_timesweep_frame()
        self._make_conversion_screen()
        self._get_user_names()
        self._make_NMRGPC_initialisation_tab()
        # self._upload_results_pop_up()
        # self._create_experiment_upload_screen()

    def main(self):
        self.tab.select(self.welcome_tab)
        self.mainloop()

    def _create_tabs(self):
        self.tab = ttk.Notebook(self)
        self.welcome_tab = ttk.Frame(self.tab)
        self.tab_overview = ttk.Frame(self.tab)
        self.setup = ttk.Frame(self.tab)
        self.tab_experiment = ttk.Frame(self.tab)
        self.tab_NMR = ttk.Frame(self.tab)
        self.tab_NMR_GPC = ttk.Frame(self.tab)

        self.tab_NMRGPC_Setup = ttk.Frame(self.tab)
        self.tab_NMRGPC_Timesweeps = ttk.Frame(self.tab)
        self.tab_NMRGPC_Conversion = ttk.Frame(self.tab)
        self.tab_NMRGPC_Initialisation = ttk.Frame(self.tab)
        self.upload_screen = ttk.Frame(self.tab)
        self.upload_pop_up = ttk.Frame(self.tab)

        self.tab.add(self.tab_NMRGPC_Timesweeps, text='Timesweeps')

        self.tab.add(self.tab_NMRGPC_Conversion, text="Conversion")

        self.tab.add(self.welcome_tab, text="Welcome")
        self.tab.add(self.setup, text="Setup")
        self.tab.add(self.tab_NMRGPC_Initialisation, text="NMR GPC Init")
        # self.tab.add(self.upload_screen, text="Upload Results")
        # self.tab.add(self.upload_pop_up, text="Upload Results Pop up")
        self.tab_NMR_Setup = ttk.Frame(self.tab)
        self.tab_NMR_Timesweeps = ttk.Frame(self.tab)
        self.tab_NMR_Conversion = ttk.Frame(self.tab)
        self.tab_NMR_Initialisation = ttk.Frame(self.tab)

        self.tab.grid()

    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.grid(padx=self.PADDING, pady=self.PADDING)

    def _make_timesweep_frame(self):
        NMRGPC_timesweep_top_frame = tk.Frame(self.tab_NMRGPC_Timesweeps, bg='white', width=1000, height=50, pady=3,
                                              padx=400)
        NMRGPC_timesweep_top_frame.grid(row=0, sticky="ew")
        NMRGPC_timesweep_picture_frame = tk.Frame(self.tab_NMRGPC_Timesweeps, bg='white', width=1000, height=300,
                                                  padx=175,
                                                  pady=3)
        NMRGPC_timesweep_picture_frame.grid(row=1, sticky="nsew")
        self.NMRGPC_timesweep_parameter_frame = tk.Frame(self.tab_NMRGPC_Timesweeps, bg='gray', width=1000, height=350,
                                                         pady=3,
                                                         padx=3)
        self.NMRGPC_timesweep_parameter_frame.grid(row=3, sticky="ew")
        self.NMRGPC_timesweep_confirm_frame = tk.Frame(self.tab_NMRGPC_Timesweeps, bg='gray', width=1000, height=50,
                                                       pady=10,
                                                       padx=10)
        self.NMRGPC_timesweep_confirm_frame.grid(row=4, sticky="ew")

        # Make-Up Top Frame in Timesweep Tab
        NMRGPC_timesweep_header = tk.Label(
            NMRGPC_timesweep_top_frame, text='Timesweeps', bg='white')
        NMRGPC_timesweep_header.config(font=FONTS['FONT_HEADER'])
        NMRGPC_timesweep_header.grid()

        # Make-Up NMRGPC_timesweep_picture_frame in Timsweep Tab
        picture_timesweep = tk.PhotoImage(
            file='Pictures/Timesweeps_pictureFrame.png')
        LabelPicture = tk.Label(
            master=NMRGPC_timesweep_picture_frame, image=picture_timesweep, bg='white')
        LabelPicture.grid(column=2)

        # Make-Up Parameter_frame_timesweep in Timesweep Tab
        NMRGPC_all_ts_info = []  # list where all the timesweeps will be saved

        # extracts reactorvolume, NMR interval and GPC interval from confirmed setup parameters

        tsparam_header = tk.Label(self.NMRGPC_timesweep_parameter_frame, text="Insert Timesweep Parameters", bg='gray',
                                  width=27)
        tsparam_header.config(font=FONTS['FONT_HEADER_BOLD'])
        tsparam_header.grid(row=0, column=1, columnspan=4)

        ts_from_lbl = tk.Label(self.NMRGPC_timesweep_parameter_frame, text='From (minutes)', width=15, bg='gray',
                               font=FONTS['FONT_NORMAL'], anchor='center')
        ts_from_lbl.grid(row=1, column=1, columnspan=2)

        self.ts_from_en = tk.Entry(
            self.NMRGPC_timesweep_parameter_frame, width=5, font=FONTS['FONT_ENTRY'])
        self.ts_from_en.grid(row=2, column=1)

        ts_to_lbl = tk.Label(self.NMRGPC_timesweep_parameter_frame, text='To (minutes)', bg='gray',
                             font=FONTS['FONT_NORMAL'],
                             anchor='center')
        ts_to_lbl.grid(row=1, column=4, columnspan=2)

        ts_to_en = tk.Entry(self.NMRGPC_timesweep_parameter_frame,
                            width=5, font=FONTS['FONT_ENTRY'])
        ts_to_en.grid(row=2, column=4)

        insert_ts_btm = tk.Button(self.NMRGPC_timesweep_parameter_frame, text='Add',
                                  command=lambda timesweep_to=ts_to_en,
                                  timesweep_from=self.ts_from_en: self.controller.add_timesweep(
                                      timesweep_to, timesweep_from),
                                  font=FONTS['FONT_BOTTON'])
        insert_ts_btm.grid(row=3, column=2)

        delete_ts_btm = tk.Button(self.NMRGPC_timesweep_parameter_frame, text='Delete',
                                  command=self.controller.delete_timesweep,
                                  font=FONTS['FONT_BOTTON'])
        delete_ts_btm.grid(row=3, column=3)

        confirmed_ts = tk.Label(
            self.NMRGPC_timesweep_parameter_frame, text='List of Timesweeps', bg='gray')
        confirmed_ts.config(font=FONTS['FONT_HEADER_BOLD'], anchor='w')
        confirmed_ts.grid(row=4, column=0)

        summary_1 = tk.Label(self.NMRGPC_timesweep_confirm_frame,
                             text=' ', width=90, bg='gray', anchor='w', padx=10)
        summary_1.grid(row=1, column=0)

        confirm_ts_btm = tk.Button(self.NMRGPC_timesweep_confirm_frame, text='Confirm', height=3, width=15,
                                   command=self.controller.confirm_timesweep, font=FONTS['FONT_BOTTON'])
        confirm_ts_btm.grid()

    def show_timesweep_info(self):

        # Creates 'List of Timesweeps'
        for i, ts_info in enumerate(self.NMRGPC_all_ts_info):
            ts_info[0] = tk.Label(self.NMRGPC_timesweep_parameter_frame, text=ts_info[1], bg='gray', width=90,
                                  font=FONTS['FONT_SMALL'], anchor='w')

            ts_info[0].grid(row=5 + i, columnspan=5)
            # to_minute of timesweep i is from_minute of timesweep i+1
            entryText = tk.DoubleVar()
            entryText.set(self.NMRGPC_all_ts_info[-1][-1])
            logger.debug(
                'This is the to_minutes varialbe of the last entred timesweep : {}'.format(
                    self.NMRGPC_all_ts_info[-1][-1]))
            self.ts_from_en.configure(textvariable=entryText, state='readonly')

    def temp(self):
        pass

    def make_pop_up_tab(self):
        self.solution_popup = tk.Toplevel()
        self.solution_popup.title('Reaction Solution')

        popuptitle = tk.Label(
            self.solution_popup, text='Reaction Solution', font=FONTS['FONT_HEADER'], padx=15)
        popuptitle.grid(row=0, column=0, columnspan=3)
        # monomer
        mLMonomer = tk.Entry(self.solution_popup)  # Entry in Column 1
        mLMonomer.grid(row=1, column=1)

        optionsMonomer = tk.StringVar()
        optionsMonomer.set('MA')
        MenuMonomer = ttk.OptionMenu(self.solution_popup, optionsMonomer,
                                     *self.monomerlist['abbreviation'])  # Menu in Column 0
        MenuMonomer.grid(row=1, column=0)

        monomerlabel = tk.Label(self.solution_popup,
                                text='mL')  # Unit in column 2
        monomerlabel.grid(row=1, column=2)
        # RAFT
        gramRAFT = tk.Entry(self.solution_popup)
        gramRAFT.grid(row=2, column=1)

        optionsRAFT = tk.StringVar()
        optionsRAFT.set('DoPAT')
        MenuRAFT = tk.OptionMenu(
            self.solution_popup, optionsRAFT, *self.RAFTlist['abbreviation'])
        MenuRAFT.grid(row=2, column=0)

        RAFTlabel = tk.Label(self.solution_popup, text='g')
        RAFTlabel.grid(row=2, column=2)
        # initator
        graminitiator = tk.Entry(self.solution_popup)
        graminitiator.grid(row=3, column=1)

        optionsinitiator = tk.StringVar()
        optionsinitiator.set("AIBN")
        MenuInitiator = tk.OptionMenu(
            self.solution_popup, optionsinitiator, *self.initiatorlist['abbreviation'])
        MenuInitiator.grid(row=3, column=0)

        initiatorlabel = tk.Label(self.solution_popup, text='g')
        initiatorlabel.grid(row=3, column=2)
        # solvent
        mLsolvent = tk.Entry(self.solution_popup)
        mLsolvent.grid(row=4, column=1)

        optionsSolvent = tk.StringVar()
        optionsSolvent.set("DMSO")
        MenuSolvent = tk.OptionMenu(
            self.solution_popup, optionsSolvent, *self.solventlist['abbreviation'])
        MenuSolvent.grid(row=4, column=0)

        solventlabel = tk.Label(self.solution_popup, text='mL')
        solventlabel.grid(row=4, column=2)

        Confirmsolution2 = tk.Button(self.solution_popup, text='Confirm',
                                     command=lambda chemical_list=[gramRAFT, graminitiator, mLMonomer, mLsolvent],
                                     monomer=optionsMonomer, solvent=optionsSolvent,
                                     RAFT=optionsRAFT,
                                     initiator=optionsinitiator: self.controller.confirm_solution(
                                         chemical_list, monomer,
                                         solvent, RAFT, initiator),
                                     font=FONTS['FONT_BOTTON'])  # Upon Confirmation --> confirmSolution()

        Confirmsolution2.grid(row=5, column=1)

    def make_solution_summary_view(self, summary_string):
        solution_summary = tk.Label(self.NMRGPC_setup_parameter_frame, text='Reaction Solution', bg='gray',
                                    font=FONTS['FONT_NORMAL'], pady=20)
        # row i + 1; i last row from parameters
        solution_summary.grid(row=8, column=0, columnspan=2, rowspan=2)

        solution_summary.config(text=summary_string)

    def go_to_tab(self, next_tab):
        self.tab.select(next_tab)

    def _make_welcome_screen(self):
        s = ttk.Style()
        s.configure('PViewStyle.Treeview', font=self.FONTS['FONT_HEADER_BOLD'])
        Welcome_top_frame = tk.Frame(
            self.welcome_tab, bg='white', pady=30, padx=400)
        Welcome_top_frame.grid(sticky='ne')
        header_Welcome = tk.Label(
            Welcome_top_frame, text='Welcome', bg='white', font=self.FONTS['FONT_HEADER'])
        header_Welcome.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        Welcome_Option_frame = tk.Frame(self.welcome_tab)
        Welcome_Option_frame.grid()
        Welcome_option_frame_header = tk.Label(Welcome_Option_frame, text='Choose a mode of operation',
                                               font=self.FONTS['FONT_HEADER_BOLD'])
        Welcome_option_frame_header.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10)

        optionNMR_btn = tk.Button(Welcome_Option_frame, text="NMR", width=20, height=3,
                                  font=FONTS['FONT_HEADER_BOLD'],
                                  command=lambda button="NMR Button": self.controller.on_button_click(button))
        optionNMR_btn.grid(padx=5, pady=5)
        optionNMRGPC_btn = tk.Button(Welcome_Option_frame, text="NMR-GPC", width=20, height=3,
                                     font=FONTS['FONT_HEADER_BOLD'],
                                     command=lambda next_tab=self.setup: self.go_to_tab(next_tab))
        optionNMRGPC_btn.grid(padx=5, pady=5)

        comfolder_label = tk.Label(
            Welcome_Option_frame, text="Communication Folder", font=FONTS['FONT_ENTRY'])
        comfolder_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        comfolder_path = tk.StringVar(value=self.CommunicationMainFolder)

        comfolder = tk.Label(Welcome_Option_frame, textvariable=comfolder_path)
        comfolder.grid(row=4, column=0, columnspan=2)
        comfolder_btn = tk.Button(Welcome_Option_frame, text="Browse", command=lambda path=comfolder_path,
                                  folder_type="COMMUNICATION": self.controller.change_file_path(
                                      path, folder_type))
        comfolder_btn.grid(row=5, column=0)

        NMRmainfolder_label = tk.Label(
            Welcome_Option_frame, text="Spinsolve Folder", font=FONTS['FONT_ENTRY'])
        NMRmainfolder_label.grid(
            row=6, column=0, columnspan=2, padx=10, pady=10)
        NMRmainfolder_path = tk.StringVar(value=self.NMRFolder)
        NMRmainfolder = tk.Label(Welcome_Option_frame,
                                 textvariable=NMRmainfolder_path)
        NMRmainfolder.grid(row=7, column=0, columnspan=2)

        NMRmainfolder_btn = ttk.Button(Welcome_Option_frame, text="Browse",
                                       command=lambda path=NMRmainfolder_path,
                                       folder_type="NMR": self.controller.change_file_path(path,
                                                                                           folder_type))
        NMRmainfolder_btn.grid(row=8, column=0)

        Psswinmainfolder_label = tk.Label(
            Welcome_Option_frame, text="Psswin Folder", font=FONTS['FONT_ENTRY'])
        Psswinmainfolder_label.grid(
            row=9, column=0, columnspan=2, padx=10, pady=10)
        Psswinmainfolder_path = tk.StringVar(value=self.PsswinFolder)
        Psswinmainfolder = tk.Label(
            Welcome_Option_frame, textvariable=Psswinmainfolder_path)
        Psswinmainfolder.grid(row=10, column=0, columnspan=2)
        Psswinmainfolder_btn = ttk.Button(Welcome_Option_frame, text="Browse",
                                          command=lambda path=Psswinmainfolder_path,
                                          folder_type="GPC": self.controller.change_file_path(path,
                                                                                              folder_type))
        Psswinmainfolder_btn.grid(row=11, column=0)

        labviewscript_info = ttk.Label(
            Welcome_Option_frame, text="Labview script", font=FONTS['FONT_SMALL_BOLD'])
        labviewscript_info.grid(padx=12)
        script = ttk.Label(Welcome_Option_frame,
                           text=self.Labviewscript, font=FONTS['FONT_SMALL'])
        script.grid()

    def change_parameter_view_values(self):
        for i, parameter in enumerate(SETUP_DEFAULT_VALUES_NMR):
            parameter[1] = tk.Label(self.NMRGPC_setup_parameter_frame, text=parameter[4], bg='gray',
                                    width=20)  # changes value in GUI
            parameter[1].config(font=View.FONTS['FONT_NORMAL'], anchor='e')
            parameter[1].grid(row=i, column=4)

    def show_warning(self, error_message="Please enter a valid floating point number for all fields"):
        warning = tk.Toplevel(self)
        warning.title("Incorrect entry")
        header_wrong_input = tk.Label(warning, text=error_message,
                                      bg='white', font=self.FONTS['FONT_HEADER'])
        header_wrong_input.grid(padx=5, pady=5)
        exit_button = tk.Button(warning, text="Exit", command=warning.destroy)
        exit_button.grid()

    def clear_fields(self, *args):
        for field in args:
            field.delete(0, 'end')

    def show_final_timesweep_info(self, total_time, total_scan, total_gpc, scan_numbers):
        entry1 = TIMESWEEP_PARAMETERS.iloc[0]
        stabili = ((entry1['Volume'] * entry1['StabilisationTime']))
        allDvs = (((entry1['DeadVolume1'] + entry1['DeadVolume2'] +
                    entry1['DeadVolume3']) * int(scan_numbers.shape[0])))
        ts_number = int(scan_numbers.shape[0])
        totalvolume = stabili + (ts_number * allDvs)

        summary_1 = tk.Label(self.NMRGPC_timesweep_confirm_frame,
                             text='Total time:             {}min'.format(round(total_time, 1)), width=90, bg='gray',
                             anchor='w', padx=10)
        summary_1.grid(row=1, column=0)
        summary_2 = tk.Label(self.NMRGPC_timesweep_confirm_frame,
                             text='Total NMR scans:         {}'.format(round(total_scan, 0)), width=90, bg='gray',
                             anchor='w')
        summary_2.grid(row=2, column=0)
        summary_3 = tk.Label(self.NMRGPC_timesweep_confirm_frame,
                             text='Total GPC samples:       {}'.format(
                                 round(total_gpc, 0)),
                             width=90, bg='gray', anchor='w')
        summary_3.grid(row=3, column=0)
        summary_4 = tk.Label(self.NMRGPC_timesweep_confirm_frame,
                             text='Volume Needed:       {} mL'.format(round(totalvolume, 1)), width=90, bg='gray',
                             anchor='w')
        summary_4.grid(row=4, column=0)

        logger.info(
            'Experiment will take {} minutes; +/- {} mL reaction solution is needed.'.format(total_time, totalvolume))

    def _set_conversion_formula(self, monomer_key):
        Constants.Conversion_values = Constants.Monomer_Conversion[monomer_key]

    def _make_conversion_screen(self):

        self.NMRGPC_top_frame_conv = tk.Frame(
            self.tab_NMRGPC_Conversion, bg='white', width=1000, height=50, pady=3, padx=400)
        self.NMRGPC_top_frame_conv.grid(row=0, sticky="ew")

        name_window_conv = tk.Label(
            self.NMRGPC_top_frame_conv, text='Conversion', bg='white', font=FONTS['FONT_HEADER'])
        name_window_conv.grid()
        self.Conversion_option_NMRGPC = tk.StringVar()

        self.IS_radio_NMRGPC = tk.Radiobutton(self.tab_NMRGPC_Conversion, text="Internal Standard",
                                              font=FONTS['FONT_ENTRY'],
                                              variable=self.Conversion_option_NMRGPC, value="Internal Standard",
                                              command=self.select_internal_standard)
        self.IS_radio_NMRGPC.grid()
        self.mol_monomerLabel_NMRGPC = tk.Label(
            self.tab_NMRGPC_Conversion, text="Monomer initial (mol)")
        self.mol_monomerLabel_NMRGPC.grid()
        self.mol_monomerEntry_NMRGPC = tk.Entry(self.tab_NMRGPC_Conversion)
        self.mol_monomerEntry_NMRGPC.grid()
        self.mol_ISlabel_NMRGPC = tk.Label(
            self.tab_NMRGPC_Conversion, text="4-hydroxy benzaldehyde initial (mol)")
        self.mol_ISlabel_NMRGPC.grid()
        self.mol_internal_standardEntry_NMRGPC = tk.Entry(
            self.tab_NMRGPC_Conversion)
        self.mol_internal_standardEntry_NMRGPC.grid()

        monomer_radio_NMRGPC = tk.Radiobutton(self.tab_NMRGPC_Conversion, text="Monomer", font=FONTS['FONT_ENTRY'],
                                              variable=self.Conversion_option_NMRGPC, value="Monomer",
                                              command=self.select_monomer)
        monomer_radio_NMRGPC.grid()
        options = tk.StringVar(self.tab_NMRGPC_Conversion)
        options.set("Choose")  # default value
        monomer_options_label = tk.Label(self.tab_NMRGPC_Conversion,  text='Monomer Options',
                                         font=('Helvetica', 16), width=30, anchor="c")
        monomer_options_label.grid()

        monomer_options_menu = tk.OptionMenu(
            self.tab_NMRGPC_Conversion, options, *Constants.Monomer_Conversion.keys(), command=lambda key=options: self._set_conversion_formula(key))
        monomer_options_menu.grid()
        print(options.get())

        solvent_radio_NMRGPC = tk.Radiobutton(self.tab_NMRGPC_Conversion, text="Solvent (Butyl Acetate)",
                                              font=FONTS[
                                                  'FONT_ENTRY'], variable=self.Conversion_option_NMRGPC,
                                              value="Solvent (Butyl Acetate)",
                                              command=self.select_solvent)
        solvent_radio_NMRGPC.grid()

        Conversion_info_frame_NMRGPC = tk.Frame(self.tab_NMRGPC_Conversion)
        Conversion_info_frame_NMRGPC.grid()

        self.Conversion_Label_NMRGPC = tk.Label(
            Conversion_info_frame_NMRGPC, text='Choose option')
        self.Conversion_Label_NMRGPC.grid(row=0, column=1, columnspan=3)

        confirm_conv_btm_NMRGPC = tk.Button(Conversion_info_frame_NMRGPC, text='Confirm', height=3, width=15,
                                            command=lambda conversion_option_chosen=self.Conversion_option_NMRGPC,
                                            field_entries=[self.mol_monomerEntry_NMRGPC,
                                                           self.mol_internal_standardEntry_NMRGPC]: self.controller.confirm_conversion(
                                                conversion_option_chosen.get(), field_entries),
                                            font=FONTS['FONT_BOTTON'])
        confirm_conv_btm_NMRGPC.grid(row=1, column=2, rowspan=3)

    def select_internal_standard(self):
        '''If internal standard option is selected'''
        self.mol_internal_standardEntry_NMRGPC.configure(state='normal')
        self.mol_monomerEntry_NMRGPC.configure(state='normal')
        self.Conversion_Label_NMRGPC.config(text='Internal Standard')
        self.mol_monomerLabel_NMRGPC.configure(foreground='black')
        self.mol_ISlabel_NMRGPC.configure(foreground='black')

    def select_monomer(self):
        '''If monomer option is selected, IS entry fields are disabled'''
        self.Conversion_Label_NMRGPC.config(
            text='Conversion will be calculated with monomer peaks (only MA for now)')
        self.mol_internal_standardEntry_NMRGPC.configure(state='disabled')
        self.mol_monomerEntry_NMRGPC.configure(state='disabled')
        self.mol_monomerLabel_NMRGPC.configure(foreground='gray')
        self.mol_ISlabel_NMRGPC.configure(foreground='gray')

    def select_solvent(self):
        '''If solvent option is selected, IS entry fields are disabled'''
        self.Conversion_Label_NMRGPC.config(
            text='Conversion will be calculated based on the solvent+monomer peak (butyl acetate)')
        self.mol_internal_standardEntry_NMRGPC.configure(state='disabled')
        self.mol_monomerEntry_NMRGPC.configure(state='disabled')
        self.mol_monomerLabel_NMRGPC.configure(foreground='gray')
        self.mol_ISlabel_NMRGPC.configure(foreground='gray')

    def _make_NMR_setup_screen(self):
        logger.info('Selected mode: NMR and GPC')
        self.tab.select(self.setup)
        ### NMR  - SETUP TAB ###
        # Create Main frame of Setup Tab
        self.NMRGPC_setup_top_frame = tk.Frame(
            self.setup, bg='white', width=1000, height=50, pady=3, padx=400)
        self.NMRGPC_setup_top_frame.grid(row=0, sticky='ew')

        self.NMRGPC_setup_picture_frame = tk.Frame(
            self.setup, bg='white', width=1000, height=30, padx=175, pady=3)
        self.NMRGPC_setup_picture_frame.grid(row=1, sticky='ew')

        self.NMRGPC_setup_parameter_frame = tk.Frame(
            self.setup, bg='gray', width=1000, height=350, pady=30)
        self.NMRGPC_setup_parameter_frame.grid(row=2, sticky='ew')

        self.NMRGPC_setup_confirm_frame = tk.Frame(
            self.setup, bg='gray', width=1000, height=50, pady=10, padx=400)
        self.NMRGPC_setup_confirm_frame.grid(row=3, sticky="ew")

        # Make-Up Top Frame
        name_window = tk.Label(
            self.NMRGPC_setup_top_frame, text='Setup', bg='white')
        name_window.config(font=FONTS['FONT_HEADER'])
        name_window.grid()

        # Make-Up Picture_frame
        self.NMRGPC_picure_setup = tk.PhotoImage(
            file='Pictures/NMRGPCsetup.png')
        NMRGPC_LabelPicture = tk.Label(
            self.NMRGPC_setup_picture_frame, image=self.NMRGPC_picure_setup, bg='black')
        NMRGPC_LabelPicture.grid()
        for i, entry_values in enumerate(SETUP_DEFAULT_VALUES_NMR):
            parameter = tk.Label(self.NMRGPC_setup_parameter_frame, text=entry_values[2],
                                 width=30)  # parameter name in column 0
            parameter.config(font=FONTS['FONT_NORMAL'])
            parameter.grid(row=i, column=0)

            entry_values[0] = tk.Entry(
                self.NMRGPC_setup_parameter_frame)  # entry in column 1
            entry_values[0].grid(row=i, column=1)

            unit = tk.Label(self.NMRGPC_setup_parameter_frame, text=entry_values[3], bg='red',
                            width=10)  # unit in column 2
            # anchor the left of the label (west)
            unit.config(font=FONTS['FONT_NORMAL'], anchor='w')
            unit.grid(row=i, column=2)

            entry_values[5] = tk.Button(self.NMRGPC_setup_parameter_frame, text='Change',
                                        command=self.controller.on_change_button_click)  # botton (with text change) in column 3
            entry_values[5].grid(row=i, column=3)

            entry_values[1] = tk.Label(self.NMRGPC_setup_parameter_frame, text=entry_values[4],
                                       bg='red')  # default value in column 4
            # anchor to the right of the label (east)
            entry_values[1].config(font=FONTS['FONT_NORMAL'], anchor='e')
            entry_values[1].grid(row=i, column=4)

            unit2 = tk.Label(self.NMRGPC_setup_parameter_frame, text=entry_values[3],
                             bg='red')  # again unit in column 5
            unit2.config(font=FONTS['FONT_NORMAL'])
            unit2.grid(row=i, column=5)

        solutionSummary1 = tk.Label(self.NMRGPC_setup_parameter_frame, text='Reaction Solution', bg='gray',
                                    font=FONTS['FONT_NORMAL'], pady=20)
        # row i + 1; i last row from parameters
        solutionSummary1.grid(row=i + 1, column=0, columnspan=2, rowspan=2)
        solution_button1 = tk.Button(self.NMRGPC_setup_parameter_frame, text='Reaction solution',
                                     command=self.make_pop_up_tab)
        solution_button1.grid(row=i + 1, column=3)

        # Make-up confirm frame
        confirm_reactorParameters = tk.Button(self.NMRGPC_setup_confirm_frame, text='Confirm', height=3, width=15,
                                              command=self.Confirm_reactor_parameters, font=FONTS['FONT_BOTTON'])

        confirm_reactorParameters.grid()

    def _make_NMRGPC_initialisation_tab(self):
        # Create Main frame of init Tab
        NMRGPC_top_frame_init = tk.Frame(
            self.tab_NMRGPC_Initialisation, bg='white', width=1000, height=50, pady=3, padx=400)
        NMRGPC_top_frame_init.grid(row=0, sticky="ew")
        NMRGPC_picture_frame_init = tk.Frame(self.tab_NMRGPC_Initialisation, bg='white', width=1000, height=300,
                                             padx=175,
                                             pady=3)
        NMRGPC_picture_frame_init.grid(row=1, sticky="nsew")
        NMRGPC_parameter_frame_init = tk.Frame(self.tab_NMRGPC_Initialisation, bg='gray', width=1000, height=350,
                                               pady=3,
                                               padx=3)
        NMRGPC_parameter_frame_init.grid(row=3, sticky="ew")
        NMRGPC_btm_frame_init = tk.Frame(
            self.tab_NMRGPC_Initialisation, bg='gray', width=1000, height=50, pady=10, padx=400)
        NMRGPC_btm_frame_init.grid(row=4, sticky="ew")

        # Make-Up Top Frame in init Tab
        name_window_init = tk.Label(
            NMRGPC_top_frame_init, text='Initialisation', bg='white', font=FONTS['FONT_HEADER'])
        name_window_init.grid()

        # Make-Up Parameter_frame_timesweep in ininialisation Tab
        tsparam = tk.Label(NMRGPC_parameter_frame_init, text="Start Initialisation", bg='gray',
                           font=FONTS['FONT_HEADER_BOLD'], padx=150)
        tsparam.grid(row=0, column=1, columnspan=2)
        # Experiment code
        code_lbl = tk.Label(NMRGPC_parameter_frame_init, text='Experiment Code', bg='gray', width=15,
                            font=FONTS['FONT_NORMAL'])
        code_lbl.grid(row=3, column=0)

        self.code_en = tk.Entry(NMRGPC_parameter_frame_init,
                                font=FONTS['FONT_ENTRY'], width=30)
        self.code_en.grid(row=3, column=1)

        self.labelLabview = tk.Label(NMRGPC_parameter_frame_init,
                                     text='LABVIEW', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelLabview.grid(row=5, column=0, columnspan=2)
        self.confirmlabview = tk.Button(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'],
                                        command=self.confirmLabview, state='disabled', width=6)
        self.confirmlabview.grid(row=5, column=3)
        self.HelpLabview = tk.Button(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'],
                                     state='disabled',
                                     command=self.HelpLabView, width=6)
        self.HelpLabview.grid(row=5, column=4)
        self.labelLabviewInfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelLabviewInfo.grid(row=6, column=0, columnspan=2)

        self.labelPss = tk.Label(
            NMRGPC_parameter_frame_init, text='PSS', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelPss.grid(row=7, column=0, columnspan=2)
        self.confirmpss = tk.Button(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'], state='disabled',
                                    command=self.confirmPss, width=6)
        self.confirmpss.grid(row=7, column=3)
        self.Helppss = tk.Button(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'], state='disabled',
                                 command=self.HelpPss, width=6)
        self.Helppss.grid(row=7, column=4)
        self.labelPssInfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelPssInfo.grid(row=8, column=0, columnspan=2)

        self.labelSpinsolve = tk.Label(
            NMRGPC_parameter_frame_init, text='Spinsolve', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelSpinsolve.grid(row=9, column=0, columnspan=2)
        self.confirmspinsolve = tk.Button(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'],
                                          state='disabled',
                                          command=self.confirmSpinsolve, width=6)
        self.confirmspinsolve.grid(row=9, column=3)
        self.Helpspinsolve = tk.Button(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'],
                                       state='disabled',
                                       command=self.HelpSpinsolve, width=6)
        self.Helpspinsolve.grid(row=9, column=4)
        self.labelSpinsolveInfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelSpinsolveInfo.grid(row=10, column=0, columnspan=2)

        self.labelEmail = tk.Label(
            NMRGPC_parameter_frame_init, text='Email', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelEmail.grid(row=11, column=0, columnspan=1)
        self.entryEmail = tk.Entry(NMRGPC_parameter_frame_init, text='Email', font=FONTS['FONT_SMALL'],
                                   state='readonly',
                                   width=30)
        self.entryEmail.grid(row=11, column=1, columnspan=1)
        self.confirmEmail = tk.Button(NMRGPC_parameter_frame_init, text='Confirm', font=FONTS['FONT_BOTTON'],
                                      state='disabled',
                                      command=self.confirm_emailadress, width=6)
        self.confirmEmail.grid(row=11, column=3)
        self.addEmail = tk.Button(NMRGPC_parameter_frame_init, text='Add', font=FONTS['FONT_BOTTON'], state='disabled',
                                  command=self.AddEmail, width=6)
        self.addEmail.grid(row=11, column=4)
        self.labelEmailinfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelEmailinfo.grid(row=12, column=0, columnspan=2)

        self.NMRGPC_confirm_code = tk.Button(NMRGPC_parameter_frame_init, text='OK',
                                             font=FONTS['FONT_BOTTON'], command=self.confirm_code, width=6)
        self.NMRGPC_confirm_code.grid(row=4, column=1, columnspan=2)

        self.start_btn = Button(NMRGPC_btm_frame_init, text='Start',
                                font=FONTS['FONT_HEADER_BOLD'], state='disabled', command=self.startexp)
        self.start_btn.grid()

        # Make-up page
        top_frame_exp = Frame(self.tab_overview, bg='white',
                              width=1000, height=50, pady=3, padx=400)
        parameter_frame_exp = Frame(self.tab_overview, bg='gray',
                                    width=1000, height=350, pady=3)
        top_frame_exp.grid(row=0, sticky="ew")
        parameter_frame_exp.grid(row=1, sticky="ew")

        # Make-Up Top Frame in exp Tab
        name_window_exp = Label(top_frame_exp, text='Experiment',
                                bg='white', font=FONTS['FONT_HEADER'])
        name_window_exp.grid()

    def db_connect(self):

        try:

            db_connection = mdb.connect(host='127.0.0.1',
                                        user='root',
                                        password='',
                                        database='chemistry')

            self.label.configure(text="Connected Successfully")

        except mdb.Error as e:
            self.label.configure(text="Not Successfully Connected")

    def get_user_experiments(self, v):
        self.v = v
        self.wanted_user_id = (list(self.dict_a.keys())[
            list(self.dict_a.values()).index(v)])
        self.experiment_list = []
        self.experimenter_id_list = []
        val_list = ["None"]

        experiments = my_conn.execute(
            f"SELECT * FROM experiments_experiment WHERE user_id={self.wanted_user_id}")
        for ds in experiments:
            self.experiment_list.append(ds[3])
            self.experimenter_id_list.append(ds[0])

        self.show_user_experiments(
            self.experimenter_id_list, self.experiment_list)

    def show_user_experiments(self, list, primary_id_list):
        try:
            self.Experiment.destroy()
        except:
            pass

        self.dict_id_list = dict(
            zip(list, primary_id_list))
        val_list = ["None"]
        default_value = tk.StringVar()
        default_value.set(val_list[0])
        self.Experiment = tk.OptionMenu(
            self.experiment_upload_frame_top, default_value, *self.dict_id_list.values(), command=self.get_experiment_pk_for_data_upload)
        self.Experiment.grid(row=6,  column=3)

    def get_experiment_pk_for_data_upload(self, v):
        wanted_user_id = (list(self.dict_id_list.keys())[
                          list(self.dict_id_list.values()).index(v)])

        set = my_conn.execute(
            f"SELECT * FROM experiments_experiment WHERE id={wanted_user_id}")

        for ds in set:

            self.pk = ds[0]
        return

    def add_upload_to_measurement(self, f, is_approved, device_id, pk):

        query_measurement = "INSERT INTO  `measurements_measurement` (`file` ,`is_approved`,`device_id`,`experiment_id` ) \
                VALUES(%s,%s,%s,%s)"
        my_measurement_data = (f, is_approved, device_id,
                               pk)
        my_conn.execute(query_measurement, my_measurement_data)
        my_retrieval_data = (f, is_approved, device_id, pk
                             )
        retrieve_query = "SELECT id FROM  `measurements_measurement` WHERE `file`=%s AND `is_approved`=%s AND `device_id`=%s AND \
                `experiment_id`=%s"
        a = my_conn.execute(
            retrieve_query, my_retrieval_data)
        for item in a:
            self.measurement_pk = item[0]

        # self.measurement_pk = a.all()[0][0]

    def csv_to_GPC_table(self, f):
        data = pd.read_csv(f, encoding='UTF-8')
        data_conv = data[['tres_GPC', 'D', 'Mn',
                          'Mw', 'Mn theory']]
        data_conv['measurement_id'] = self.measurement_pk

        data_conv = data_conv.dropna()

        data['tres_GPC'] = data_conv.apply(
            lambda row: timedelta(minutes=float(row.tres_GPC)).total_seconds(), axis=1)

        data_conv.to_sql('measurements_GPC_data', my_conn,
                         if_exists='append', index=False, method='multi')
        return

    def csv_to_table_nmr(self, f):
        data = pd.read_csv(f, encoding='UTF-8')

        data_conv = data[['conversion', 'tres']]
        data_conv = data_conv.dropna()

        data_conv['tres'] = data_conv.apply(
            lambda row: timedelta(minutes=float(row.tres)).total_seconds(), axis=1)
        data_conv.rename(columns={'conversion': 'result',
                                  'tres': 'res_time'}, inplace=True)

        data_conv['measurement_id'] = self.measurement_pk

        data_conv.to_sql('measurements_data', my_conn,
                         if_exists='append', index=False, method='multi')

    def upload(self):
        # uploads GPC and NMR data to the database
        f = open(self.filename)
        a = open(self.filename)
        csv_path_split_array = f.name.split("/")
        csv_path = csv_path_split_array[-1]
        is_approved = 1
        device_id = 1
        self.add_upload_to_measurement(
            csv_path, is_approved, device_id, self.pk)

        self.csv_to_table_nmr(f)
        print("csv uploaded to nmr")
        self.csv_to_GPC_table(a)
        print("GPC uploaded to database")

    def browseFiles(self):
        self.f_types = [('CSV files', "*.csv"), ('All', "*.*")]
        self.filename = filedialog.askopenfilename(filetypes=self.f_types)

        # Change label contents
        self.label_file_explorer.configure(
            text="File Opened: " + self.filename)
        # self.get_experiment_pk_for_data_upload(self.pk)

    def _create_experiment_upload_screen(self):

        self.experiment_upload_frame_top = Toplevel()

        self.experiment_upload_frame_top.title("Select File for data upload")
        button = ttk.Button(
            self.experiment_upload_frame_top, text="Connection Status", command=self.db_connect)
        button.grid(row=0, column=3)

        self.label = ttk.Label(self.experiment_upload_frame_top, text="")
        self.label.grid(row=1, column=3)

        self.label_file_explorer = tk.Label(self.experiment_upload_frame_top,
                                            text="File path")
        button_explore = ttk.Button(self.experiment_upload_frame_top,
                                    text="Browse Files",
                                    command=self.browseFiles)

        upload_button = ttk.Button(self.experiment_upload_frame_top,
                                   text="Upload CSV file",
                                   command=self.upload)
        self.label_file_explorer.grid(row=7, column=3)
        try:
            self.filename = self.csvprefill
            self.label_file_explorer.configure(
                text="File Opened: " + self.filename)
        except:
            self.filename = '/'
            self.label_file_explorer.configure(
                text="File Opened: " + self.filename)

        button_explore.grid(row=8, column=3)

        upload_button.grid(row=9, column=3)

    def _upload_results_pop_up(self):
        self.pop_up_frame_top = Toplevel()
        self.pop_up_frame_top.geometry("650x550")
        self.pop_up_frame_top.title("Select User for upload")

        pop_up_upload_frame = tk.Frame(
            self.pop_up_frame_top, bg='white', width=100, height=50, pady=3, padx=100)
        pop_up_upload_frame.grid()

        options = tk.StringVar(pop_up_upload_frame)
        options.set("Choose")  # default value

        user_label = tk.Label(pop_up_upload_frame,  text='User',
                              font=('Helvetica', 16), width=30, anchor="c")
        user_label.grid(row=0, column=0, columnspan=4)

        user_options_menu = tk.OptionMenu(
            pop_up_upload_frame, options, *self.dict_a.values(), command=self.get_user_experiments)
        user_options_menu.configure(width=30)
        user_options_menu.grid(row=1, column=0)

        self.name_label = tk.Label(pop_up_upload_frame,  text='Experiment Name',
                                   font=('Helvetica', 16), width=30, anchor="c")
        self.name_label.grid(row=2, column=0, columnspan=5)

        self.experiment_name_en = tk.Entry(pop_up_upload_frame,
                                           font=FONTS['FONT_ENTRY'], width=30)
        self.experiment_name_en.grid(row=3, column=0)

        self.experiment_name_en.insert(END, self.code_en.get())

        self.monomer_label = tk.Label(pop_up_upload_frame,  text='Monomer Used',
                                      font=('Helvetica', 16), width=30, anchor="c")
        self.monomer_label.grid(row=4, column=0, columnspan=5)

        self.monomer_list = ["MA", "EA", "MMA", "BA"]

        self.monomer_value = tk.StringVar(pop_up_upload_frame)

        self.monomer_value.set("Choose a Monomer")

        self.monomer_name_en = tk.OptionMenu(
            pop_up_upload_frame, self.monomer_value, *self.monomer_list)

        # self.monomer_name_en = tk.Entry(pop_up_upload_frame,
        #                                 font=FONTS['FONT_ENTRY'], width=30)
        self.monomer_name_en.grid(row=5, column=0)

        self.CTA_label = tk.Label(pop_up_upload_frame,  text='CTA Used',
                                  font=('Helvetica', 16), width=30, anchor="c")
        self.CTA_label.grid(row=6, column=0, columnspan=5)

        self.CTA_list = ["Dodecanethiol", "Carbon Tetrabromide"]

        self.CTA_value = tk.StringVar(pop_up_upload_frame)

        self.CTA_value.set("Choose a CTA")

        self.CTA_en = tk.OptionMenu(
            pop_up_upload_frame, self.CTA_value, *self.CTA_list)

        self.CTA_en.grid()

        self.Cx_ratio_label = tk.Label(pop_up_upload_frame,  text='Cx/Cm Ratio',
                                       font=('Helvetica', 16), width=30, anchor="c")
        self.Cx_ratio_label.grid(row=8, column=0, columnspan=5)

        self.Cx_ratio_en = tk.Entry(pop_up_upload_frame,
                                    font=FONTS['FONT_ENTRY'], width=30)
        self.Cx_ratio_en.grid(row=9, column=0)

        self.temperature_label = tk.Label(pop_up_upload_frame,  text='Temperature',
                                          font=('Helvetica', 16), width=30, anchor="c")
        self.temperature_label.grid(row=10, column=0, columnspan=4)

        self.temperature_en = tk.Entry(pop_up_upload_frame,
                                       font=FONTS['FONT_ENTRY'], width=30)
        self.temperature_en.grid(row=11, column=0)
        self.volume_label = tk.Label(pop_up_upload_frame,  text='Volume',
                                     font=('Helvetica', 16), width=30, anchor="c")
        self.volume_label.grid(row=12, column=0, columnspan=4)

        self.volume_en = tk.Entry(pop_up_upload_frame,
                                  font=FONTS['FONT_ENTRY'], width=30)
        self.volume_en.grid(row=13, column=0)

        upload_button = tk.Button(pop_up_upload_frame,  text='Add to Database', width=10,
                                  command=lambda: self.add_experiment_data())
        upload_button.grid(row=14, column=0)
        self.my_str = tk.StringVar()
        l5 = tk.Label(pop_up_upload_frame,
                      textvariable=self.my_str, width=10)
        l5.grid(row=15, column=0)
        self.my_str.set("Output")

    def add_experiment_data(self):

        flag_validation = True
        self.date = datetime.today().date()

        self.time = datetime.now().time()
        self.exp_name = self.experiment_name_en.get()
        self.temperature = self.temperature_en.get()
        self.volume = self.volume_en.get()
        self.CA = self.CTA_value.get()
        self.monomer = self.monomer_value.get()
        self.CxCm = self.Cx_ratio_en.get()

        print(f"date: {self.date}, time: {self.time} , name: {self.exp_name}, temperature: {self.temperature}, volume: {self.volume}, user_id: {self.wanted_user_id}, monomer: {self.monomer}, CA: {self.CA}, Cx/Cm {self.CxCm}")
        print((len(self.monomer)))
        print(len(self.CA))

        if (len(self.exp_name)) < 2 and (len(self.CA) < 1) and (len(self.monomer) < 1):
            flag_validation = False
        try:
            temp_val = int(self.temperature)  # checking mark as integer
            volume_val = int(self.volume)
            CxCm = float(self.CxCm)

        except:
            flag_validation = False

        if (flag_validation):

            # upload experiment
            query = "INSERT INTO  `experiments_experiment` (`date` ,`time` ,`name` ,`temperature`, `total_volume`,`user_id`,`monomer`, `CTA`, `cx_ratio` ) \
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            my_data = (self.date, self.time, self.exp_name,
                       self.temperature, self.volume, self.wanted_user_id, self.monomer, self.CA, self.CxCm)

            my_retrieval_data = (self.exp_name, self.date, self.temperature, self.volume, self.monomer, self.CA,  self.CxCm
                                 )
            retrieve_query = "SELECT id FROM  `experiments_experiment` WHERE `name`=%s AND `date`=%s AND `temperature`=%s AND \
                `total_volume`=%s AND `monomer`=%s AND `CTA`=%s AND `cx_ratio`=%s"
            ex = my_conn.execute(query, my_data)
            row_id = my_conn.execute(retrieve_query, my_retrieval_data)

            # retrieve its primary key
            # use primary keu for data insersion

            self.get_user_experiments(self.v)
            self.pop_up_frame_top.destroy()

        else:
            self.temperature_label.config(fg='red')   # foreground color
            self.temperature_label.config(bg='yellow')  # background color
            self.volume_label.config(fg='red')   # foreground color
            self.volume_label.config(bg='yellow')  # background color
            self.name_label.config(fg='red')
            self.name_label.config(bg='yellow')
            self.Cx_ratio_label.config(bg='yellow')
            self.Cx_ratio_label.config(fg='red')
            self.CTA_label.config(bg='yellow')
            self.CTA_label.config(fg='red')
            self.monomer_label.config(bg='yellow')
            self.monomer_label.config(fg='red')
            self.my_str.set("check inputs.")

    def _get_user_names(self):
        list_of_experimenters = []
        list_of_experimenter_ids = []
        re_set = my_conn.execute("SELECT * FROM users_user")
        for ds in re_set:
            list_of_experimenters.append(ds[4])
            list_of_experimenter_ids.append(ds[0])
        self.dict_a = dict(
            zip(list_of_experimenter_ids, list_of_experimenters))

    def SearchCommunicationFolder(self, folder):
        '''
        Makes the different data folders in the main experiment folder.

        input:\n Folder

        Output:\n1) Folder where GPCs are going to be stored.\n2) Folder where timesweeps are going to be stored.\n3) Folder where Raw GPCs are going to be stored.\n4) Folder where experiment details are going to be stored.\n5) Folder where Injection infos are going to be stored.
        '''
        self.SolutionDataframe = pd.DataFrame()

        mode = self.parametersDF.loc[0, 'mode']

        newfolderTimesweepdata = os.path.join(folder, 'Timesweep Data')
        if not os.path.exists(newfolderTimesweepdata):
            os.mkdir(newfolderTimesweepdata)
        newfoldersoftware = os.path.join(folder, 'Software details')
        if not os.path.exists(newfoldersoftware):
            os.mkdir(newfoldersoftware)
        self.parametersDF.to_csv(
            '{}/ParameterDF.csv'.format(newfoldersoftware))
        newfolderplots = os.path.join(folder, 'Plots')
        if not os.path.exists(newfolderplots):
            os.mkdir(newfolderplots)

        if str(mode) == 'GPCandNMR':
            newfolderGPC = os.path.join(folder, 'Filtered GPC Data')
            if not os.path.exists(newfolderGPC):
                os.mkdir(newfolderGPC)

            newfolderinfoGPC = os.path.join(folder, 'Info GPC Injections')
            if not os.path.exists(newfolderinfoGPC):
                os.mkdir(newfolderinfoGPC)

            newfolderRawGPC = os.path.join(folder, 'Raw GPC text files')
            if not os.path.exists(newfolderRawGPC):
                os.mkdir(newfolderRawGPC)

        elif mode == 'NMR':
            newfolderGPC, newfolderinfoGPC, newfolderRawGPC = 'NaN', 'NaN', 'NaN'

        self.experiment_extra.loc[0, ['GPCfolder', 'Timesweepfolder', 'Infofolder', 'Softwarefolder', 'Rawfolder', 'Plotsfolder']] = str(newfolderGPC).replace("\\", "/"), str(newfolderTimesweepdata).replace(
            "\\", "/"), str(newfolderinfoGPC).replace("\\", "/"), str(newfoldersoftware).replace("\\", "/"), str(newfolderRawGPC).replace("\\", "/"), str(newfolderplots).replace("\\", "/")
        self.experiment_extra.to_csv(
            '{}/extras_experiment.csv'.format(newfoldersoftware))

        if not self.SolutionDataframe.empty:
            self.SolutionDataframe.to_csv(
                '{}/ReactionSolution_{}.csv'.format(newfoldersoftware, self.experiment_extra.loc[0, 'code']))
            # updateGUI('Solution Dataframe saved in software subfolder')
        else:
            # updateGUI('No Solution Details given')
            return newfolderGPC, newfolderTimesweepdata, newfolderRawGPC

    def startexp(self):
        print("experiment name")
        print(self.code_en.get())

        nmr_interval = self.parametersDF.loc[0, 'NMR interval']
        code = self.experiment_extra.loc[0, 'code']
        mode = self.parametersDF.loc[0, 'mode']

        startfile = open(Temporary_textfile, 'w')
        startfile.write('start')
        startfile.close()

        logger.info(
            'Experiment started by operator. Start sign is communicated to LabView.')

        vals = starting(self.ExperimentFolder)
        NMRfolder = vals[0]
        print(NMRfolder)
        expDF = vals[1]

        expDF_directory = '{}/{}_Experiment'.format(
            self.experiment_extra.loc[0, 'Softwarefolder'], code)

        scansDF = calculate_scans(TIMESWEEP_PARAMETERS, mode=mode)
        last_timesweep_row = scansDF.iloc[-1][4]
        scansDF_directory = '{}/{}_{}'.format(
            self.experiment_extra.loc[0, 'Softwarefolder'], code, 'Scans.csv')
        scansDF.to_csv(scansDF_directory)  # saves scans in csv file

        end_counter = 0
        analysis = True
        gpc_number = 0
        modify_time = 0
        saving_directory_plots, GPCfolder, infofolder, rawGPCfolder = self.experiment_extra.loc[0, [
            'Plotsfolder', 'GPCfolder', 'Infofolder', 'Rawfolder']]
        self.SearchCommunicationFolder(self.ExperimentFolder)

        while analysis and end_counter < (last_timesweep_row +25):
            print("sleeps {}".format(nmr_interval))
            end_counter += 1
            sleep(nmr_interval)

            #nextLoop = input('>> Next Loop press ENTER')
            expDF, newNMR_bool, modify_time = UpdateDF_NMRdata.updateDF_integrals(
                expDF, NMRfolder, expDF_directory, mode, self.SolutionDataframe, modify_time)
            if newNMR_bool == False:
                try:
                    save_plots.save_scanconversion(
                        expDF, code, saving_directory_plots)
                    save_plots.save_scanintegrals(
                        expDF, code, saving_directory_plots)
                    save_plots.save_tresconversion(
                        expDF, code, saving_directory_plots)
                    save_plots.save_fit(expDF, code, saving_directory_plots)
                except PermissionError:
                    print('Please close the .png files to update the experiment plots')
                except:
                    print('could not save plots for unknown reason')
                continue

            if mode == 'GPCandNMR':
                expDF, gpc_number, newGPC = UpdateDF_GPCdata.search_newGPC(
                    self.PsswinFolder, code, gpc_number, expDF, expDF_directory, GPCfolder, infofolder, rawGPCfolder)
                if newGPC:
                    try:
                        save_plots.save_tresMn(
                            expDF, code, saving_directory_plots)
                        save_plots.save_conversionMn(
                            expDF, code, saving_directory_plots)
                    except PermissionError:
                        print(
                            'Please close the .png files to update the experiment plots')
                        print('GPC plots are updated')
            try:
                save_plots.save_scanconversion(
                    expDF, code, saving_directory_plots)
                save_plots.save_scanintegrals(
                    expDF, code, saving_directory_plots)
                save_plots.save_tresconversion(
                    expDF, code, saving_directory_plots)
            except PermissionError:
                print('Please close the .png files to update the experiment plots')

            try:
                expDF.to_csv(
                    '{}/{}_data.csv'.format(self.experiment_extra.loc[0, 'Mainfolder'], code))
            except:
                pass
        print('End of Experiment')

        search = findexperimentcsvfile.CSVFileFinder(self.code_en.get())
        self.csvprefill = search.find_experiment_path()
        print("path csv")
        print(self.csvprefill)
        self._upload_results_pop_up()
        self._create_experiment_upload_screen()

    def check_experimentFoldertxtfile(self, expfolder, exp_code):
        directory_code = os.path.basename(expfolder).split('_')[-1]
        if not directory_code == exp_code:
            logger.warning('It seems that the code given by LabView ({}) does not match the real code ({}). Please give the correct Experiment Folder'.format(
                directory_code, exp_code))
            experimentfolder = input('>> ')
            return experimentfolder
        return expfolder

    def confirm_code(self):
        '''
        Extracts code from entry field and writes it in temporary text file (as 'Code,,code') in Communication folder. Can now be read by LabView.
        '''
        code = self.code_en.get()

        # code will later be extracted from path as .split('_')[-1]
        if '_' in code:
            logger.warning('Code cannot contain _.')
            return
        self.code_en.configure(state='readonly')
        self.NMRGPC_confirm_code.configure(state='disabled')
        print(Temporary_textfile)

        with open(Temporary_textfile, "a") as f:
            f.write('Code,,')
            f.write(code)
            f.close()

        logger.info(
            'Code ({}) and timesweep parameters are communicated to LabVIEW software'.format(code))

        self.experiment_extra.loc[0, 'code'] = code

        reactorvol = self.parameterList1[0][4]

        col_names = ['Start', 'Stop', 'volume', 'StartFR', 'StopFR', 'stabilisation time', 'dead volume 1', 'Dead Volume 2', 'GPC Interval',
                     'Dead Volume 3', 'Dilution FR', 'DeadVolume1(min)', 'DeadVolume2(min)', 'DeadVolume3(min)', 'NMR interval', 'mode']
        self.parametersDF = pd.DataFrame(columns=col_names)
        params = {}

        for item in SETUP_DEFAULT_VALUES_NMR:
            params[item[2]] = item[4]

        for i, timesweep in enumerate(self.NMRGPC_all_ts_info):

            fr1, fr2 = reactorvol/timesweep[2], reactorvol/timesweep[3]
            # Create DF with all the parameters

            # Create DF with all the parameters
            self.parametersDF.loc[i, 'Start'] = timesweep[2]
            self.parametersDF.loc[i, 'Stop'] = timesweep[3]
            self.parametersDF.loc[i, 'volume'] = params['Reactor Volume']
            self.parametersDF.loc[i, 'StartFR'] = fr1
            self.parametersDF.loc[i, 'StopFR'] = fr2
            self.parametersDF.loc[i, 'dead volume 1'] = params['Dead Volume 1']
            self.parametersDF.loc[i, 'Dead Volume 2'] = params['Dead Volume 2']
            self.parametersDF.loc[i, 'Dead Volume 3'] = params['Dead Volume 3']
            self.parametersDF.loc[i, 'NMR interval'] = params['NMR Interval']
            self.parametersDF.loc[i, 'GPC Interval'] = params['GPC Interval']
            self.parametersDF.loc[i,
                                  'stabilisation time'] = params['Stabilization factor']
            self.parametersDF.loc[i,
                                  'Dilution FR'] = params['Dilution Flowrate']
            self.parametersDF.loc[i, 'DeadVolume1(min)'] = self.parametersDF.loc[i,
                                                                                 'dead volume 1']/self.parametersDF.loc[i, 'StopFR']
            self.parametersDF.loc[i, 'DeadVolume2(min)'] = self.parametersDF.loc[i,
                                                                                 'Dead Volume 2']/self.parametersDF.loc[i, 'StopFR']
            self.parametersDF.loc[i, 'DeadVolume3(min)'] = self.parametersDF.loc[i,
                                                                                 'Dead Volume 3']/self.parametersDF.loc[i, 'Dilution FR']
            self.parametersDF.loc[i, 'mode'] = 'GPCandNMR'

        self.parametersDF.to_csv(
            '{}/ExperimentParameters.csv'.format(CommunicationMainFolder))

        self.labelLabview.configure(
            text='Open the LabVIEW and start running the software.')
        self.confirmlabview.configure(state='normal')
        self.HelpLabview.configure(state='normal')
        return code

    def confirmLabview(self):
        '''
        Confirms if LabView is started
        '''

        if not os.path.exists(Pathlastexp_textfile):
            logger.warning('Text file ({}) were experiment folder is saved does not exists.'.format(
                Pathlastexp_textfile))

        self.ExperimentFolder = Path(
            (open(Pathlastexp_textfile, 'r').read().replace("\\", "/")))
        logger.debug(
            'Experiment folder communicated by LabView: {}'.format(self.ExperimentFolder))

        self.ExperimentFolder = Path(
            self.check_experimentFoldertxtfile(self.ExperimentFolder, self.code_en.get()))

        ExperimentFolder_SDRIVE = str(self.ExperimentFolder)
        try:
            ExperimentFolder_SDRIVE = ExperimentFolder_SDRIVE.replace(
                'Z', 'S', 1)
            ExperimentFolder_SDRIVE = Path(ExperimentFolder_SDRIVE)
        except:
            pass

        found = False
        while found == False:
            if self.ExperimentFolder.exists():
                self.labelLabviewInfo.configure(
                    text='Experiment folder found ({})'.format(self.ExperimentFolder))
                logger.info(
                    'Experiment folder found as {}'.format(self.ExperimentFolder))
                found = True
            elif ExperimentFolder_SDRIVE.exists():
                self.ExperimentFolder = ExperimentFolder_SDRIVE
                logger.info(
                    'Experiment folder found as {} (changed to S drive)'.format(self.ExperimentFolder))
                self.labelLabviewInfo.configure(
                    text='Experiment folder found ({})'.format(self.ExperimentFolder))
                found = True
            else:
                self.labelLabviewInfo.configure(
                    text='Experiment folder NOT found.')
                logger.warning('Experiment Folder given by LabView ({}) not found. Please give the correct Experiment Folder.'.format(
                    self.ExperimentFolder))
                self.ExperimentFolder = Path(input('>> '))

        self.experiment_extra.loc[0,
                                  'Mainfolder'] = self.ExperimentFolder
        self.experiment_extra = SearchExperimentFolder(
            self.ExperimentFolder, CommunicationMainFolder, self.experiment_extra, mode='GPCandNMR')

        self.labelPss.configure(
            text='Open the PSSwin software and name the experiment ({}.txt).'.format(self.code_en.get()))
        self.confirmpss.configure(state='normal')
        self.Helppss.configure(state='normal')
        self.confirmlabview.configure(state='disabled')
        self.HelpLabview.configure(state='disabled')

    def confirm_emailadress(self):
        self.addEmail.configure(state='disabled')
        self.entryEmail.configure(state='readonly')
        self.start_btn.configure(state='normal')
        self.confirmEmail.configure(state='disabled')

        self.experiment_extra.to_csv(os.path.join(
            self.experiment_extra.loc[0, 'Softwarefolder'], '{}_extras.csv'.format(self.code_en.get())))
        logger.info('{}_extra.csv saved in {}'.format(
            self.code_en, self.experiment_extra.loc[0, 'Softwarefolder']))

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

    def confirmSpinsolve(self):

        self.labelSpinsolveInfo.configure(text='Spinsolve Check')
        logger.info('Spinsolve is okay')
        self.confirmspinsolve.configure(state='disabled')
        self.Helpspinsolve.configure(state='disabled')
        self.confirmEmail.configure(state='normal')
        self.addEmail.configure(state='normal')
        self.entryEmail.configure(state='normal')
        self.experiment_extra['Emails'] = [[]]
        # self.labelEmailinfo.configure(
        #     text='Optional: Data will be send via email at the end of the experiment')
        # if not email_check:
        #     self.confirm_emailadress()
        #     self.labelEmailinfo.configure(
        #         text='Email function not in use. Connection could not be made.')

    def AddEmail(self):
        return

    def Confirm_reactor_parameters(self):
        logger.info('Reactor parameters confirmed')

        # once confirmed, do not allow further changes by disabling button
        for parameterline in SETUP_DEFAULT_VALUES_NMR:
            parameterline[5].configure(state='disabled')  # button disabled
            parameterline[0].configure(state='readonly')  # entry readonly
        self.go_to_tab(self.tab_NMRGPC_Timesweeps)

    def change_values(self):
        self.parameterList1 = [['entry1', 'default1', 'Reactor Volume', 'mL', 0.90, 'change1'],
                               ['entry2', 'default2', 'Dead Volume 1',
                                   'mL', 0.32, 'change2'],
                               ['entry3', 'default3', 'Dead Volume 2',
                                   'mL', 0.17, 'change3'],
                               ['entry4', 'default4', 'Dead Volume 3',
                                   'mL', 0.17, 'change4'],
                               ['entry5', 'default5', 'NMR Interval',
                                   'sec', 17, 'change5'],
                               ['entry6', 'default6', 'GPC Interval',
                                   'minutes', 3, 'change6'],
                               ['entry7', 'default7', 'Stabilization factor',
                                   'x', 1.3, 'change7'],
                               ['entry8', 'default87', 'Dilution Flowrate', 'mL/min', 1.5, 'change8']]

        list_parameters = self.parameterList1
        entries = [i[0] for i in list_parameters]
        entries_values = [i for i in entries]

        for i, value in enumerate(entries_values):
            if list(value) == []:
                pass
            else:
                if isfloat(value) == True and float(list_parameters[i][4]) != float(value):
                    if float(value) == 0:
                        return print("No changes to parameters")
                    else:
                        self.parameterList1[i][4] = float(value)
                else:
                    pass
        print('Parameters Changed')
        print(self.parameterList1)
