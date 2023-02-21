import tkinter as tk
from tkinter import *
from customtkinter import *
from constants import *
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra import Constants


def _make_NMR_setup_screen(self):
    logger.info('Selected mode: NMR and GPC')
    self.tab.select(self.setup)
    ### NMR  - SETUP TAB ###
    # Create Main frame of Setup Tab

    self.setup_main_frame = CTkFrame(self.setup, fg_color=FRAME_FG)
    self.setup_main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    self.NMRGPC_setup_top_frame = CTkFrame(
        self.setup_main_frame, width=1000, height=50, fg_color=FRAME_FG)
    self.NMRGPC_setup_top_frame.pack(pady=3, padx=400)

    self.NMRGPC_setup_picture_frame = CTkFrame(
        self.setup_main_frame, width=1000, height=30, fg_color=FRAME_FG)
    self.NMRGPC_setup_picture_frame.pack(padx=175, pady=3)

    self.NMRGPC_setup_parameter_frame = CTkFrame(
        self.setup_main_frame, width=1000, height=350, fg_color=FRAME_FG)
    self.NMRGPC_setup_parameter_frame.pack()

    self.NMRGPC_setup_confirm_frame = CTkFrame(
        self.setup_main_frame, width=1000, height=50, fg_color=FRAME_FG)
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

        unit = CTkLabel(self.NMRGPC_setup_parameter_frame,
                        text=entry_values[3], width=10)  # unit in column 2
        # anchor the left of the label (west)
        unit.configure(font=FONTS['FONT_NORMAL'], anchor='w')
        unit.grid(row=i, column=2, pady=2, padx=3)

        entry_values[5] = CTkButton(self.NMRGPC_setup_parameter_frame, text='Change',
                                    command=self.controller.on_change_button_click)  # botton (with text change) in column 3
        entry_values[5].grid(row=i, column=3, pady=2, padx=3)

        # default value in column 4
        entry_values[1] = CTkLabel(
            self.NMRGPC_setup_parameter_frame, text=entry_values[4])
        # anchor to the right of the label (east)
        entry_values[1].configure(font=FONTS['FONT_NORMAL'], anchor='e')
        entry_values[1].grid(row=i, column=4, pady=2, padx=3)

        unit2 = CTkLabel(self.NMRGPC_setup_parameter_frame,
                         text=entry_values[3])  # again unit in column 5
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


def isfloat(Number):
    try:
        is_float = type(float(Number)) == float
    except ValueError:
        is_float = False
    except:
        return "Unknown Error"
    return is_float


def Confirm_reactor_parameters(self):
    logger.info('Reactor parameters confirmed')
    # once confirmed, do not allow further changes by disabling button
    for parameterline in SETUP_DEFAULT_VALUES_NMR:
        parameterline[5].configure(state='disabled')  # button disabled
        parameterline[0].configure(state='readonly')  # entry readonly
    self.go_to_tab(self.tab_NMRGPC_Timesweeps)
