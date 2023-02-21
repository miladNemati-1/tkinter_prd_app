import pandas as pd
from datetime import timedelta
from tkinter import filedialog
from constants import *

pk = 0
measurement_pk = 0


def get_experiment_pk_for_data_upload(self, v, dict_id_list):
    v = v.get()
    wanted_user_id = (list(dict_id_list.keys())[
                      list(dict_id_list.values()).index(v)])

    set = my_conn.execute(
        f"SELECT * FROM experiments_experiment WHERE id={wanted_user_id}")

    for ds in set:
        global pk
        pk = ds[0]
    return


def csv_to_GPC_table(self, f):
    data = pd.read_csv(f, encoding='UTF-8')
    data_conv = data[['tres_GPC', 'D', 'Mn',
                      'Mw', 'Mn theory']]
    data_conv['measurement_id'] = measurement_pk

    data_conv = data_conv.dropna()

    data['tres_GPC'] = data_conv.apply(
        lambda row: timedelta(minutes=float(row.tres_GPC)).total_seconds(), axis=1)
    print("GPC uploaded to database")

    data_conv.to_sql('measurements_GPC_data', my_conn,
                     if_exists='append', index=False, method='multi')
    print("GPC uploaded to database")
    return


def csv_to_table_nmr(self, f):
    data = pd.read_csv(f, encoding='UTF-8')

    data_conv = data[['conversion', 'tres']]
    data_conv = data_conv.dropna()

    data_conv['tres'] = data_conv.apply(
        lambda row: timedelta(minutes=float(row.tres)).total_seconds(), axis=1)
    data_conv.rename(columns={'conversion': 'result',
                              'tres': 'res_time'}, inplace=True)

    data_conv['measurement_id'] = measurement_pk

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
    add_upload_to_measurement(self,
                              csv_path, is_approved, device_id, pk)

    csv_to_table_nmr(self, f)
    print("NMR uploaded to database")
    csv_to_GPC_table(self, a)
    print("GPC uploaded to database")


def browseFiles(self):
    self.f_types = [('CSV files', "*.csv"), ('All', "*.*")]
    self.filename = filedialog.askopenfilename(filetypes=self.f_types)

    # Change label contents
    self.label_file_explorer.configure(
        text="File Opened: " + self.filename)


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
        global measurement_pk
        measurement_pk = item[0]

    # measurement_pk = a.all()[0][0]
