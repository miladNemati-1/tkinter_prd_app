import tkinter as tk
from tkinter import *
from customtkinter import *
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.log_method import setup_logger
from constants import logger
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

    confirm_ts_btm = CTkButton(self.NMRGPC_timesweep_submit_frame, text='Confirm',
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


