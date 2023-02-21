import tkinter as tk
from tkinter import *
from customtkinter import *
from constants import *
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra import Constants

def make_conversion_screen(self):



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
# '''If internal standard option is selected'''
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