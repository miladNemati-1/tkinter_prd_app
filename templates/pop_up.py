import tkinter as tk
from tkinter import *
from customtkinter import *
from constants import *
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra.Constants import SETUP_DEFAULT_VALUES_NMR, FONTS, TIMESWEEP_PARAMETERS, FOLDERS
from code_extra import Constants
from tkinter import ttk

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