import view
from code_extra.Constants import TIMESWEEP_PARAMETERS, SETUP_DEFAULT_VALUES_NMR, FOLDERS
from code_extra.defining_folder import SearchExperimentFolder
from model import Model
from view import View
import tkinter as tk
import os
from tkinter import filedialog
from code_extra.calculateScans import calculate_scans
from tkinter import ttk
from code_extra import Constants
from pathlib import Path
import pandas as pd
from syringepump import SyringePump as Pump
import time


experiment_extra = view.pd.DataFrame(
    columns=['code', 'Mainfolder', 'GPCfolder', 'Timesweepfolder', 'Infofolder', 'Softwarefolder', 'Rawfolder',
             'Plotsfolder', 'COMMUNICATION', 'GPC', 'NMR'])


class Controller:
    """"""

    def __init__(self):
        """Constructor"""
        self.model = Model()
        self.view = View(self)

    def main(self):
        self.view.main()

    def on_button_click(self, caption):
        print(f"the button is {caption}")

    def on_change_button_click(self):
        self.model.change_value()
        View.change_values(self.view)

    def calculate_flow_rates(self, timesweep_from, timesweep_to):

        flowrate1, flowrate2 = float(self.view.reactor_volume) / float(timesweep_from.get()), float(
            self.view.reactor_volume) / float(timesweep_to.get())
        return flowrate1, flowrate2

    def add_timesweep(self, timesweep_to_entry, timesweep_from_entry):
        timesweeps = [timesweep_to_entry, timesweep_from_entry]
        print(timesweeps)
        if not self.model.check_entries_is_float(timesweeps):
            self.view.show_warning()
            self.view.clear_fields(timesweep_to_entry, timesweep_from_entry)
            return
        if not self.model.if_timesweep_range_is_valid(timesweeps)[0]:
            self.view.show_warning(
                self.model.if_timesweep_range_is_valid(timesweeps)[1])
            self.view.clear_fields(timesweep_to_entry, timesweep_from_entry)
            return
        self.record_timesweep_info(timesweep_from_entry, timesweep_to_entry)
        self.view.show_timesweep_info()

    def record_timesweep_info(self, timesweep_from_entry, timesweep_to_entry):
        number_of_added_timesweep = len(self.view.NMRGPC_all_ts_info) + 1

        timesweep_from_value, timesweep_to_value = float(
            timesweep_from_entry.get()), float(timesweep_to_entry.get())
        flowrate1, flowrate2 = self.calculate_flow_rates(
            timesweep_to_entry, timesweep_from_entry)
        # Creates list with [the label for the GUI, and the content of the label as string, from_minutes, to_minutes]
        timesweep_info = ['label_{}'.format(number_of_added_timesweep),
                          'Timesweep {}: From {} minutes ({} mL/min) to {} minutes ({} mL/min) (NMR interval: {}sec, GPC interval: {}min)'.format(
                              number_of_added_timesweep, timesweep_from_value, round(
                                  flowrate1, 3), timesweep_to_value,
                              round(flowrate2, 3), self.view.NMRinterval1,
                              self.view.GPCinterval1), timesweep_from_value, timesweep_to_value]
        view.logger.debug(timesweep_info)
        view.logger.info('Timesweep added: {}'.format(timesweep_info[1]))
        self.view.NMRGPC_all_ts_info.append(
            timesweep_info)  # list of lists e.g. [[label_1, text_1] , [label_2, text_2]]

    def delete_timesweep(self):
        if not self.view.NMRGPC_all_ts_info:
            view.logger.info('No timesweeps to delete')
            self.view.show_warning("No Timesweeps to delete")
            return
        view.logger.info('Timesweep deleted: {}'.format(
            self.view.NMRGPC_all_ts_info[-1][-1]))

        # destroys 'label' of last timesweep
        self.view.NMRGPC_all_ts_info[-1][0].destroy()
        self.view.NMRGPC_all_ts_info.pop(-1)

        self.view._make_timesweep_frame()
        self.view.show_timesweep_info()

    def confirm_conversion(self, conversion_option_chosen, internal_standard_entries):

        if conversion_option_chosen == "Internal Standard":
            if not self.model.check_entries_is_float(internal_standard_entries):
                self.view.show_warning()
                self.view.clear_fields(
                    internal_standard_entries[0], internal_standard_entries[1])
                return
            mol_init_monomer = float(internal_standard_entries[0].get())
            mol_init_IS = float(internal_standard_entries[1].get())
            view.logger.info(
                'Conversion will be determined via internal standard peaks (4-hydroxy benzaldehyde; ratio IS/monomer {})'.format(
                    float(mol_init_IS) / float(mol_init_monomer)))

        if conversion_option_chosen == "Monomer":
            view.logger.info(
                'Conversion will be determined via the monomer peaks (no internal standard)')

        if conversion_option_chosen == "Solvent (Butyl Acetate)":
            path = '../CommunicationFolder/code_solution.csv'
            if self.model.find_solvent("Butyl Acetate", view.pd.read_csv(path)):
                view.logger.info(
                    'Conversion will be determined via solvent (butyl acetate) + monomer peak')
        self.view.go_to_tab(self.view.tab_NMRGPC_Initialisation)

    def set_experiment_folders(self, file_path):
        self.model.create_experiment_txt_files(file_path)

    def change_file_path(self, file_path, folder_type):
        filename = filedialog.askdirectory()
        file_path.set(filename)
        self.model.change_folder_path(file_path, folder_type)
        self.view.CommunicationMainFolder, self.view.Temporary_textfile, self.view.Pathlastexp_textfile, = self.model.get_communication_folder_paths()

    def confirm_timesweep(self):
        if not self.view.NMRGPC_all_ts_info:
            self.view.show_warning("Please add at least one timesweep(s)")
            return
        self.model.add_timesweep_parameters_to_csv(
            self.view.CommunicationMainFolder, self.view.NMRGPC_all_ts_info)
        view.logger.info(
            'Confirmed timesweep Experiment:\n{}'.format(TIMESWEEP_PARAMETERS))
        self.model.add_scan_numbers_to_csv(self.view.CommunicationMainFolder)

        total_scan = self.model.calculate_final_scan_gpc_time()[0]
        total_time = self.model.calculate_final_scan_gpc_time()[1]
        total_gpc = self.model.calculate_final_scan_gpc_time()[2]
        self.scan_numbers = self.model.calculate_final_scan_gpc_time()[3]

        self.view.show_final_timesweep_info(
            total_time, total_scan, total_gpc, self.scan_numbers)

        self.view.go_to_tab(self.view.tab_NMRGPC_Conversion)

    def confirm_solution(self, list_entries, finalMonomer, finalSolvent, finalRAFT, finalInitiator):

        finalMonomer = finalMonomer.get()
        finalSolvent = finalSolvent.get()
        finalRAFT = finalRAFT.get()
        finalInitiator = finalInitiator.get()

        view.logger.debug(
            'Selected Chemicals: {}, {}, {}, {}'.format(finalMonomer, finalSolvent, finalRAFT, finalInitiator))
        if not self.model.check_entries_is_float(list_entries):
            self.view.solution_popup.destroy()
            self.view.show_warning()
            self.view.make_pop_up_tab()
        monomer = (
            self.view.monomerlist[self.view.monomerlist['abbreviation'] == finalMonomer])
        solvent = (
            self.view.solventlist[self.view.solventlist['abbreviation'] == finalSolvent])
        raft = (
            self.view.RAFTlist[self.view.RAFTlist['abbreviation'] == finalRAFT])
        initiator = (
            self.view.initiatorlist[self.view.initiatorlist['abbreviation'] == finalInitiator])

        solutionDataFrame = view.pd.concat(
            [raft, monomer, initiator, solvent], ignore_index=True)
        self.model.add_entries_to_dataframe(list_entries[0], list_entries[1], list_entries[2], list_entries[3],
                                            solutionDataFrame)
        raft = solutionDataFrame.iloc[0]
        monomer = solutionDataFrame.iloc[1]
        initiator = solutionDataFrame.iloc[2]
        solvent = solutionDataFrame.iloc[3]

        # Mn for 100% conversion
        Mn_100 = raft['molecular mass'] + \
            (monomer['molecular mass'] * monomer['eq'])

        summaryString = '{}:{}:{}  {} : {} : {} ( {} g/mol);\n {}M {};\n {}'.format(raft['abbreviation'],
                                                                                    monomer['abbreviation'],
                                                                                    initiator['abbreviation'],
                                                                                    round(
                                                                                        raft['eq'], 1),
                                                                                    round(
                                                                                        monomer['eq'], 2),
                                                                                    round(
                                                                                        initiator['eq'], 2),
                                                                                    round(
                                                                                        Mn_100, 1),
                                                                                    round(
                                                                                        monomer['Molar (M)'], 2),
                                                                                    monomer['abbreviation'],
                                                                                    solvent['abbreviation'])

        self.view.solution_popup.destroy()

        view.logger.info('Reaction Solution confirmed: {}'.format(
            summaryString.replace('\n', '')))
        self.view.make_solution_summary_view(summaryString)

        # creates the csv file of the dataframe
        print(self.view.CommunicationMainFolder)
        solutionDataFrame.to_csv(os.path.join(
            self.view.CommunicationMainFolder, 'code_Solution.csv'))
        view.logger.info(
            'code_Solution.csv saved in Communication folder ({})'.format(self.view.CommunicationMainFolder))

    def confirm_experiment_name(self, name_entry, labelLabview, confirmLabview, HelpLabview):
        name_entry_string = name_entry.get()

        # code will later be extracted from path as .split('_')[-1]
        if '_' in name_entry_string:
            self.view.show_warning("Experiment name cannot contain '_' symbol")
            self.view.clear_fields(name_entry)
            return

        self.model.write_experiment_name_to_txt_file(view.Temporary_textfile, labelLabview, confirmLabview, HelpLabview,
                                                     name_entry_string)
        experiment_extra.loc[0, 'code'] = name_entry_string

    def check_experimentFoldertxtfile(self, expfolder, exp_code):
        directory_code = os.path.basename(expfolder).split('_')[-1]
        if not directory_code == exp_code:
            view.logger.warning(
                'It seems that the code given by LabView ({}) does not match the real code ({}). Please give the correct Experiment Folder'.format(
                    directory_code, exp_code))
            experimentfolder = input('>> ')
            return experimentfolder
        return expfolder

    def confirm_labview_com(self, labelLabviewInfo):
        
        code = experiment_extra.loc[0, 'code']
        if not self.model.check_if_pastexperiment_file_exists(view.Pathlastexp_textfile):
            view.logger.warning(
                'Text file ({}) were experiment folder is saved does not exists.'.format(view.Pathlastexp_textfile))

        ExperimentFolder = Path(
            (open(view.Pathlastexp_textfile, 'r').read().replace("\\", "/")))
        view.logger.debug(
            'Experiment folder communicated by LabView: {}'.format(ExperimentFolder))

        ExperimentFolder = Path(
            self.check_experimentFoldertxtfile(ExperimentFolder, code))
        print(ExperimentFolder)

        ExperimentFolder_SDRIVE = str(ExperimentFolder)
        print(ExperimentFolder)
        print(ExperimentFolder_SDRIVE)
        try:
            ExperimentFolder_SDRIVE = ExperimentFolder_SDRIVE.replace(
                'Z', 'S', 1)
            ExperimentFolder_SDRIVE = Path(ExperimentFolder_SDRIVE)
        except:
            pass

        found = False
        while not found:
            if ExperimentFolder.exists():
                labelLabviewInfo.configure(
                    text='Experiment folder found ({})'.format(ExperimentFolder))
                view.logger.info(
                    'Experiment folder found as {}'.format(ExperimentFolder))
                found = True
            elif ExperimentFolder_SDRIVE.exists():
                ExperimentFolder = ExperimentFolder_SDRIVE
                view.logger.info(
                    'Experiment folder found as {} (changed to S drive)'.format(ExperimentFolder))
                labelLabviewInfo.configure(
                    text='Experiment folder found ({})'.format(ExperimentFolder))
                found = True
            else:
                labelLabviewInfo.configure(text='Experiment folder NOT found.')
                view.logger.warning(
                    'Experiment Folder given by LabView ({}) not found. Please give the correct Experiment Folder.'.format(
                        ExperimentFolder))
                ExperimentFolder = Path(input('>> '))
        print(ExperimentFolder)

        experiment_extra.loc[0, 'Mainfolder'] = ExperimentFolder

        self.view.labelPss.configure(
            text='Open the PSSwin software and name the experiment ({}.txt).'.format(code))
        self.view.confirmPss.configure(state='normal')
        self.view.HelpPss.configure(state='normal')
        self.view.confirmLabview.configure(state='disabled')
        self.view.HelpLabview.configure(state='disabled')

    def confirmPss(self):
        self.view.labelPssInfo.configure(text='Pss Check')
        view.logger.info('Psswin is okay')
        self.view.labelSpinsolve.configure(
            text='Name the experiment ({}) in the Spinsolve software.'.format("l"))
        self.view.confirmPss.configure(state='disabled')
        self.view.HelpPss.configure(state='disabled')
        self.view.confirmSpinsolve.configure(state='normal')
        self.view.HelpSpinsolve.configure(state='normal')

    def confirmSpinsolve(self):
        self.view.labelSpinsolveInfo.configure(text='Spinsolve Check')
        view.logger.info('Spinsolve is okay')
        self.view.confirmSpinsolve.configure(state='disabled')
        self.view.HelpSpinsolve.configure(state='disabled')
        self.view.confirmEmail.configure(state='normal')
        self.view.AddEmail.configure(state='normal')
        self.view.entryEmail.configure(state='normal')
        experiment_extra['Emails'] = [[]]
        self.view.labelEmailinfo.configure(
            text='Optional: Data will be send via email at the end of the experiment')


    def confirm_emailadress(self):
        code = experiment_extra.loc[0, 'code']
        experiment_extra.to_csv(os.path.join(
            experiment_extra.loc[0, 'Softwarefolder'], '{}_extras.csv'.format(code)))
        view.logger.info('{}_extra.csv saved in {}'.format(
            code, experiment_extra.loc[0, 'Softwarefolder']))


if __name__ == '__main__':
    app = Controller()
    app.main()
