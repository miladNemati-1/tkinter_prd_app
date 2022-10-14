import os

from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.calculateScans import calculate_scans
from code_extra.log_method import setup_logger
from pathlib import Path

logger = setup_logger('App')


def isfloat(Number):
    try:
        is_float = type(float(Number)) == float
    except ValueError:
        is_float = False
    except:
        return "Unknown Error"
    return is_float



class Model:

    def __init__(self):
        """Constructor"""

    def change_folder_path(self, new_parent_folder_path, folder_type):

        if type(new_parent_folder_path) != str:
            new_parent_folder_path = str(new_parent_folder_path.get())
        else:

            new_parent_folder_path = str(new_parent_folder_path.get())

        if not os.path.exists(new_parent_folder_path):
            if folder_type == "COMMUNICATION":
                os.mkdir(new_parent_folder_path)
                logger.info(f'New {folder_type} folder created: {new_parent_folder_path}')
            else:
                logger.info(f'Could not find {folder_type} folder')
        if folder_type == "COMMUNICATION":
            self.create_experiment_txt_files(new_parent_folder_path)
        FOLDERS[f'{folder_type}'] = new_parent_folder_path
        print(FOLDERS)
        logger.info(f"New {folder_type} Folder: {new_parent_folder_path}")


    def create_experiment_txt_files(self, new_parent_folder_path):


        Temporary_textfile = new_parent_folder_path + '/temporary_experiment.txt'
        Pathlastexp_textfile = new_parent_folder_path + '/PathLastExperiment.txt'

        try:
            open(Temporary_textfile, 'w').close()
            open(Pathlastexp_textfile, 'w').close()
            logger.info(f"Experiment text files were created")
        except FileNotFoundError:
            print('If in lab, use Z:/Sci-Chem/...')
            logger.error('If in Lab, use Z drive!')

    def get_communication_folder_paths(self):
        print(FOLDERS['COMMUNICATION'] + "asdasd")
        return FOLDERS['COMMUNICATION'], FOLDERS['COMMUNICATION'] + '/temporary_experiment.txt',  FOLDERS['COMMUNICATION'] + '/PathLastExperiment.txt'



    def change_value(self):
        """
        Changes the values of the setup (NMR mode)
        Note: press any 'change' button and all parameters change
        """
        list_parameters = SETUP_DEFAULT_VALUES_NMR
        entries_values = [i[0].get() for i in
                          list_parameters]  # i[0] are the entry fields of the GUI; .get() extracts the values
        logger.debug(entries_values)

        for i, value in enumerate(entries_values):
            parameter = SETUP_DEFAULT_VALUES_NMR[i][2]  # extracts the parameter
            if not list(value):  # if no entry, pass
                pass
            else:
                if isfloat(value) == True and float(list_parameters[i][4]) != float(
                        value):  # if number is a float (no string) and new value is not the same as old value
                    if float(value) == 0:  # parameter cannot be zero
                        return logger.warning('No changes, entry needs to be non-zero value.')
                    else:
                        old_parameter = SETUP_DEFAULT_VALUES_NMR[i][4]
                        SETUP_DEFAULT_VALUES_NMR[i][4] = float(value)  # Changes the old value to the given new value
                        logger.info(
                            '{} changed from {} to {}'.format(parameter, old_parameter, SETUP_DEFAULT_VALUES_NMR[i][4]))
                else:
                    pass
        print("itemdown")
        for item in SETUP_DEFAULT_VALUES_NMR:
            print(item)
        

    def check_entries_is_float(self, list_entries):
        for entry in list_entries:
            if not isfloat(entry.get()):
                logger.debug('One of the entries ({}) was a not a float'.format(entry.get()))
                return False
        return True
    def if_timesweep_range_is_valid(self, list_timesweep_entries):
        for timesweep_entry in list_timesweep_entries:
            if float(timesweep_entry.get()) <= 0:
                return False, "enter a timesweep higher than 0"
            if self.all_equal(self.get_listof_timesweep_numbers(list_timesweep_entries)):
                return False, "timeweeps cannot be identical"
            if self.check_if_list_value_larger_than_max(list_timesweep_entries, 30):
                return False, "Timeweep range is too large"
            if self.check_correct_timesweep_range(self.get_listof_timesweep_numbers(list_timesweep_entries)):
                return False, "Timesweep range is invalid From is smaller than to"

        return True, ""

    def check_correct_timesweep_range(self, list_of_timesweeps):
        for i in range(len(list_of_timesweeps)-1):
            if list_of_timesweeps[i] > list_of_timesweeps[i+1]:
                return False
        return True

    def get_listof_timesweep_numbers(self, list_timesweep_entries):
        list_of_entries = []
        for item in list_timesweep_entries:
            list_of_entries.append(float(item.get()))
        return list_of_entries


    def all_equal(self, list):

        list_of_entries = iter(list)
        try:
            first = next(list_of_entries)
        except StopIteration:
            return True
        return all(first == x for x in list_of_entries)

    def check_if_list_value_larger_than_max(self, list, max_value):
        for item in list:
            if float(item.get()) > max_value:
                return True
        return False
    def add_timesweep_parameters_to_csv(self, communication_folder_path, time_sweep_info):
        reactorvol = SETUP_DEFAULT_VALUES_NMR[0][4]

        for i, timesweep in enumerate(time_sweep_info):
            fr1, fr2 = reactorvol / timesweep[2], reactorvol / timesweep[3]
            # Create DF with all the parameters
            TIMESWEEP_PARAMETERS.loc[i, 'Start_min'] = timesweep[2]
            TIMESWEEP_PARAMETERS.loc[i, 'Stop_min'] = timesweep[3]
            TIMESWEEP_PARAMETERS.loc[i, 'Volume'] = SETUP_DEFAULT_VALUES_NMR[0][4]
            TIMESWEEP_PARAMETERS.loc[i, 'StartFR'] = fr1
            TIMESWEEP_PARAMETERS.loc[i, 'StopFR'] = fr2
            TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume1'] = SETUP_DEFAULT_VALUES_NMR[1][4]
            TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume2'] = SETUP_DEFAULT_VALUES_NMR[2][4]
            TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume3'] = SETUP_DEFAULT_VALUES_NMR[3][4]
            TIMESWEEP_PARAMETERS.loc[i, 'NMRInterval'] = SETUP_DEFAULT_VALUES_NMR[4][4]
            TIMESWEEP_PARAMETERS.loc[i, 'GPCInterval'] = SETUP_DEFAULT_VALUES_NMR[5][4]
            TIMESWEEP_PARAMETERS.loc[i, 'StabilisationTime'] = SETUP_DEFAULT_VALUES_NMR[6][4]
            TIMESWEEP_PARAMETERS.loc[i, 'DilutionFR'] = SETUP_DEFAULT_VALUES_NMR[7][4]
            TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume1(min)'] = TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume1'] / \
                                                              TIMESWEEP_PARAMETERS.loc[i, 'StopFR']
            TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume2(min)'] = TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume1'] / \
                                                              TIMESWEEP_PARAMETERS.loc[i, 'StopFR']
            TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume3(min)'] = TIMESWEEP_PARAMETERS.loc[i, 'DeadVolume1'] / \
                                                              TIMESWEEP_PARAMETERS.loc[i, 'DilutionFR']
            TIMESWEEP_PARAMETERS.loc[i, 'Mode'] = 'GPCandNMR'

            TIMESWEEP_PARAMETERS.to_csv(os.path.join(communication_folder_path, 'code_Parameters.csv'))
            logger.info('code_Paramters.csv saved in communication folder ({})'.format(communication_folder_path))

    def calculate_scan_numbers(self):
        return calculate_scans(TIMESWEEP_PARAMETERS, mode='GPCandNMR')

    def add_scan_numbers_to_csv(self, communication_folder_path):
        self.scannumbers = self.calculate_scan_numbers()
        self.scannumbers.to_csv(os.path.join(communication_folder_path, 'code_Scans.csv'))
        logger.info('code_Scans.csv saved in communication folder ({})'.format(communication_folder_path))

    def calculate_final_scan_gpc_time(self):
        totalscan = self.scannumbers['Stop Scan GPC'].iloc[-1]
        total_time = (totalscan * TIMESWEEP_PARAMETERS.loc[0, 'NMRInterval']) / 60
        totalgpc = sum([self.scannumbers['GPC Samples'].iloc[i] for i in range(int(self.scannumbers.shape[0]))])

        return totalscan, total_time, totalgpc, self.scannumbers
    def find_solvent(self, solvent_to_find, data_frame):
        all_cells = []
        for item in data_frame:
            for cell_value in data_frame[item]:
                all_cells.append(cell_value)
        if solvent_to_find in all_cells:
            return True




    def add_entries_to_dataframe(self, raft_entry, initiator_entry, monomer_entry, solvent_entry, data_frame):
        # extract entries () and add them to dataframe (new columns are created (mass (g) and volume (mL)) )
        raft_value = float(raft_entry.get())
        initiator_value = float(initiator_entry.get())
        monomer_value = float(monomer_entry.get())
        solvent_value = float(solvent_entry.get())

        data_frame.loc[data_frame['class'] == 'RAFT', 'mass (g)'] = raft_value
        data_frame.loc[data_frame['class'] == 'initiator', 'mass (g)'] = initiator_value
        data_frame.loc[data_frame['class'] == 'monomer', 'volume (mL)'] = monomer_value
        data_frame.loc[data_frame['class'] == 'solvent', 'volume (mL)'] = solvent_value
        # convert volume to mass where needed
        data_frame.loc[data_frame['class'] == 'monomer', 'mass (g)'] = monomer_value * float(
            data_frame.loc[data_frame['class'] == 'monomer', 'density'])
        data_frame.loc[data_frame['class'] == 'solvent', 'mass (g)'] = solvent_value * float(
            data_frame.loc[data_frame['class'] == 'solvent', 'density'])

        # moles in dataframe for all chemicals
        data_frame['moles (mol)'] = data_frame['mass (g)'] / data_frame['molecular mass']
        # molar in dataframe for all entries
        total_volume = data_frame['volume (mL)'].sum()
        data_frame['Molar (M)'] = data_frame['moles (mol)'] / (total_volume / 1000)
        # eq in dataframe for all entries
        moles_RAFT = float(data_frame.loc[data_frame['class'] == 'RAFT', 'moles (mol)'])
        data_frame['eq'] = [i / moles_RAFT for i in data_frame['moles (mol)']]
    def write_experiment_name_to_txt_file(self, txt_file_name, labelLabview, confirmLabview, HelpLabview,experiment_name):
        with open(txt_file_name, "a") as f:
            f.truncate(0)
            f.write('Code,,')
            f.write(experiment_name)
            f.close()

        logger.info(
            'Code ({}) and timesweep parameters are communicated to LabVIEW software'.format(experiment_name))



        labelLabview.configure(text='Open the LabVIEW and start running the software.')
        confirmLabview.configure(state='normal')
        HelpLabview.configure(state='normal')
        return experiment_name
    def check_if_pastexperiment_file_exists(self, path_of_file):
        if not os.path.exists(path_of_file):

            return False
        return True





