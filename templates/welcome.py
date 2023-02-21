import tkinter as tk
from tkinter import *
from customtkinter import *
from constants import *
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra import Constants


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
        Welcome_Option_frame.place(relx=0.5, rely=0.40, anchor=CENTER, width='500')
        
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
