from functools import partial
from multiprocessing import Process
from threading import Thread
import threading
import tkinter as tk
from tkinter import *
import subprocess
from customtkinter import *
from constants import *
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra import Constants
from code_extra.start_experiment import starting
from code_extra.calculateScans import calculate_scans
from model import isfloat
import save_plots
import UpdateDF_NMRdata
from time import gmtime, strftime, sleep
import UpdateDF_NMRdata
import UpdateDF_GPCdata
from ExperimentFolder import findexperimentcsvfile
from tkinter import ttk
import datetime
from pathlib import Path
import view
from util import csv
from main import *
import pandas as pd
from syringepump import SyringePump as Pump
import time


def initialise_params(self):
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


def _make_NMRGPC_initialisation_tab(self):
    # Create Main frame of init Tab

    name_window_init = CTkLabel(
        self.tab_NMRGPC_Initialisation, text='Initialisation', font=FONTS['FONT_HEADER'])
    name_window_init.pack()
    NMRGPC_main_frame = CTkFrame(
        self.tab_NMRGPC_Initialisation,  width=1000, height=50, fg_color=FRAME_FG)
    NMRGPC_main_frame.place(relx=0.5, rely=0.4, anchor=CENTER)

    NMRGPC_top_frame_init = CTkFrame(
        NMRGPC_main_frame,  width=1000, height=50, fg_color=FRAME_FG)

    NMRGPC_top_frame_init.grid(row=0, sticky="ew", pady=3, padx=400)
    # NMRGPC_picture_frame_init = CTkFrame(NMRGPC_main_frame,  width=1000, height=300, fg_color=FRAME_FG)
    # NMRGPC_picture_frame_init.grid(row=1, sticky="nsew",
    #                                      padx=175,
    #                                      pady=3)
    NMRGPC_parameter_frame_init = CTkFrame(
        NMRGPC_main_frame, width=1000, height=350, fg_color=FRAME_FG)
    NMRGPC_parameter_frame_init.grid(row=3, sticky="ew",
                                     pady=3,
                                     padx=3)
    NMRGPC_btm_frame_init = CTkFrame(
        NMRGPC_main_frame, width=1000, height=50, fg_color=FRAME_FG)
    NMRGPC_btm_frame_init.grid(row=4, sticky="ew", pady=10, padx=400)

    # Make-Up Top Frame in init Tab
    name_window_init = CTkLabel(
        NMRGPC_top_frame_init, text='', font=FONTS['FONT_HEADER'])
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
    self.entryEmail = CTkEntry(NMRGPC_parameter_frame_init, font=FONTS['FONT_SMALL'],
                               state='readonly')
    self.entryEmail.grid(row=11, column=1, columnspan=1)
    self.confirmEmail = CTkButton(NMRGPC_parameter_frame_init, text='Confirm', font=FONTS['FONT_BOTTON'],
                                  state='disabled',
                                  command=self.confirm_emailadress)
    self.confirmEmail.grid(row=11, column=3, padx=20)
    self.addEmail = CTkButton(NMRGPC_parameter_frame_init, text='Add', font=FONTS['FONT_BOTTON'], state='disabled',
                              )
    self.addEmail.grid(row=11, column=4)
    self.labelEmailinfo = CTkLabel(
        NMRGPC_parameter_frame_init, text='', font=FONTS['FONT_SMALL'])
    self.labelEmailinfo.grid(row=12, column=0, columnspan=2)

    self.NMRGPC_confirm_code = CTkButton(NMRGPC_parameter_frame_init, text='OK',
                                         font=FONTS['FONT_BOTTON'], command=self.confirm_code)
    self.NMRGPC_confirm_code.grid(row=3, column=3, padx=20)

    self.start_btn = CTkButton(NMRGPC_btm_frame_init, text='Start',
                               font=FONTS['FONT_HEADER_BOLD'], state='enabled', command=self.startexp)
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


def _get_user_names(self):
    list_of_experimenters = []
    list_of_experimenter_ids = []
    re_set = my_conn.execute("SELECT * FROM users_user")
    for ds in re_set:
        list_of_experimenters.append(ds[4])
        list_of_experimenter_ids.append(ds[0])
    self.dict_a = dict(
        zip(list_of_experimenter_ids, list_of_experimenters))
    return self.dict_a


def _get_monomers(self):
    list_of_monomers = []
    list_of_monomer_ids = []
    re_set = my_conn.execute("SELECT * FROM measurements_monomer")
    for monomer_ds in re_set:
        list_of_monomer_ids.append(monomer_ds[0])
        list_of_monomers.append(monomer_ds[1])
    self.dict_monomers = dict(
        zip(list_of_monomer_ids, list_of_monomers))
    return self.dict_monomers


def _get_ctas(self):
    list_of_ctas = []
    list_of_cta_ids = []
    re_set = my_conn.execute("SELECT * FROM measurements_cta")
    for cta_ds in re_set:
        list_of_ctas.append(cta_ds[1])
        list_of_cta_ids.append(cta_ds[0])
    self.dict_ctas = dict(
        zip(list_of_cta_ids, list_of_ctas))
    return self.dict_ctas


def _get_initiators(self):
    list_of_initators = []
    list_of_initiator_ids = []
    re_set = my_conn.execute("SELECT * FROM measurements_initiator")
    for ini_ds in re_set:
        list_of_initators.append(ini_ds[1])
        list_of_initiator_ids.append(ini_ds[0])
    self.dict_inis = dict(
        zip(list_of_initiator_ids, list_of_initators))
    return self.dict_inis
    
def startexp(self):
    long_thread = threading.Thread(target=run)
    long_thread.start()
    other_thread = threading.Thread(target= self.start)
    other_thread.start()

def start(self):

    

    nmr_interval = self.parametersDF.loc[0, 'NMR interval']
    code = self.experiment_extra.loc[0, 'code']
    mode = self.parametersDF.loc[0, 'mode']

    startfile = open(Temporary_textfile, 'w')
    startfile.write('start')
    startfile.close()

    logger.info(
        'Experiment started by operator. Start sign is communicated to LabView.')
    print(self.ExperimentFolder)

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
    view._create_experiment_upload_screen()
    view._upload_results_pop_up()
    print('End of Experiment')

    search = findexperimentcsvfile.CSVFileFinder(self.code_en.get())
    self.csvprefill = search.find_experiment_path()
    print("path csv")
    print(self.csvprefill)
    self._upload_results_pop_up()
    self._create_experiment_upload_screen()


def upload_results_pop_up(self):
    self.dict_a = _get_user_names(self)
    self.dict_monomers = _get_monomers(self)
    self.dict_ctas = _get_ctas(self)
    self.dict_init = _get_initiators(self)

    self.pop_up_frame_top = Toplevel()
    self.pop_up_frame_top.geometry("550x750")
    self.pop_up_frame_top.title("Select User for upload")

    pop_up_upload_frame = CTkFrame(
        self.pop_up_frame_top, bg_color='white', width=100, height=50)
    pop_up_upload_frame.grid(pady=3, padx=100)

    options = tk.StringVar(pop_up_upload_frame)
    options.set("Choose")  # default value

    user_label = CTkLabel(pop_up_upload_frame,  text='User',
                          font=('Helvetica', 16), width=30)
    user_label.grid(row=0, column=0, columnspan=4)

    user_options_menu = tk.OptionMenu(
        pop_up_upload_frame, options, *self.dict_a.values(), command=self.get_user_experiments)
    user_options_menu.configure(width=30)
    user_options_menu.grid(row=1, column=0)

    self.name_label = CTkLabel(pop_up_upload_frame,  text='Experiment Name',
                               font=('Helvetica', 16), width=30)
    self.name_label.grid(row=2, column=0, columnspan=5)

    self.experiment_name_en = CTkEntry(pop_up_upload_frame,
                                       font=FONTS['FONT_ENTRY'], width=30)
    self.experiment_name_en.grid(row=3, column=0)

    self.experiment_name_en.insert(END, self.code_en.get())

    self.monomer_label = CTkLabel(pop_up_upload_frame,  text='Monomer Used',
                                  font=('Helvetica', 16), width=30)
    self.monomer_label.grid(row=4, column=0, columnspan=5)

    self.monomer_value = tk.StringVar(pop_up_upload_frame)
    self.monomer_value.set("Choose a Monomer")

    self.monomer_name_en = tk.OptionMenu(
        pop_up_upload_frame, self.monomer_value, *self.dict_monomers.values())

    self.monomer_name_en.grid(row=5, column=0)

    self.CTA_label = CTkLabel(pop_up_upload_frame,  text='CTA Used',
                              font=('Helvetica', 16), width=30)
    self.CTA_label.grid(row=6, column=0, columnspan=5)

    self.CTA_value = tk.StringVar(pop_up_upload_frame)

    self.CTA_value.set("Choose a CTA")

    self.CTA_en = tk.OptionMenu(
        pop_up_upload_frame, self.CTA_value, *self.dict_ctas.values())

    self.CTA_en.grid()
    ###
    self.initiator_label = CTkLabel(pop_up_upload_frame,  text='Initiator Used',
                                    font=('Helvetica', 16), width=30)
    self.initiator_label.grid(row=8, column=0, columnspan=5)

    self.Initiator_value = tk.StringVar(pop_up_upload_frame)

    self.Initiator_value.set("Choose a Initiator")

    self.Initiator_en = tk.OptionMenu(
        pop_up_upload_frame, self.Initiator_value, *self.dict_inis.values())

    self.Initiator_en.grid()
    ###

    self.CTA_concentration_label = CTkLabel(pop_up_upload_frame,  text='Enter CTA Concentration',
                                            font=('Helvetica', 16), width=30)
    self.CTA_concentration_label.grid(row=10, column=0, columnspan=5)

    self.CTA_concentration_en = CTkEntry(pop_up_upload_frame,
                                         font=FONTS['FONT_ENTRY'], width=30)
    self.CTA_concentration_en.grid(row=11, column=0)

    self.Monomer_concentration_label = CTkLabel(pop_up_upload_frame,  text='Enter Monomer Concentration',
                                                font=('Helvetica', 16), width=30)
    self.Monomer_concentration_label.grid(row=12, column=0, columnspan=5)

    self.Monomer_concentration_en = CTkEntry(pop_up_upload_frame,
                                             font=FONTS['FONT_ENTRY'], width=30)
    self.Monomer_concentration_en.grid(row=13, column=0)

    self.Initiator_concentration_label = CTkLabel(pop_up_upload_frame,  text='Enter Initiator Concentration',
                                                  font=('Helvetica', 16), width=30)
    self.Initiator_concentration_label.grid(row=14, column=0, columnspan=5)

    self.Initiator_concentration_en = CTkEntry(pop_up_upload_frame,
                                               font=FONTS['FONT_ENTRY'], width=30)
    self.Initiator_concentration_en.grid(row=15, column=0)

    self.temperature_label = CTkLabel(pop_up_upload_frame,  text='Enter Temperature',
                                      font=('Helvetica', 16), width=30)
    self.temperature_label.grid(row=16, column=0, columnspan=4)

    self.temperature_en = CTkEntry(pop_up_upload_frame,
                                   font=FONTS['FONT_ENTRY'], width=30)
    self.temperature_en.grid(row=17, column=0)
    self.volume_label = CTkLabel(pop_up_upload_frame,  text='Volume',
                                 font=('Helvetica', 16), width=30)
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


def create_experiment_upload_screen(self):

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
        self.experiment_upload_frame_top, default_value, *self.dict_id_list.values(), command=lambda self=self, v=default_value, dict_id_list=self.dict_id_list: csv.get_experiment_pk_for_data_upload(self, v, dict_id_list))
    self.Experiment.grid(row=6,  column=3)


def add_experiment_data(self):
    flag_validation = True
    self.date = datetime.date.today()
    print(self.date)
    self.time = datetime.time()
    print(self.time)
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


def change_values(self):

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

    self.confirmlabview.configure(state='normal')
    self.HelpLabview.configure(state='normal')
    return code


def confirmLabview(self):
    '''
    Confirms if LabView is started
    '''

    parent_directory = '../'
    now = datetime.date.today()
    time = datetime.datetime.now()

    date = f"{now.year}/{now.month}/{now.day}/"
    sesh = time.strftime("%H%M%p")

    folder_name = str(sesh) + "_" + str(self.code_en.get())

    p = parent_directory + date + folder_name

    path = os.path.join(parent_directory, date, folder_name)

    print(p)
    os.makedirs(p)
    self.ExperimentFolder = Path(path)
    print(self.ExperimentFolder)

    SearchCommunicationFolder(self, self.ExperimentFolder)

    self.experiment_extra.loc[0, 'Mainfolder'] = self.ExperimentFolder
    print('LabView Check: Communication folder found, subfolder created in {}.'.format(
        self.ExperimentFolder))
    self.labelLabview.configure(
        text='Name the experiment ({}) in the Spinsolve software.'.format(self.code_en.get()))
    self.labelPss.configure(
        text='Open the PSSwin software and name the experiment ({}.txt).'.format(self.code_en.get()))
    self.confirmSpinsolve2.configure(state='normal')
    self.HelpSpinsolve2.configure(state='normal')
    self.confirmLabview2.configure(state='normal')
    self.HelpLabview2.configure(state='normal')

    self.experiment_extra.loc[0,
                              'Mainfolder'] = self.ExperimentFolder
    self.experiment_extra = SearchExperimentFolder(self,
                                                   self.ExperimentFolder, CommunicationMainFolder, self.experiment_extra, mode='GPCandNMR')

    self.confirmpss.configure(state='normal')
    self.Helppss.configure(state='normal')
    self.confirmlabview.configure(state='normal')
    self.HelpLabview.configure(state='normal')


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
        '{}/parameters.csv'.format(newfoldersoftware))
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

def check_experimentFoldertxtfile(self, expfolder, exp_code):
    directory_code = os.path.basename(expfolder).split('_')[-1]
    if not directory_code == exp_code:
        logger.warning('It seems that the code given by LabView ({}) does not match the real code ({}). Please give the correct Experiment Folder'.format(
            directory_code, exp_code))
        experimentfolder = input('>> ')
        return experimentfolder
    return expfolder


def confirmSpinsolve(self):
    self.labelSpinsolveInfo.configure(text='Spinsolve Check')
    logger.info('Spinsolve is okay')
    self.confirmspinsolve.configure(state='disabled')
    self.Helpspinsolve.configure(state='disabled')
    self.confirmEmail.configure(state='normal')
    self.addEmail.configure(state='normal')
    self.entryEmail.configure(state='normal')
    self.experiment_extra['Emails'] = [[]]


def confirm_emailadress(self):
    self.addEmail.configure(state='disabled')
    self.entryEmail.configure(state='readonly')
    self.start_btn.configure(state='normal')
    self.confirmEmail.configure(state='disabled')

    self.experiment_extra.to_csv(os.path.join(
        self.experiment_extra.loc[0, 'Softwarefolder'], '{}_extras.csv'.format(self.code_en.get())))
    logger.info('{}_extra.csv saved in {}'.format(
        self.code_en, self.experiment_extra.loc[0, 'Softwarefolder']))
