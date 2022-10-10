from email.policy import default
from gc import callbacks
import imp
import tkinter
import tkinter as tk
from tkinter import ttk
from code_extra.defining_folder import defining_communication_folder, defining_PsswinFolder, defining_NMRFolder, \
    SearchExperimentFolder
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
import pandas as pd
from code_extra.log_method import setup_logger
from tkinter import filedialog
import os as a
import pymysql as mdb
import pymysql.connections


#
# my_conn = create_engine("mysql+mysqldb://root@localhost/chemistry")
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
        self._make_NMRGPC_initialisation_tab()
        self._create_experiment_upload_screen()

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

        self.tab.add(self.tab_NMRGPC_Timesweeps, text='Timesweeps')

        self.tab.add(self.tab_NMRGPC_Conversion, text="Conversion")
        self.tab.add(self.tab_overview, text="Experiment")
        self.tab.add(self.welcome_tab, text="Welcome")
        self.tab.add(self.setup, text="Setup")
        self.tab.add(self.tab_NMRGPC_Initialisation, text="NMR GPC Init")
        self.tab.add(self.upload_screen, text="Upload Results")
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
        self.NMRGPC_timesweep_confirm_frame = tk.Frame(self.tab_NMRGPC_Timesweeps, bg='gray', width=1000, height=50, pady=10,
                                                       padx=10)
        self.NMRGPC_timesweep_confirm_frame.grid(row=4, sticky="ew")

        # Make-Up Top Frame in Timesweep Tab
        NMRGPC_timesweep_header = tk.Label(
            NMRGPC_timesweep_top_frame, text='Timesweeps', bg='white')
        NMRGPC_timesweep_header.config(font=FONTS['FONT_HEADER'])
        NMRGPC_timesweep_header.grid()

        # Make-Up NMRGPC_timesweep_picture_frame in Timsweep Tab
        # picture_timesweep = tk.PhotoImage(
        #     file="Pictures/Timesweeps_pictureFrame.png")
        # LabelPicture = tk.Label(
        #     master=NMRGPC_timesweep_picture_frame, image=picture_timesweep, bg='white')
        # LabelPicture.grid(column=2)

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

        insert_ts_btm = tk.Button(self.NMRGPC_timesweep_parameter_frame, text='Add', command=lambda timesweep_to=ts_to_en,
                                  timesweep_from=self.ts_from_en: self.controller.add_timesweep(
                                      timesweep_to, timesweep_from),
                                  font=FONTS['FONT_BOTTON'])
        insert_ts_btm.grid(row=3, column=2)

        delete_ts_btm = tk.Button(self.NMRGPC_timesweep_parameter_frame, text='Delete', command=self.controller.delete_timesweep,
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
                'This is the to_minutes varialbe of the last entred timesweep : {}'.format(self.NMRGPC_all_ts_info[-1][-1]))
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
        print(comfolder_path)
        comfolder = tk.Label(Welcome_Option_frame, textvariable=comfolder_path)
        comfolder.grid(row=4, column=0, columnspan=2)
        comfolder_btn = tk.Button(Welcome_Option_frame, text="Browse", command=lambda path=comfolder_path,
                                  folder_type="COMMUNICATION": self.controller.change_file_path(path, folder_type))
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
                                       command=lambda path=NMRmainfolder_path, folder_type="NMR": self.controller.change_file_path(path, folder_type))
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
                                          command=lambda path=Psswinmainfolder_path, folder_type="GPC": self.controller.change_file_path(path, folder_type))
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
        summary_3 = tk.Label(self.NMRGPC_timesweep_confirm_frame, text='Total GPC samples:       {}'.format(round(total_gpc, 0)),
                             width=90, bg='gray', anchor='w')
        summary_3.grid(row=3, column=0)
        summary_4 = tk.Label(self.NMRGPC_timesweep_confirm_frame,
                             text='Volume Needed:       {} mL'.format(round(totalvolume, 1)), width=90, bg='gray',
                             anchor='w')
        summary_4.grid(row=4, column=0)

        logger.info(
            'Experiment will take {} minutes; +/- {} mL reaction solution is needed.'.format(total_time, totalvolume))

    def _make_conversion_screen(self):

        self.NMRGPC_top_frame_conv = tk.Frame(
            self.tab_NMRGPC_Conversion, bg='white', width=1000, height=50, pady=3, padx=400)
        self.NMRGPC_top_frame_conv.grid(row=0, sticky="ew")

        name_window_conv = tk.Label(
            self.NMRGPC_top_frame_conv, text='Conversion', bg='white', font=FONTS['FONT_HEADER'])
        name_window_conv.grid()
        self.Conversion_option_NMRGPC = tk.StringVar()

        self.IS_radio_NMRGPC = tk.Radiobutton(self.tab_NMRGPC_Conversion, text="Internal Standard", font=FONTS['FONT_ENTRY'],
                                              variable=self.Conversion_option_NMRGPC, value="Internal Standard", command=self.select_internal_standard)
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
                                              variable=self.Conversion_option_NMRGPC, value="Monomer", command=self.select_monomer)
        monomer_radio_NMRGPC.grid()

        solvent_radio_NMRGPC = tk.Radiobutton(self.tab_NMRGPC_Conversion, text="Solvent (Butyl Acetate)",
                                              font=FONTS[
                                                  'FONT_ENTRY'], variable=self.Conversion_option_NMRGPC, value="Solvent (Butyl Acetate)",
                                              command=self.select_solvent)
        solvent_radio_NMRGPC.grid()

        Conversion_info_frame_NMRGPC = tk.Frame(self.tab_NMRGPC_Conversion)
        Conversion_info_frame_NMRGPC.grid()

        self.Conversion_Label_NMRGPC = tk.Label(
            Conversion_info_frame_NMRGPC, text='Choose option')
        self.Conversion_Label_NMRGPC.grid(row=0, column=1, columnspan=3)

        confirm_conv_btm_NMRGPC = tk.Button(Conversion_info_frame_NMRGPC, text='Confirm', height=3, width=15,
                                            command=lambda conversion_option_chosen=self.Conversion_option_NMRGPC, field_entries=[self.mol_monomerEntry_NMRGPC, self.mol_internal_standardEntry_NMRGPC]: self.controller.confirm_conversion(conversion_option_chosen.get(), field_entries), font=FONTS['FONT_BOTTON'])
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
        # self.NMRGPC_picure_setup = tkinter.PhotoImage(
        #     file='None')
        # NMRGPC_LabelPicture = tk.Label(
        #     self.NMRGPC_setup_picture_frame, image=self.NMRGPC_picure_setup, bg='black')
        # NMRGPC_LabelPicture.grid()
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
                                              command=lambda next_tab=self.tab_NMRGPC_Timesweeps: self.go_to_tab(
                                                  next_tab), font=FONTS['FONT_BOTTON'])
        confirm_reactorParameters.grid()

    def db_connect(self):

        try:
            db = mdb.connect('127.0.0.1', 'root', '', 'chemistry')
            self.label.configure(text="Connected Successfully")

        except mdb.Error as e:
            self.label.configure(text="Not Successfully Connected")
    
    def get_user_experiments(self, v):
        print((list(self.dict_a.keys())[list(self.dict_a.values()).index(v)]) )
        wanted_user_id = (list(self.dict_a.keys())[list(self.dict_a.values()).index(v)]) 
        self.experiment_list = []
        val_list = ["None"]

        # experiments = my_conn.execute(f"SELECT * FROM experiments_experiment WHERE user_id={wanted_user_id}")
        # for ds in experiments:
        #     self.experiment_list.append(ds[3])
        #
        # try:
        #     self.Experiment.destroy()
        # except:
        #     pass
        
        default_value = tk.StringVar()
        default_value.set(val_list[0])
        self.Experiment = tk.OptionMenu(
            self.Upload_Screen, default_value ,*self.experiment_list)
        self.Experiment.grid()






        







    def _create_experiment_upload_screen(self):

        button = ttk.Button(
            self.upload_screen, text="Connection Status", command=self.db_connect)
        button.grid()

        self.label = ttk.Label(self.upload_screen, text="")
        self.label.grid()

        self.Upload_Screen = tk.Frame(self.upload_screen, bg='white', width=1000, height=50, pady=3,
                                 padx=400)
        self.Upload_Screen.grid()
        

        list_of_experimenters = []
        list_of_experimenter_ids = []

        # re_set = my_conn.execute("SELECT * FROM users_user")
        # for ds in re_set:
        #     list_of_experimenters.append(ds[4])
        #     list_of_experimenter_ids.append(ds[0])
        # self.dict_a = dict(zip(list_of_experimenter_ids,list_of_experimenters))



        variable = tk.StringVar()
        variable.set(list_of_experimenters[0])



        self.Experimenter = tk.OptionMenu(
            self.Upload_Screen,variable,*self.dict_a.values(),command=self.get_user_experiments)
        self.Experimenter.grid()

        self.experiment_list = ["None"]
        a = tk.StringVar()








    

        variable = tk.StringVar()
        variable.set("one")  # default value

        file_upload = tk.OptionMenu(
            self.Upload_Screen, variable, "one", "two", "three")
        file_upload.grid()

        self.label_file_explorer = tk.Label(self.Upload_Screen,
                                            text="File Explorer using Tkinter")

        button_explore = ttk.Button(self.Upload_Screen,
                                    text="Browse Files",
                                    command=self.browseFiles)

        button_exit = ttk.Button(self.Upload_Screen,
                                 text="Exit",
                                 command=None)
        self.label_file_explorer.grid()

        button_explore.grid()

        button_exit.grid()

    def browseFiles(self):
        f_types = [('CSV files', "*.csv"), ('All', "*.*")]
        filename = filedialog.askopenfilename(filetypes=f_types)

        # Change label contents
        self.label_file_explorer.configure(text="File Opened: " + filename)

    def _make_NMRGPC_initialisation_tab(self):
        # Create Main frame of init Tab
        NMRGPC_top_frame_init = tk.Frame(
            self.tab_NMRGPC_Initialisation, bg='white', width=1000, height=50, pady=3, padx=400)
        NMRGPC_top_frame_init.grid(row=0, sticky="ew")
        NMRGPC_picture_frame_init = tk.Frame(self.tab_NMRGPC_Initialisation, bg='white', width=1000, height=300, padx=175,
                                             pady=3)
        NMRGPC_picture_frame_init.grid(row=1, sticky="nsew")
        NMRGPC_parameter_frame_init = tk.Frame(self.tab_NMRGPC_Initialisation, bg='gray', width=1000, height=350, pady=3,
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

        code_en = tk.Entry(NMRGPC_parameter_frame_init,
                           font=FONTS['FONT_ENTRY'], width=30)
        code_en.grid(row=3, column=1)

        labelLabview = tk.Label(NMRGPC_parameter_frame_init,
                                text='LABVIEW', font=FONTS['FONT_NORMAL'], bg='gray')
        labelLabview.grid(row=5, column=0, columnspan=2)
        self.confirmLabview = tk.Button(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'],
                                        command=lambda labelLabview_view=labelLabview: self.controller.confirm_labview_com(labelLabview_view), state='disabled', width=6)
        self.confirmLabview.grid(row=5, column=3)
        self.HelpLabview = tk.Button(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'], state='disabled',
                                     command=self.temp, width=6)
        self.HelpLabview.grid(row=5, column=4)
        labelLabviewInfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        labelLabviewInfo.grid(row=6, column=0, columnspan=2)

        self.labelPss = tk.Label(
            NMRGPC_parameter_frame_init, text='PSS', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelPss.grid(row=7, column=0, columnspan=2)
        self.confirmPss = tk.Button(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'], state='disabled',
                                    command=self.temp, width=6)
        self.confirmPss.grid(row=7, column=3)
        self.HelpPss = tk.Button(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'], state='disabled',
                                 command=self.temp, width=6)
        self.HelpPss.grid(row=7, column=4)
        self.labelPssInfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelPssInfo.grid(row=8, column=0, columnspan=2)

        self.labelSpinsolve = tk.Label(
            NMRGPC_parameter_frame_init, text='Spinsolve', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelSpinsolve.grid(row=9, column=0, columnspan=2)
        self.confirmSpinsolve = tk.Button(NMRGPC_parameter_frame_init, text='OK', font=FONTS['FONT_BOTTON'], state='disabled',
                                          command=self.temp, width=6)
        self.confirmSpinsolve.grid(row=9, column=3)
        self.HelpSpinsolve = tk.Button(NMRGPC_parameter_frame_init, text='Help', font=FONTS['FONT_BOTTON'], state='disabled',
                                       command=self.temp, width=6)
        self.HelpSpinsolve.grid(row=9, column=4)
        self.labelSpinsolveInfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelSpinsolveInfo.grid(row=10, column=0, columnspan=2)

        self.labelEmail = tk.Label(
            NMRGPC_parameter_frame_init, text='Email', font=FONTS['FONT_NORMAL'], bg='gray')
        self.labelEmail.grid(row=11, column=0, columnspan=1)
        self.entryEmail = tk.Entry(NMRGPC_parameter_frame_init, text='Email', font=FONTS['FONT_SMALL'], state='readonly',
                                   width=30)
        self.entryEmail.grid(row=11, column=1, columnspan=1)
        self.confirmEmail = tk.Button(NMRGPC_parameter_frame_init, text='Confirm', font=FONTS['FONT_BOTTON'], state='disabled',
                                      command=self.temp, width=6)
        self.confirmEmail.grid(row=11, column=3)
        self.AddEmail = tk.Button(NMRGPC_parameter_frame_init, text='Add', font=FONTS['FONT_BOTTON'], state='disabled',
                                  command=self.temp, width=6)
        self.AddEmail.grid(row=11, column=4)
        self.labelEmailinfo = tk.Label(
            NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'], bg='gray')
        self.labelEmailinfo.grid(row=12, column=0, columnspan=2)
