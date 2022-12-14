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
FRAME_FG ='#d9d4d4'
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
        self._make_NMR_setup_screen()
        self._make_welcome_screen()
        self._make_timesweep_frame()
        self._make_conversion_screen()
        self._get_user_names()
        self._get_monomers()
        self._get_ctas()
        self._get_initiators()
        self._make_NMRGPC_initialisation_tab()
        # self._upload_results_pop_up()
        # self._create_experiment_upload_screen()

    def main(self):
        set_appearance_mode("light")  # Modes: system (default), light, dark
        set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
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
        self.tab_NMRGPC_Conversion.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.tab_NMRGPC_Initialisation = Frame(self.tab, width=550, height=550)
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

        self.tab.pack(expand=True)

    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.pack(padx=self.PADDING, pady=self.PADDING, expand=True)

    def _make_timesweep_frame(self):
        NMRGPC_timesweep_top_frame = Frame(self.tab_NMRGPC_Timesweeps,  width=1000, height=50)
        NMRGPC_timesweep_top_frame.pack(pady=3, padx=400)

        NMRGPC_timesweep_picture_frame = Frame(self.tab_NMRGPC_Timesweeps, width=1000, height=300)
        NMRGPC_timesweep_picture_frame.pack(padx=175, pady=3)

        self.NMRGPC_timesweep_parameter_frame = Frame(self.tab_NMRGPC_Timesweeps, width=600, height=350)
        self.NMRGPC_timesweep_parameter_frame.pack()

        self.NMRGPC_timesweep_confirm_frame = Frame(self.tab_NMRGPC_Timesweeps, width=1000, height=50)
        self.NMRGPC_timesweep_confirm_frame.pack()



        self.NMRGPC_timesweep_log_frame = Frame(self.tab_NMRGPC_Timesweeps, width=1000, height=50)
        self.NMRGPC_timesweep_log_frame.pack()

        self.NMRGPC_timesweep_submit_frame = Frame(self.tab_NMRGPC_Timesweeps, width=1000, height=50)
        self.NMRGPC_timesweep_submit_frame.pack()



        # Make-Up Top Frame in Timesweep Tab
        NMRGPC_timesweep_header = CTkLabel(
            NMRGPC_timesweep_top_frame, text='Timesweeps')
        NMRGPC_timesweep_header.configure(font=FONTS['FONT_HEADER'])
        NMRGPC_timesweep_header.grid()

        # Make-Up NMRGPC_timesweep_picture_frame in Timsweep Tab

        # image = Image.open("Image File Path")
        # resize_image = image.resize((500, 500))
        # img = ImageTk.PhotoImage(resize_image)
        # LabelPicture = CTkLabel(image=img)
        # LabelPicture.image = img
        







        picture_timesweep = tk.PhotoImage(
            file='Pictures/Timesweeps_pictureFrame.png', height=300)
        LabelPicture = CTkLabel(
            master=NMRGPC_timesweep_picture_frame, image=picture_timesweep,bg_color='white')
        LabelPicture.grid()

        # Make-Up Parameter_frame_timesweep in Timesweep Tab
        NMRGPC_all_ts_info = []  # list where all the timesweeps will be saved

        # extracts reactorvolume, NMR interval and GPC interval from confirmed setup parameters

        tsparam_header = CTkLabel(self.NMRGPC_timesweep_parameter_frame, text="Insert Timesweep Parameters",
                                  width=27)
        tsparam_header.configure(font=FONTS['FONT_HEADER_BOLD'])
        tsparam_header.grid(row=0, column=1, columnspan=4)

        ts_from_lbl = CTkLabel(self.NMRGPC_timesweep_parameter_frame, text='From (minutes)', width=15,
                               font=FONTS['FONT_NORMAL'], anchor='center')
        ts_from_lbl.grid(row=1, column=2)

        self.ts_from_en = CTkEntry(
            self.NMRGPC_timesweep_parameter_frame, font=FONTS['FONT_ENTRY'])
        self.ts_from_en.grid(row=2, column=2)

        ts_to_lbl = CTkLabel(self.NMRGPC_timesweep_parameter_frame, text='To (minutes)',
                             font=FONTS['FONT_NORMAL'],
                             anchor='center')
        ts_to_lbl.grid(row=1, column=3, padx=(10, 0))

        ts_to_en = CTkEntry(self.NMRGPC_timesweep_parameter_frame,
                            font=FONTS['FONT_ENTRY'])
        ts_to_en.grid(row=2, column=3, padx=(10, 0))
        insert_ts_btm = CTkButton(self.NMRGPC_timesweep_parameter_frame, text='Add', width=60,
                                  command=lambda timesweep_to=ts_to_en,
                                  timesweep_from=self.ts_from_en: self.controller.add_timesweep(
                                      timesweep_to, timesweep_from),
                                  font=FONTS['FONT_BOTTON'])
        insert_ts_btm.grid(row=3, column=2, pady=20, padx=(60, 0))

        delete_ts_btm = CTkButton(self.NMRGPC_timesweep_parameter_frame, text='Delete', width=60,
                                  command=self.controller.delete_timesweep,
                                  font=FONTS['FONT_BOTTON'])
        delete_ts_btm.grid(row=3, column=3, pady=20, padx=(0, 60))

        confirmed_ts = CTkLabel(
            self.NMRGPC_timesweep_parameter_frame, text='List of Timesweeps')
        confirmed_ts.configure(font=FONTS['FONT_HEADER_BOLD'], anchor='w')
        confirmed_ts.grid(row=4, column=2, columnspan=3)

        summary_1 = CTkLabel(self.NMRGPC_timesweep_confirm_frame,
                             text='', width=90, anchor='w', padx=10)
        summary_1.grid(row=1, column=0)

        confirm_ts_btm = CTkButton(self.NMRGPC_timesweep_submit_frame, text='Confirm', height=3, width=15,
                                   command=self.controller.confirm_timesweep, font=FONTS['FONT_BOTTON'])
        confirm_ts_btm.grid()

    def show_timesweep_info(self):

        # Creates 'List of Timesweeps'
        for i, ts_info in enumerate(self.NMRGPC_all_ts_info):
            ts_info[0] = CTkLabel(self.NMRGPC_timesweep_log_frame, text=ts_info[1], bg_color='gray', width=90,
                                  font=FONTS['FONT_SMALL'], anchor='w')

            ts_info[0].grid(row=i, columnspan=5)
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

        popuptitle = CTkLabel(
            self.solution_popup, text='Reaction Solution', font=FONTS['FONT_HEADER'], padx=15)
        popuptitle.grid(row=0, column=0, columnspan=3)
        # monomer
        mLMonomer = CTkEntry(self.solution_popup)  # Entry in Column 1
        mLMonomer.grid(row=1, column=1)

        optionsMonomer = tk.StringVar()
        optionsMonomer.set('MA')
        MenuMonomer = ttk.OptionMenu(self.solution_popup, optionsMonomer,
                                     *self.monomerlist['abbreviation'])  # Menu in Column 0
        MenuMonomer.grid(row=1, column=0)

        monomerlabel = CTkLabel(self.solution_popup,
                                text='mL')  # Unit in column 2
        monomerlabel.grid(row=1, column=2)
        # RAFT
        gramRAFT = CTkEntry(self.solution_popup)
        gramRAFT.grid(row=2, column=1)

        optionsRAFT = tk.StringVar()
        optionsRAFT.set('DoPAT')
        MenuRAFT = tk.OptionMenu(
            self.solution_popup, optionsRAFT, *self.RAFTlist['abbreviation'])
        MenuRAFT.grid(row=2, column=0)

        RAFTlabel = CTkLabel(self.solution_popup, text='g')
        RAFTlabel.grid(row=2, column=2)
        # initator
        graminitiator = CTkEntry(self.solution_popup)
        graminitiator.grid(row=3, column=1)

        optionsinitiator = tk.StringVar()
        optionsinitiator.set("AIBN")
        MenuInitiator = tk.OptionMenu(
            self.solution_popup, optionsinitiator, *self.initiatorlist['abbreviation'])
        MenuInitiator.grid(row=3, column=0)

        initiatorlabel = CTkLabel(self.solution_popup, text='g')
        initiatorlabel.grid(row=3, column=2)
        # solvent
        mLsolvent = CTkEntry(self.solution_popup)
        mLsolvent.grid(row=4, column=1)

        optionsSolvent = tk.StringVar()
        optionsSolvent.set("DMSO")
        MenuSolvent = tk.OptionMenu(
            self.solution_popup, optionsSolvent, *self.solventlist['abbreviation'])
        MenuSolvent.grid(row=4, column=0)

        solventlabel = CTkLabel(self.solution_popup, text='mL')
        solventlabel.grid(row=4, column=2)

        Confirmsolution2 = CTkButton(self.solution_popup, text='Confirm',
                                     command=lambda chemical_list=[gramRAFT, graminitiator, mLMonomer, mLsolvent],
                                     monomer=optionsMonomer, solvent=optionsSolvent,
                                     RAFT=optionsRAFT,
                                     initiator=optionsinitiator: self.controller.confirm_solution(
                                         chemical_list, monomer,
                                         solvent, RAFT, initiator),
                                     font=FONTS['FONT_BOTTON'])  # Upon Confirmation --> confirmSolution()

        Confirmsolution2.grid(row=5, column=1)

    def make_solution_summary_view(self, summary_string):
        solution_summary = CTkLabel(self.NMRGPC_setup_parameter_frame, text='Reaction Solution', bg_color='gray',
                                    font=FONTS['FONT_NORMAL'], pady=20)
        # row i + 1; i last row from parameters
        solution_summary.grid(row=8, column=0, columnspan=2, rowspan=2)

        solution_summary.configure(text=summary_string)

    def go_to_tab(self, next_tab):
        self.tab.select(next_tab)

    
    def _make_welcome_screen(self):
        # s = ttk.Style()
        # s.configure('PViewStyle.Treeview', font=self.FONTS['FONT_HEADER_BOLD'])
        Welcome_top_frame = CTkFrame(
            self.welcome_tab)
        Welcome_top_frame.pack()

        header_Welcome = Label(
            Welcome_top_frame, text='Welcome', font=self.FONTS['FONT_HEADER'])
        header_Welcome.pack()

        Welcome_Option_frame = CTkFrame(self.welcome_tab)
        Welcome_Option_frame.place(relx=0.5, rely=0.50, anchor=CENTER, width='500')
        
        Welcome_option_frame_header = CTkLabel(Welcome_Option_frame, text='Choose a mode of operation',
                                               font=self.FONTS['FONT_HEADER_BOLD'])
        
        
        
        Welcome_option_frame_header.pack()

        optionNMR_btn = CTkButton(Welcome_Option_frame, text="NMR",
                                  font=FONTS['FONT_HEADER_BOLD'],
                                  command=lambda button="NMR Button": self.controller.on_button_click(button))
        self.button_spacing(optionNMR_btn)
        optionNMRGPC_btn = CTkButton(Welcome_Option_frame, text="NMR-GPC", 
                                     font=FONTS['FONT_HEADER_BOLD'],
                                     command=lambda next_tab=self.setup: self.go_to_tab(next_tab))
        self.button_spacing(optionNMRGPC_btn)

        comfolder_label = CTkLabel(
            Welcome_Option_frame, text="Communication Folder",font=FONTS['FONT_HEADER_BOLD'])
        comfolder_label.pack()
        comfolder_path = tk.StringVar(value=self.CommunicationMainFolder)

        comfolder = CTkLabel(Welcome_Option_frame, textvariable=comfolder_path)
        comfolder.pack()
        comfolder_btn = CTkButton(Welcome_Option_frame, text="Browse", command=lambda path=comfolder_path,
                                  folder_type="COMMUNICATION": self.controller.change_file_path(
                                      path, folder_type))
        self.button_spacing(comfolder_btn)

        NMRmainfolder_label = CTkLabel(
            Welcome_Option_frame, text="Spinsolve Folder", font=FONTS['FONT_HEADER_BOLD'])
        NMRmainfolder_label.pack()
        NMRmainfolder_path = tk.StringVar(value=self.NMRFolder)
        NMRmainfolder = CTkLabel(Welcome_Option_frame,
                                 textvariable=NMRmainfolder_path)
        NMRmainfolder.pack()

        NMRmainfolder_btn = CTkButton(Welcome_Option_frame, text="Browse",
                                       command=lambda path=NMRmainfolder_path,
                                       folder_type="NMR": self.controller.change_file_path(path,
                                                                                           folder_type))
        self.button_spacing(NMRmainfolder_btn)

        Psswinmainfolder_label = CTkLabel(
            Welcome_Option_frame, text="Psswin Folder", font=FONTS['FONT_HEADER_BOLD'])
        Psswinmainfolder_label.pack()
        Psswinmainfolder_path = tk.StringVar(value=self.PsswinFolder)
        Psswinmainfolder = CTkLabel(
            Welcome_Option_frame, textvariable=Psswinmainfolder_path)
        Psswinmainfolder.pack()
        Psswinmainfolder_btn = CTkButton(Welcome_Option_frame, text="Browse",
                                          command=lambda path=Psswinmainfolder_path,
                                          folder_type="GPC": self.controller.change_file_path(path,
                                                                                              folder_type))
        self.button_spacing(Psswinmainfolder_btn)

        labviewscript_info = CTkLabel(
            Welcome_Option_frame, text="Labview script", font=FONTS['FONT_ENTRY'])
        labviewscript_info.pack()
        script = CTkLabel(Welcome_Option_frame,
                           text=self.Labviewscript, font=FONTS['FONT_SMALL'])
        script.pack()

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

    def show_final_timesweep_info(self, total_time, total_scan, total_gpc, scan_numbers):
        entry1 = TIMESWEEP_PARAMETERS.iloc[0]
        stabili = ((entry1['Volume'] * entry1['StabilisationTime']))
        allDvs = (((entry1['DeadVolume1'] + entry1['DeadVolume2'] +
                    entry1['DeadVolume3']) * int(scan_numbers.shape[0])))
        ts_number = int(scan_numbers.shape[0])
        totalvolume = stabili + (ts_number * allDvs)

        summary_1 = CTkLabel(self.NMRGPC_timesweep_confirm_frame,
                             text='Total time:             {}min'.format(round(total_time, 1)), width=90, bg_color='gray',
                             anchor='w', padx=10)
        summary_1.grid(row=1, column=0)
        summary_2 = CTkLabel(self.NMRGPC_timesweep_confirm_frame,
                             text='Total NMR scans:         {}'.format(round(total_scan, 0)), width=90, bg_color='gray',
                             anchor='w')
        summary_2.grid(row=2, column=0)
        summary_3 = CTkLabel(self.NMRGPC_timesweep_confirm_frame,
                             text='Total GPC samples:       {}'.format(
                                 round(total_gpc, 0)),
                             width=90, bg_color='gray', anchor='w')
        summary_3.grid(row=3, column=0)
        summary_4 = CTkLabel(self.NMRGPC_timesweep_confirm_frame,
                             text='Volume Needed:       {} mL'.format(round(totalvolume, 1)), width=90, bg_color='gray',
                             anchor='w')
        summary_4.grid(row=4, column=0)

        logger.info(
            'Experiment will take {} minutes; +/- {} mL reaction solution is needed.'.format(total_time, totalvolume))

    def _set_conversion_formula(self, monomer_key):
        Constants.Conversion_values = Constants.Monomer_Conversion[monomer_key]
    def indent_conversion_elements(self, label):
        label.config(padx=(0, 20), pady=(0, 5))

    def _make_conversion_screen(self):

        name_window_conv = CTkLabel(
            self.tab_NMRGPC_Conversion, text='Conversion', font=FONTS['FONT_HEADER'])
        name_window_conv.pack()

        self.NMRGPC_top_frame_conv = CTkFrame( 
            self.tab_NMRGPC_Conversion, 
            fg_color = '#d9d4d4'
        )
        self.NMRGPC_top_frame_conv.place(relx=0.5, rely=0.4, anchor=CENTER, width='500', height='500')




        self.Conversion_option_NMRGPC = tk.StringVar()

        self.IS_radio_NMRGPC = CTkRadioButton(self.NMRGPC_top_frame_conv, text="Internal Standard",
                                              font=FONTS['FONT_ENTRY'],
                                              variable=self.Conversion_option_NMRGPC, value="Internal Standard",
                                              command=self.select_internal_standard)
        self.IS_radio_NMRGPC.pack(pady=(20, 0))


        self.conversion_inputs = CTkFrame(self.NMRGPC_top_frame_conv, fg_color = '#d9d4d4')
        self.conversion_inputs.pack(pady=(15, 15))

        # self.conversion_inputs.configure(padx=15, pady=15)
        self.mol_monomerLabel_NMRGPC = CTkLabel(
            self.conversion_inputs, text="Monomer initial (mol)")
        self.mol_monomerLabel_NMRGPC.pack()

        self.mol_monomerEntry_NMRGPC = CTkEntry(self.conversion_inputs)
        self.mol_monomerEntry_NMRGPC.pack()

        self.mol_ISlabel_NMRGPC = CTkLabel(
            self.conversion_inputs, text="4-hydroxy benzaldehyde initial (mol)")
        self.mol_ISlabel_NMRGPC.pack()

        self.mol_internal_standardEntry_NMRGPC = CTkEntry(
            self.conversion_inputs)
        self.mol_internal_standardEntry_NMRGPC.pack()



        monomer_radio_NMRGPC = CTkRadioButton(self.NMRGPC_top_frame_conv, text="Monomer", font=FONTS['FONT_ENTRY'],
                                              variable=self.Conversion_option_NMRGPC, value="Monomer",
                                              command=self.select_monomer)
        monomer_radio_NMRGPC.pack()
        self.monomer_options_frame = CTkFrame(self.NMRGPC_top_frame_conv, fg_color='#d9d4d4')
        self.monomer_options_frame.pack(pady=(15,15))

        options = tk.StringVar(self.monomer_options_frame)
        options.set("Choose")  # default value
        monomer_options_label = CTkLabel(self.monomer_options_frame,  text='Monomer Options',
                                         font=('Helvetica', 16), width=30, bg_color='#d9d4d4')#, anchor="c")        #############
        monomer_options_label.pack()

        monomer_options_menu = tk.OptionMenu(
            self.monomer_options_frame, options, *Constants.Monomer_Conversion.keys(), command=lambda key=options: self._set_conversion_formula(key))
        monomer_options_menu.config(bg="GREEN", fg="WHITE")
        monomer_options_menu.pack()
        print(options.get())

        solvent_radio_NMRGPC = CTkRadioButton(self.NMRGPC_top_frame_conv, text="Solvent (Butyl Acetate)",
                                              font=FONTS[
                                                  'FONT_ENTRY'], variable=self.Conversion_option_NMRGPC,
                                              value="Solvent (Butyl Acetate)",
                                              command=self.select_solvent)
        solvent_radio_NMRGPC.pack(pady=(30, 15))

        Conversion_info_frame_NMRGPC = CTkFrame(self.NMRGPC_top_frame_conv, fg_color = '#d9d4d4')
        Conversion_info_frame_NMRGPC.pack()

        self.Conversion_Label_NMRGPC = CTkLabel(
            Conversion_info_frame_NMRGPC, text='Choose option')
        self.Conversion_Label_NMRGPC.pack()

        confirm_conv_btn_NMRGPC = CTkButton(Conversion_info_frame_NMRGPC, text='Confirm',
                                            command=lambda conversion_option_chosen=self.Conversion_option_NMRGPC,
                                            field_entries=[self.mol_monomerEntry_NMRGPC,
                                                           self.mol_internal_standardEntry_NMRGPC]: self.controller.confirm_conversion(
                                                conversion_option_chosen.get(), field_entries),
                                            font=FONTS['FONT_BOTTON'])
        confirm_conv_btn_NMRGPC.pack(pady=(9, 40))

    def select_internal_standard(self):
        '''If internal standard option is selected'''
        self.mol_internal_standardEntry_NMRGPC.configure(state='normal')
        self.mol_monomerEntry_NMRGPC.configure(state='normal')
        self.Conversion_Label_NMRGPC.configure(text='Internal Standard')
        self.mol_monomerLabel_NMRGPC.configure(foreground='black')
        self.mol_ISlabel_NMRGPC.configure(foreground='black')

    def select_monomer(self):
        '''If monomer option is selected, IS entry fields are disabled'''
        self.Conversion_Label_NMRGPC.configure(
            text='Conversion will be calculated with monomer peaks (only MA for now)')
        self.mol_internal_standardEntry_NMRGPC.configure(state='disabled')
        self.mol_monomerEntry_NMRGPC.configure(state='disabled')
        self.mol_monomerLabel_NMRGPC.configure(foreground='gray')
        self.mol_ISlabel_NMRGPC.configure(foreground='gray')

    def select_solvent(self):
        '''If solvent option is selected, IS entry fields are disabled'''
        self.Conversion_Label_NMRGPC.configure(
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

        self.setup_main_frame = CTkFrame(self.setup, fg_color = FRAME_FG)
        self.setup_main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.NMRGPC_setup_top_frame = CTkFrame(
            self.setup_main_frame, width=1000, height=50, fg_color = FRAME_FG)
        self.NMRGPC_setup_top_frame.pack(pady=3, padx=400)

        self.NMRGPC_setup_picture_frame =CTkFrame(
            self.setup_main_frame, width=1000, height=30, fg_color = FRAME_FG)
        self.NMRGPC_setup_picture_frame.pack(padx=175, pady=3)

        self.NMRGPC_setup_parameter_frame = CTkFrame(
            self.setup_main_frame, width=1000, height=350, fg_color = FRAME_FG)
        self.NMRGPC_setup_parameter_frame.pack()

        self.NMRGPC_setup_confirm_frame = CTkFrame(
            self.setup_main_frame, width=1000, height=50, fg_color = FRAME_FG)
        self.NMRGPC_setup_confirm_frame.pack(pady=10, padx=400)

        # Make-Up Top Frame
        name_window = CTkLabel(
            self.NMRGPC_setup_top_frame, text='Setup')
        name_window.configure(font=FONTS['FONT_HEADER'])
        name_window.grid()

        # Make-Up Picture_frame
        self.NMRGPC_picure_setup = tk.PhotoImage(
            file='Pictures/NMRGPCsetup.png')
        NMRGPC_LabelPicture = CTkLabel(
            self.NMRGPC_setup_picture_frame, image=self.NMRGPC_picure_setup)
        NMRGPC_LabelPicture.grid(pady=(0, 66))

        for i, entry_values in enumerate(SETUP_DEFAULT_VALUES_NMR):
            parameter = CTkLabel(self.NMRGPC_setup_parameter_frame, text=entry_values[2],
                                 width=30)  # parameter name in column 0
            parameter.configure(font=FONTS['FONT_NORMAL'])
            parameter.grid(row=i, column=0, pady=2, padx=3)

            entry_values[0] = CTkEntry(
                self.NMRGPC_setup_parameter_frame)  # entry in column 1
            entry_values[0].grid(row=i, column=1, pady=2, padx=3)

            unit = CTkLabel(self.NMRGPC_setup_parameter_frame, text=entry_values[3]
                            ,width=10)  # unit in column 2
            # anchor the left of the label (west)
            unit.configure(font=FONTS['FONT_NORMAL'], anchor='w')
            unit.grid(row=i, column=2, pady=2, padx=3)

            entry_values[5] = CTkButton(self.NMRGPC_setup_parameter_frame, text='Change',
                                        command=self.controller.on_change_button_click)  # botton (with text change) in column 3
            entry_values[5].grid(row=i, column=3, pady=2, padx=3)

            entry_values[1] = CTkLabel(self.NMRGPC_setup_parameter_frame, text=entry_values[4])  # default value in column 4
            # anchor to the right of the label (east)
            entry_values[1].configure(font=FONTS['FONT_NORMAL'], anchor='e')
            entry_values[1].grid(row=i, column=4, pady=2, padx=3)

            unit2 = CTkLabel(self.NMRGPC_setup_parameter_frame, text=entry_values[3])  # again unit in column 5
            unit2.configure(font=FONTS['FONT_NORMAL'])
            unit2.grid(row=i, column=5, pady=2, padx=3)

        solutionSummary1 = CTkLabel(self.NMRGPC_setup_parameter_frame, text='Reaction Solution',
                                    font=FONTS['FONT_NORMAL'], pady=20)
        # row i + 1; i last row from parameters
        solutionSummary1.grid(row=i + 1, column=0, columnspan=2, rowspan=2)
        solution_button1 = CTkButton(self.NMRGPC_setup_parameter_frame, text='Reaction solution',
                                     command=self.make_pop_up_tab)
        solution_button1.grid(row=i + 1, column=3)

        # Make-up confirm frame
        confirm_reactorParameters = CTkButton(self.NMRGPC_setup_confirm_frame, text='Confirm',
                                              command=self.Confirm_reactor_parameters, font=FONTS['FONT_BOTTON'])

        confirm_reactorParameters.grid()

    def _make_NMRGPC_initialisation_tab(self):
        # Create Main frame of init Tab
        NMRGPC_main_frame = CTkFrame(
            self.tab_NMRGPC_Initialisation,  width=1000, height=50, fg_color=FRAME_FG)
        NMRGPC_main_frame.pack()

        NMRGPC_top_frame_init = CTkFrame(
            NMRGPC_main_frame,  width=1000, height=50, fg_color=FRAME_FG)

        NMRGPC_top_frame_init.grid(row=0, sticky="ew", pady=3, padx=400)
        # NMRGPC_picture_frame_init = CTkFrame(NMRGPC_main_frame,  width=1000, height=300, fg_color=FRAME_FG)
        # NMRGPC_picture_frame_init.grid(row=1, sticky="nsew",
        #                                      padx=175,
        #                                      pady=3)
        NMRGPC_parameter_frame_init = CTkFrame(NMRGPC_main_frame, width=1000, height=350, fg_color=FRAME_FG)
        NMRGPC_parameter_frame_init.grid(row=3, sticky="ew",
                                               pady=3,
                                               padx=3)
        NMRGPC_btm_frame_init = CTkFrame(
            NMRGPC_main_frame, width=1000, height=50, fg_color=FRAME_FG)
        NMRGPC_btm_frame_init.grid(row=4, sticky="ew", pady=10, padx=400)

        # Make-Up Top Frame in init Tab
        name_window_init = CTkLabel(
            NMRGPC_top_frame_init, text='Initialisation', font=FONTS['FONT_HEADER'])
        name_window_init.grid()

        # Make-Up Parameter_frame_timesweep in ininialisation Tab
        # tsparam = CTkLabel(NMRGPC_parameter_frame_init, text="Start Initialisation",
        #                    font=FONTS['FONT_HEADER_BOLD'])
        # tsparam.grid(row=0, column=1, columnspan=2, padx=150)
        # Experiment code
        code_lbl = CTkLabel(NMRGPC_parameter_frame_init, text='Experiment Code',  width=15,
                            font=FONTS['FONT_NORMAL'])
        code_lbl.grid(row=3, column=0, padx=20)

        self.code_en = CTkEntry(NMRGPC_parameter_frame_init,
                                font=FONTS['FONT_ENTRY'])
        self.code_en.grid(row=3, column=1, columnspan=2, padx=20, pady=30)

        self.labelLabview = CTkLabel(NMRGPC_parameter_frame_init,
                                     text='LABVIEW', font=FONTS['FONT_NORMAL'])
        self.labelLabview.grid(row=5, column=0, columnspan=2)
        
        self.confirmlabview = CTkButton(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'],
                                        command=self.confirmLabview, state='disabled')
        self.confirmlabview.grid(row=5, column=3, padx=20)
        self.HelpLabview = CTkButton(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'],
                                     state='disabled',
                                     command=self.HelpLabView)
        self.HelpLabview.grid(row=5, column=4)
        self.labelLabviewInfo = CTkLabel(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'])
        self.labelLabviewInfo.grid(row=6, column=0, columnspan=2)

        self.labelPss = CTkLabel(
            NMRGPC_parameter_frame_init, text='PSS', font=FONTS['FONT_NORMAL'])
        self.labelPss.grid(row=7, column=0, columnspan=2)
        self.confirmpss = CTkButton(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'], state='disabled',
                                    command=self.confirmPss)
        self.confirmpss.grid(row=7, column=3, padx=20)
        self.Helppss = CTkButton(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'], state='disabled',
                                 command=self.HelpPss)
        self.Helppss.grid(row=7, column=4)
        self.labelPssInfo = CTkLabel(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'])
        self.labelPssInfo.grid(row=8, column=0, columnspan=2)

        self.labelSpinsolve = CTkLabel(
            NMRGPC_parameter_frame_init, text='Spinsolve', font=FONTS['FONT_NORMAL'])
        self.labelSpinsolve.grid(row=9, column=0, columnspan=2)
        self.confirmspinsolve = CTkButton(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'],
                                          state='disabled',
                                          command=self.confirmSpinsolve)
        self.confirmspinsolve.grid(row=9, column=3, padx=20)
        self.Helpspinsolve = CTkButton(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'],
                                       state='disabled',
                                       command=self.HelpSpinsolve)
        self.Helpspinsolve.grid(row=9, column=4)
        self.labelSpinsolveInfo = CTkLabel(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'])
        self.labelSpinsolveInfo.grid(row=10, column=0, columnspan=2)

        self.labelEmail = CTkLabel(
            NMRGPC_parameter_frame_init, text='Email', font=FONTS['FONT_NORMAL'])
        self.labelEmail.grid(row=11, column=0, columnspan=1)
        self.entryEmail = CTkEntry(NMRGPC_parameter_frame_init, font=FONTS['FONT_SMALL'], ###############################
                                   state='readonly')
        self.entryEmail.grid(row=11, column=1, columnspan=1)
        self.confirmEmail = CTkButton(NMRGPC_parameter_frame_init, text='Confirm', font=FONTS['FONT_BOTTON'],
                                      state='disabled',
                                      command=self.confirm_emailadress)
        self.confirmEmail.grid(row=11, column=3, padx=20)
        self.addEmail = CTkButton(NMRGPC_parameter_frame_init, text='Add', font=FONTS['FONT_BOTTON'], state='disabled',
                                  command=self.AddEmail)
        self.addEmail.grid(row=11, column=4)
        self.labelEmailinfo = CTkLabel(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'])
        self.labelEmailinfo.grid(row=12, column=0, columnspan=2)

        self.NMRGPC_confirm_code = CTkButton(NMRGPC_parameter_frame_init, text='OK',
                                             font=FONTS['FONT_BOTTON'], command=self.confirm_code)
        self.NMRGPC_confirm_code.grid(row=3, column=3, padx=20)

        self.start_btn = CTkButton(NMRGPC_btm_frame_init, text='Start',
                                font=FONTS['FONT_HEADER_BOLD'], state='disabled', command=self.startexp)
        self.start_btn.grid()

        # Make-up page
        top_frame_exp = CTkFrame(self.tab_overview,
                              width=1000, height=50, fg_color=FRAME_FG)
        parameter_frame_exp = CTkFrame(self.tab_overview,
                                    width=1000, height=350, fg_color=FRAME_FG)
        top_frame_exp.grid(row=0, sticky="ew", pady=3, padx=400)
        parameter_frame_exp.grid(row=1, sticky="ew")

        # Make-Up Top Frame in exp Tab
        name_window_exp = CTkLabel(top_frame_exp, text='Experiment',
                                font=FONTS['FONT_HEADER'])
        name_window_exp.grid(pady=3)

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

        self.label = CTkLabel(self.experiment_upload_frame_top, text="")
        self.label.grid(row=1, column=3)

        self.label_file_explorer = CTkLabel(self.experiment_upload_frame_top,
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
        self.pop_up_frame_top.geometry("550x750")
        self.pop_up_frame_top.title("Select User for upload")

        pop_up_upload_frame = CTkFrame(
            self.pop_up_frame_top, bg_color='white', width=100, height=50)
        pop_up_upload_frame.grid(pady=3, padx=100)

        options = tk.StringVar(pop_up_upload_frame)
        options.set("Choose")  # default value

        user_label = CTkLabel(pop_up_upload_frame,  text='User',
                              font=('Helvetica', 16), width=30)      #################
        user_label.grid(row=0, column=0, columnspan=4)

        user_options_menu = tk.OptionMenu(
            pop_up_upload_frame, options, *self.dict_a.values(), command=self.get_user_experiments)
        user_options_menu.configure(width=30)
        user_options_menu.grid(row=1, column=0)

        self.name_label = CTkLabel(pop_up_upload_frame,  text='Experiment Name',
                                   font=('Helvetica', 16), width=30)   ########
        self.name_label.grid(row=2, column=0, columnspan=5)

        self.experiment_name_en = CTkEntry(pop_up_upload_frame,
                                           font=FONTS['FONT_ENTRY'], width=30)
        self.experiment_name_en.grid(row=3, column=0)

        self.experiment_name_en.insert(END, self.code_en.get())

        self.monomer_label = CTkLabel(pop_up_upload_frame,  text='Monomer Used',
                                      font=('Helvetica', 16), width=30)      ##########
        self.monomer_label.grid(row=4, column=0, columnspan=5)

        self.monomer_value = tk.StringVar(pop_up_upload_frame)
        self.monomer_value.set("Choose a Monomer")

        self.monomer_name_en = tk.OptionMenu(
            pop_up_upload_frame, self.monomer_value, *self.dict_monomers.values())

        self.monomer_name_en.grid(row=5, column=0)

        self.CTA_label = CTkLabel(pop_up_upload_frame,  text='CTA Used',    
                                  font=('Helvetica', 16), width=30)     ############
        self.CTA_label.grid(row=6, column=0, columnspan=5)

        self.CTA_value = tk.StringVar(pop_up_upload_frame)

        self.CTA_value.set("Choose a CTA")

        self.CTA_en = tk.OptionMenu(
            pop_up_upload_frame, self.CTA_value, *self.dict_ctas.values())

        self.CTA_en.grid()
        ###
        self.initiator_label = CTkLabel(pop_up_upload_frame,  text='Initiator Used',
                                        font=('Helvetica', 16), width=30)       ##################
        self.initiator_label.grid(row=8, column=0, columnspan=5)

        self.Initiator_value = tk.StringVar(pop_up_upload_frame)

        self.Initiator_value.set("Choose a Initiator")

        self.Initiator_en = tk.OptionMenu(
            pop_up_upload_frame, self.Initiator_value, *self.dict_inis.values())

        self.Initiator_en.grid()
        ###

        self.CTA_concentration_label = CTkLabel(pop_up_upload_frame,  text='Enter CTA Concentration',
                                                font=('Helvetica', 16), width=30)       ################
        self.CTA_concentration_label.grid(row=10, column=0, columnspan=5)

        self.CTA_concentration_en = CTkEntry(pop_up_upload_frame,
                                             font=FONTS['FONT_ENTRY'], width=30)
        self.CTA_concentration_en.grid(row=11, column=0)

        self.Monomer_concentration_label = CTkLabel(pop_up_upload_frame,  text='Enter Monomer Concentration',
                                                    font=('Helvetica', 16), width=30)       ###################
        self.Monomer_concentration_label.grid(row=12, column=0, columnspan=5)

        self.Monomer_concentration_en = CTkEntry(pop_up_upload_frame,
                                                 font=FONTS['FONT_ENTRY'], width=30)
        self.Monomer_concentration_en.grid(row=13, column=0)

        self.Initiator_concentration_label = CTkLabel(pop_up_upload_frame,  text='Enter Initiator Concentration',
                                                      font=('Helvetica', 16), width=30)     ############
        self.Initiator_concentration_label.grid(row=14, column=0, columnspan=5)

        self.Initiator_concentration_en = CTkEntry(pop_up_upload_frame,
                                                   font=FONTS['FONT_ENTRY'], width=30)
        self.Initiator_concentration_en.grid(row=15, column=0)

        self.temperature_label = CTkLabel(pop_up_upload_frame,  text='Enter Temperature',
                                          font=('Helvetica', 16), width=30)     ###########
        self.temperature_label.grid(row=16, column=0, columnspan=4)

        self.temperature_en = CTkEntry(pop_up_upload_frame,
                                       font=FONTS['FONT_ENTRY'], width=30)
        self.temperature_en.grid(row=17, column=0)
        self.volume_label = CTkLabel(pop_up_upload_frame,  text='Volume',
                                     font=('Helvetica', 16), width=30)      ##############
        self.volume_label.grid(row=18, column=0, columnspan=4)

        self.volume_en = CTkEntry(pop_up_upload_frame,
                                  font=FONTS['FONT_ENTRY'], width=30)
        self.volume_en.grid(row=19, column=0)

        upload_button = CTkButton(pop_up_upload_frame,  text='Add to Database', width=15,
                                  command=lambda: self.add_experiment_data())
        upload_button.grid(row=20, column=0)
        self.my_str = tk.StringVar()
        l5 = CTkLabel(pop_up_upload_frame,
                      textvariable=self.my_str, width=10)
        l5.grid(row=21, column=0)
        self.my_str.set("Output")

    def add_experiment_data(self):

        flag_validation = True

        self.date = datetime.today().date()
        self.time = datetime.now().time()
        self.exp_name = self.experiment_name_en.get()
        self.temperature = self.temperature_en.get()
        self.volume = self.volume_en.get()
        self.initiator_concentration = self.Initiator_concentration_en.get()
        self.monomer_concentration = self.Monomer_concentration_en.get()
        self.CTA_concentration = self.CTA_concentration_en.get()

        if (len(self.exp_name)) < 2 and (len(self.CTA_concentration) < 1) and (len(self.monomer_concentration) < 1):
            flag_validation = False
        try:

            self.initiator_id = [
                k for k, v in self.dict_inis.items() if v == self.Initiator_value.get()][0]
            print(self.initiator_id)

            self.CTA_id = [
                k for k, v in self.dict_ctas.items() if v == self.CTA_value.get()][0]
            print(self.CTA_id)

            self.monomer_id = [
                k for k, v in self.dict_monomers.items() if v == self.monomer_value.get()][0]
            print(self.monomer_id)
            temp_val = int(self.temperature)  # checking mark as integer
            volume_val = int(self.volume)
            CxCm = float(self.CTA_concentration)
            # print(f"date: {self.date}, time: {self.time} , name: {self.exp_name}, temperature: {self.temperature}, volume: {self.volume}, user_id: {self.wanted_user_id}, monomer_id: {self.monomer_id}, Monomer_concentration:{self.monomer_concentration},CTA_id: {self.CTA_id}, cta_conc {self.CTA_concentration}")

        except:
            flag_validation = False

        if (flag_validation):

            # upload experiment
            query = "INSERT INTO  `experiments_experiment` (`date` ,`time` ,`name` ,`temperature`, `total_volume`,`user_id`,`monomer_id`,`cta_id`,`initiator_id`, `monomer_concentration`, `cta_concentration`, `initiator_concentration`) \
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            my_data = (self.date, self.time, self.exp_name,
                       self.temperature, self.volume, self.wanted_user_id, self.monomer_id, self.CTA_id, self.initiator_id, self.monomer_concentration, self.CTA_concentration, self.initiator_concentration)

            my_retrieval_data = (self.date, self.time, self.exp_name,
                                 self.temperature, self.volume, self.wanted_user_id, int(self.monomer_id), int(self.CTA_id), int(self.initiator_id), self.monomer_concentration, self.CTA_concentration, self.initiator_concentration)
            retrieve_query = "SELECT id FROM  `experiments_experiment` WHERE `date`=%s AND `time`=%s AND `name`=%s AND \
                `temperature`=%s AND `total_volume`=%s AND `user_id`=%s AND `monomer_id`=%s AND `cta_id`=%s AND `initiator_id`=%s AND `monomer_concentration`=%s AND `cta_concentration`=%s AND `initiator_concentration`=%s"
            ex = my_conn.execute(query, my_data)
            row_id = my_conn.execute(retrieve_query, my_retrieval_data)

            self.get_user_experiments(self.v)
            self.pop_up_frame_top.destroy()

        else:
            self.temperature_label.configure(fg='red')   # foreground color
            self.temperature_label.configure(bg_color='yellow')  # background color
            self.volume_label.configure(fg='red')   # foreground color
            self.volume_label.configure(bg_color='yellow')  # background color
            self.name_label.configure(fg='red')
            self.name_label.configure(bg_color='yellow')
            self.CTA_concentration_label.configure(bg_color='yellow')
            self.Monomer_concentration_label.configure(fg='red')
            self.CTA_label.configure(bg_color='yellow')
            self.CTA_label.configure(fg='red')
            self.monomer_label.configure(bg_color='yellow')
            self.monomer_label.configure(fg='red')
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

    def _get_monomers(self):
        list_of_monomers = []
        list_of_monomer_ids = []
        re_set = my_conn.execute("SELECT * FROM measurements_monomer")
        for monomer_ds in re_set:
            list_of_monomer_ids.append(monomer_ds[0])
            list_of_monomers.append(monomer_ds[1])
        self.dict_monomers = dict(
            zip(list_of_monomer_ids, list_of_monomers))

    def _get_ctas(self):
        list_of_ctas = []
        list_of_cta_ids = []
        re_set = my_conn.execute("SELECT * FROM measurements_cta")
        for cta_ds in re_set:
            list_of_ctas.append(cta_ds[1])
            list_of_cta_ids.append(cta_ds[0])
        self.dict_ctas = dict(
            zip(list_of_cta_ids, list_of_ctas))

    def _get_initiators(self):
        list_of_initators = []
        list_of_initiator_ids = []
        re_set = my_conn.execute("SELECT * FROM measurements_initiator")
        for ini_ds in re_set:
            list_of_initators.append(ini_ds[1])
            list_of_initiator_ids.append(ini_ds[0])
        self.dict_inis = dict(
            zip(list_of_initiator_ids, list_of_initators))

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

        while analysis and end_counter < (last_timesweep_row + 25):
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

    def button_spacing(self, button):
        button.pack(pady=(0, 10))

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
